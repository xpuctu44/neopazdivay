from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User


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
def admin_schedule(request: Request, db: Session = Depends(get_db)):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result
    return templates.TemplateResponse(
        "admin.html",
        {"request": request, "title": "Админ — график", "active_tab": "schedule"},
    )


@router.get("/admin/planning", include_in_schema=False)
def admin_planning(request: Request, db: Session = Depends(get_db)):
    result = _ensure_admin(request, db)
    if isinstance(result, RedirectResponse):
        return result
    return templates.TemplateResponse(
        "admin.html",
        {"request": request, "title": "Админ — планирование", "active_tab": "planning"},
    )


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

