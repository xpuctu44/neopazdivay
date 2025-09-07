from datetime import datetime, date, timezone, timedelta

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Attendance, User, AllowedIP


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _get_current_user(request: Request, db: Session) -> User | None:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.get(User, user_id)


def _get_client_ip(request: Request) -> str:
    """Получает реальный IP адрес клиента, учитывая прокси"""
    # Сначала проверяем заголовок X-Forwarded-For (для прокси)
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        # Берем первый IP из списка (реальный клиент)
        client_ip = x_forwarded_for.split(",")[0].strip()
    else:
        # Используем прямой IP от клиента
        client_ip = request.client.host

    return client_ip


def _get_moscow_time() -> datetime:
    """Получает текущее время в московском часовом поясе (UTC+3)"""
    moscow_tz = timezone(timedelta(hours=3))
    return datetime.now(moscow_tz)


def _check_ip_allowed(request: Request, db: Session) -> bool:
    """Проверяет, разрешен ли IP адрес для отметки прихода/ухода"""
    # Получаем IP адрес клиента
    client_ip = _get_client_ip(request)

    # Если нет разрешенных IP, разрешаем всем
    allowed_ips = db.query(AllowedIP).filter(AllowedIP.is_active == True).all()
    if not allowed_ips:
        return True

    # Проверяем первые 3 октета IP (например, 192.168.1.x)
    client_parts = client_ip.split('.')
    if len(client_parts) != 4:
        return False

    client_prefix = '.'.join(client_parts[:3])  # Получаем первые 3 октета

    # Проверяем, есть ли совпадение с разрешенными IP
    for allowed_ip in allowed_ips:
        allowed_parts = allowed_ip.ip_address.split('.')
        if len(allowed_parts) >= 3:
            allowed_prefix = '.'.join(allowed_parts[:3])
            if client_prefix == allowed_prefix:
                return True

    return False


@router.get("/dashboard", include_in_schema=False)
def dashboard(request: Request, db: Session = Depends(get_db)):
    user = _get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    # Only employee flow shows single toggle button
    active = (
        db.query(Attendance)
        .filter(Attendance.user_id == user.id, Attendance.ended_at.is_(None))
        .first()
    )
    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "title": "Dashboard",
            "user": user,
            "is_active": bool(active),
            "start_time": active.started_at if active else None,
        },
    )


@router.post("/attendance/start", include_in_schema=False)
def start_attendance(request: Request, db: Session = Depends(get_db)):
    user = _get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    # Проверяем IP адрес
    if not _check_ip_allowed(request, db):
        return RedirectResponse(url="/dashboard?error=ip_not_allowed", status_code=status.HTTP_303_SEE_OTHER)

    # If already started, just redirect
    existing = (
        db.query(Attendance)
        .filter(Attendance.user_id == user.id, Attendance.ended_at.is_(None))
        .first()
    )
    if existing:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)

    now = _get_moscow_time()
    record = Attendance(
        user_id=user.id,
        started_at=now,
        work_date=now.date(),  # Используем дату из московского времени
    )
    db.add(record)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/attendance/stop", include_in_schema=False)
def stop_attendance(request: Request, db: Session = Depends(get_db)):
    user = _get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    # Проверяем IP адрес
    if not _check_ip_allowed(request, db):
        return RedirectResponse(url="/dashboard?error=ip_not_allowed", status_code=status.HTTP_303_SEE_OTHER)

    active = (
        db.query(Attendance)
        .filter(Attendance.user_id == user.id, Attendance.ended_at.is_(None))
        .first()
    )
    if not active:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)

    now = _get_moscow_time()
    active.ended_at = now

    # compute duration in hours - handle both timezone-aware and naive datetimes
    started_at = active.started_at
    ended_at = active.ended_at

    # If started_at is naive, assume it's in UTC (since that's what datetime.utcnow() produces)
    if started_at.tzinfo is None:
        utc_tz = timezone.utc
        started_at = started_at.replace(tzinfo=utc_tz)

    elapsed_seconds = (ended_at - started_at).total_seconds()
    active.hours = round(elapsed_seconds / 3600.0, 4)
    db.add(active)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
