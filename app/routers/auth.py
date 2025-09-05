from datetime import date

from fastapi import APIRouter, Depends, Form, Request, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User
from app.security import hash_password


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/register", include_in_schema=False)
def register_page(request: Request):
    success = request.query_params.get("success")
    return templates.TemplateResponse(
        "register.html",
        {
            "request": request,
            "title": "Регистрация",
            "success": bool(success),
            "error": None,
        },
    )


@router.post("/register", include_in_schema=False)
def register_user(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    full_name: str = Form(""),
    date_of_birth: date | None = Form(None),
    role: str = Form("employee"),
    db: Session = Depends(get_db),
):
    role_normalized = role.lower()
    if role_normalized not in ("admin", "employee"):
        role_normalized = "employee"

    existing = db.query(User).filter(User.email == email).first()
    if existing:
        return templates.TemplateResponse(
            "register.html",
            {
                "request": request,
                "title": "Регистрация",
                "error": "Пользователь с такой почтой уже существует",
                "success": False,
            },
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    user = User(
        email=email,
        full_name=full_name or None,
        hashed_password=hash_password(password),
        role=role_normalized,
        date_of_birth=date_of_birth,
    )
    db.add(user)
    db.commit()

    return RedirectResponse(url="/register?success=1", status_code=status.HTTP_303_SEE_OTHER)

