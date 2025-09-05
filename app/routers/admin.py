from datetime import date
import calendar

from fastapi import APIRouter, Depends, Request, status, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, ScheduleEntry


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _current_user(request: Request, db: Session) -> User | None:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.get(User, user_id)


def _admin_guard(request: Request, db: Session) -> User | None:
    user = _current_user(request, db)
    if not user:
        return None
    if user.role != "admin":
        return None
    return user


def _ensure_admin(request: Request, db: Session):
    user = _admin_guard(request, db)
    if not user:
        if not request.session.get("user_id"):
            return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
    return user


@router.get("/admin", include_in_schema=False)
def admin_root(request: Request, db: Session = Depends(get_db)):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result
    return templates.TemplateResponse(
        "admin.html",
        {"request": request, "title": "Админ — график", "active_tab": "schedule"},
    )


@router.get("/admin/schedule", include_in_schema=False)
def admin_schedule(request: Request, db: Session = Depends(get_db), year: int | None = None, month: int | None = None):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result
    today = date.today()
    y = year or today.year
    m = month or today.month
    days_in_month = calendar.monthrange(y, m)[1]
    days = list(range(1, days_in_month + 1))
    employees = db.query(User).filter(User.role == "employee", User.is_active == True).order_by(User.full_name.nulls_last()).all()

    # Load published entries for the month
    first_day = date(y, m, 1)
    last_day = date(y, m, days_in_month)
    entries = (
        db.query(ScheduleEntry)
        .filter(
            ScheduleEntry.work_date >= first_day,
            ScheduleEntry.work_date <= last_day,
            ScheduleEntry.published == True,
        )
        .all()
    )
    entry_map: dict[tuple[int, int], str] = {}
    for e in entries:
        entry_map[(e.user_id, e.work_date.day)] = e.shift_type
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "title": "Админ — график",
            "active_tab": "schedule",
            "year": y,
            "month": m,
            "days": days,
            "employees": employees,
            "entry_map": entry_map,
            "shift_labels": {
                "work": "Рабочий",
                "off": "Отгул",
                "vacation": "Отпуск",
                "sick": "Больничный",
                "weekend": "Выходной",
            },
            "readonly": True,
        },
    )


@router.get("/admin/planning", include_in_schema=False)
def admin_planning(request: Request, db: Session = Depends(get_db), year: int | None = None, month: int | None = None):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result
    today = date.today()
    y = year or today.year
    m = month or today.month
    days_in_month = calendar.monthrange(y, m)[1]
    days = list(range(1, days_in_month + 1))
    employees = db.query(User).filter(User.role == "employee", User.is_active == True).order_by(User.full_name.nulls_last()).all()

    # Load draft (unpublished) entries for the month
    first_day = date(y, m, 1)
    last_day = date(y, m, days_in_month)
    entries = (
        db.query(ScheduleEntry)
        .filter(
            ScheduleEntry.work_date >= first_day,
            ScheduleEntry.work_date <= last_day,
            ScheduleEntry.published == False,
        )
        .all()
    )
    entry_map: dict[tuple[int, int], str] = {}
    for e in entries:
        entry_map[(e.user_id, e.work_date.day)] = e.shift_type
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "title": "Админ — планирование",
            "active_tab": "planning",
            "year": y,
            "month": m,
            "days": days,
            "employees": employees,
            "entry_map": entry_map,
            "shift_labels": {
                "work": "Рабочий",
                "off": "Отгул",
                "vacation": "Отпуск",
                "sick": "Больничный",
                "weekend": "Выходной",
            },
            "readonly": False,
        },
    )


@router.post("/admin/planning/save", include_in_schema=False)
def admin_planning_save(
    request: Request,
    db: Session = Depends(get_db),
    year: int = Form(...),
    month: int = Form(...),
):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result
    days_in_month = calendar.monthrange(year, month)[1]
    first_day = date(year, month, 1)
    last_day = date(year, month, days_in_month)

    # Remove existing draft entries for the range
    db.query(ScheduleEntry).filter(
        ScheduleEntry.work_date >= first_day,
        ScheduleEntry.work_date <= last_day,
        ScheduleEntry.published == False,
    ).delete(synchronize_session=False)

    # Parse fields like shift_{userId}_{day}
    form = await request.form()
    for key, value in form.items():
        if not key.startswith("shift_"):
            continue
        if not value:
            continue
        _, uid_str, day_str = key.split("_", 2)
        try:
            uid = int(uid_str)
            d = int(day_str)
        except ValueError:
            continue
        if d < 1 or d > days_in_month:
            continue
        shift = value
        if shift not in {"work", "off", "vacation", "sick", "weekend"}:
            continue
        entry = ScheduleEntry(
            user_id=uid,
            work_date=date(year, month, d),
            shift_type=shift,
            published=False,
        )
        db.add(entry)
    db.commit()

    return RedirectResponse(url=f"/admin/planning?year={year}&month={month}", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/admin/planning/publish", include_in_schema=False)
def admin_planning_publish(
    request: Request,
    db: Session = Depends(get_db),
    year: int = Form(...),
    month: int = Form(...),
):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result
    days_in_month = calendar.monthrange(year, month)[1]
    first_day = date(year, month, 1)
    last_day = date(year, month, days_in_month)

    db.query(ScheduleEntry).filter(
        ScheduleEntry.work_date >= first_day,
        ScheduleEntry.work_date <= last_day,
        ScheduleEntry.published == False,
    ).update({ScheduleEntry.published: True}, synchronize_session=False)
    db.commit()

    return RedirectResponse(url=f"/admin/schedule?year={year}&month={month}", status_code=status.HTTP_303_SEE_OTHER)


@router.get("/admin/reports", include_in_schema=False)
def admin_reports(request: Request, db: Session = Depends(get_db)):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result
    return templates.TemplateResponse(
        "admin.html",
        {"request": request, "title": "Админ — отчеты", "active_tab": "reports"},
    )


@router.get("/admin/users", include_in_schema=False)
def admin_users(request: Request, db: Session = Depends(get_db)):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result
    return templates.TemplateResponse(
        "admin.html",
        {"request": request, "title": "Админ — сотрудники", "active_tab": "users"},
    )

