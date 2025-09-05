from datetime import date
import calendar

from fastapi import APIRouter, Depends, Request, status, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, ScheduleEntry, Store


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
def admin_schedule(request: Request, db: Session = Depends(get_db), year: int | None = None, month: int | None = None, store_id: int | None = None):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result
    today = date.today()
    y = year or today.year
    m = month or today.month
    days_in_month = calendar.monthrange(y, m)[1]
    days = list(range(1, days_in_month + 1))
    q = db.query(User).filter(User.role == "employee", User.is_active == True)
    if store_id:
        q = q.filter(User.store_id == store_id)
    employees = q.order_by(User.full_name.nulls_last()).all()
    stores = db.query(Store).filter(Store.is_active == True).order_by(Store.name).all()
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
            "store_id": store_id,
            "stores": stores,
        },
    )


@router.get("/admin/planning", include_in_schema=False)
def admin_planning(request: Request, db: Session = Depends(get_db), year: int | None = None, month: int | None = None, store_id: int | None = None):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result
    today = date.today()
    y = year or today.year
    m = month or today.month
    days_in_month = calendar.monthrange(y, m)[1]
    days = list(range(1, days_in_month + 1))
    q = db.query(User).filter(User.role == "employee", User.is_active == True)
    if store_id:
        q = q.filter(User.store_id == store_id)
    employees = q.order_by(User.full_name.nulls_last()).all()
    stores = db.query(Store).filter(Store.is_active == True).order_by(Store.name).all()
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
            "store_id": store_id,
            "stores": stores,
        },
    )


@router.post("/admin/planning/save", include_in_schema=False)
async def admin_planning_save(
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


@router.get("/admin/reports/shifts", include_in_schema=False)
def admin_reports_shifts(
    request: Request,
    db: Session = Depends(get_db),
    user_id: int | None = None,
    year: int | None = None,
    month: int | None = None,
):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result

    from app.models import Attendance
    today = date.today()
    y = year or today.year
    m = month or today.month
    days_in_month = calendar.monthrange(y, m)[1]
    first_day = date(y, m, 1)
    last_day = date(y, m, days_in_month)

    employees = db.query(User).filter(User.role == "employee").order_by(User.full_name.nulls_last()).all()
    selected_user = db.get(User, user_id) if user_id else None
    entries = []
    if selected_user:
        entries = (
            db.query(Attendance)
            .filter(
                Attendance.user_id == selected_user.id,
                Attendance.work_date >= first_day,
                Attendance.work_date <= last_day,
            )
            .order_by(Attendance.work_date.asc(), Attendance.started_at.asc())
            .all()
        )

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "title": "Админ — отчеты по сменам",
            "active_tab": "reports_shifts",
            "employees": employees,
            "selected_user": selected_user,
            "entries": entries,
            "year": y,
            "month": m,
        },
    )


@router.post("/admin/reports/shifts/update", include_in_schema=False)
async def admin_reports_shifts_update(
    request: Request,
    db: Session = Depends(get_db),
):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result

    from app.models import Attendance
    form = await request.form()
    attendance_id = int(form.get("attendance_id"))
    started_at_str = form.get("started_at")
    ended_at_str = form.get("ended_at")
    back = form.get("back") or "/admin/reports/shifts"

    from datetime import datetime
    started_at = datetime.fromisoformat(started_at_str) if started_at_str else None
    ended_at = datetime.fromisoformat(ended_at_str) if ended_at_str else None

    row = db.get(Attendance, attendance_id)
    if row and started_at:
        row.started_at = started_at
        row.work_date = started_at.date()
        row.ended_at = ended_at
        if row.ended_at and row.started_at:
            elapsed_seconds = (row.ended_at - row.started_at).total_seconds()
            row.hours = round(max(elapsed_seconds, 0) / 3600.0, 4)
        else:
            row.hours = None
        db.add(row)
        db.commit()

    return RedirectResponse(url=back, status_code=status.HTTP_303_SEE_OTHER)


@router.get("/admin/reports", include_in_schema=False)
def admin_reports(request: Request, db: Session = Depends(get_db), year: int | None = None, month: int | None = None):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result

    today = date.today()
    y = year or today.year
    m = month or today.month
    days_in_month = calendar.monthrange(y, m)[1]
    first_day = date(y, m, 1)
    last_day = date(y, m, days_in_month)

    employees = db.query(User).filter(User.role == "employee", User.is_active == True).order_by(User.full_name.nulls_last()).all()

    # Aggregate actual worked hours from Attendance
    from app.models import Attendance, ScheduleEntry

    hours_by_user = {}
    attendance = (
        db.query(Attendance)
        .filter(Attendance.work_date >= first_day, Attendance.work_date <= last_day)
        .all()
    )
    for a in attendance:
        if a.hours is None:
            continue
        hours_by_user[a.user_id] = hours_by_user.get(a.user_id, 0.0) + float(a.hours)

    # Aggregate counts from published schedules (off/vacation/sick)
    entries = (
        db.query(ScheduleEntry)
        .filter(
            ScheduleEntry.work_date >= first_day,
            ScheduleEntry.work_date <= last_day,
            ScheduleEntry.published == True,
            ScheduleEntry.shift_type.in_(["off", "vacation", "sick"]),
        )
        .all()
    )
    off_by_user = {}
    sick_by_user = {}
    vac_by_user = {}
    for e in entries:
        if e.shift_type == "off":
            off_by_user[e.user_id] = off_by_user.get(e.user_id, 0) + 1
        elif e.shift_type == "sick":
            sick_by_user[e.user_id] = sick_by_user.get(e.user_id, 0) + 1
        elif e.shift_type == "vacation":
            vac_by_user[e.user_id] = vac_by_user.get(e.user_id, 0) + 1

    rows = []
    for emp in employees:
        rows.append({
            "emp": emp,
            "hours": round(hours_by_user.get(emp.id, 0.0), 2),
            "off": off_by_user.get(emp.id, 0),
            "sick": sick_by_user.get(emp.id, 0),
            "vacation": vac_by_user.get(emp.id, 0),
        })

    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "title": "Админ — отчеты",
            "active_tab": "reports",
            "year": y,
            "month": m,
            "report_rows": rows,
        },
    )


@router.get("/admin/users", include_in_schema=False)
def admin_users(request: Request, db: Session = Depends(get_db), store_id: int | None = None):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result
    stores = db.query(Store).filter(Store.is_active == True).order_by(Store.name).all()
    q = db.query(User).filter(User.role == "employee")
    if store_id:
        q = q.filter(User.store_id == store_id)
    employees = q.order_by(User.full_name.nulls_last()).all()
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "title": "Админ — сотрудники",
            "active_tab": "users",
            "stores": stores,
            "employees": employees,
            "selected_store_id": store_id,
        },
    )


@router.post("/admin/users/assign_store", include_in_schema=False)
async def admin_users_assign_store(
    request: Request,
    db: Session = Depends(get_db),
):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result
    form = await request.form()
    user_id = int(form.get("user_id"))
    store_id = form.get("store_id")
    store_id_int = int(store_id) if store_id else None
    user = db.get(User, user_id)
    if user:
        user.store_id = store_id_int
        db.add(user)
        db.commit()
    back = form.get("back") or "/admin/users"
    return RedirectResponse(url=back, status_code=status.HTTP_303_SEE_OTHER)


@router.get("/admin/stores", include_in_schema=False)
def admin_stores(request: Request, db: Session = Depends(get_db)):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result
    stores = db.query(Store).order_by(Store.is_active.desc(), Store.name).all()
    return templates.TemplateResponse(
        "admin.html",
        {
            "request": request,
            "title": "Админ — магазины",
            "active_tab": "stores",
            "stores": stores,
        },
    )


@router.post("/admin/stores/add", include_in_schema=False)
async def admin_stores_add(request: Request, db: Session = Depends(get_db)):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result
    form = await request.form()
    name = (form.get("name") or "").strip()
    address = (form.get("address") or "").strip() or None
    if name:
        exists = db.query(Store).filter(Store.name == name).first()
        if not exists:
            store = Store(name=name, address=address)
            db.add(store)
            db.commit()
    return RedirectResponse(url="/admin/stores", status_code=status.HTTP_303_SEE_OTHER)

