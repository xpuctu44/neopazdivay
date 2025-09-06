from datetime import datetime, date

from fastapi import APIRouter, Depends, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import Attendance, User


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


def _get_current_user(request: Request, db: Session) -> User | None:
    user_id = request.session.get("user_id")
    if not user_id:
        return None
    return db.get(User, user_id)


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
    # If already started, just redirect
    existing = (
        db.query(Attendance)
        .filter(Attendance.user_id == user.id, Attendance.ended_at.is_(None))
        .first()
    )
    if existing:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)

    now = datetime.utcnow()
    record = Attendance(
        user_id=user.id,
        started_at=now,
        work_date=date.today(),
    )
    db.add(record)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/attendance/stop", include_in_schema=False)
def stop_attendance(request: Request, db: Session = Depends(get_db)):
    user = _get_current_user(request, db)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    active = (
        db.query(Attendance)
        .filter(Attendance.user_id == user.id, Attendance.ended_at.is_(None))
        .first()
    )
    if not active:
        return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)

    now = datetime.utcnow()
    active.ended_at = now
    # compute duration in hours
    elapsed_seconds = (active.ended_at - active.started_at).total_seconds()
    active.hours = round(elapsed_seconds / 3600.0, 4)
    db.add(active)
    db.commit()
    return RedirectResponse(url="/dashboard", status_code=status.HTTP_303_SEE_OTHER)
