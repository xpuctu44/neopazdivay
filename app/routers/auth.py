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
    admin_secret: str | None = Form(None),
    db: Session = Depends(get_db),
):
    role_normalized = role.lower()
    if role_normalized not in ("admin", "employee"):
        role_normalized = "employee"

    # Require secret code for admin registration
    if role_normalized == "admin":
        if not admin_secret or admin_secret != "20252025":
            return templates.TemplateResponse(
                "register.html",
                {
                    "request": request,
                    "title": "Регистрация",
                    "error": "Для регистрации администратора введите верный секретный код",
                    "success": False,
                },
                status_code=status.HTTP_400_BAD_REQUEST,
            )

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


@router.get("/login", include_in_schema=False)
def login_page(request: Request):
    return templates.TemplateResponse(
        "login.html",
        {
            "request": request,
            "title": "Вход",
            "error": None,
        },
    )


@router.post("/login", include_in_schema=False)
def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "title": "Вход", "error": "Неверная почта или пароль"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )
    # Password verification is optional for now since we do not import verify
    # For correctness, use security.verify_password
    from app.security import verify_password

    if not verify_password(password, user.hashed_password):
        return templates.TemplateResponse(
            "login.html",
            {"request": request, "title": "Вход", "error": "Неверная почта или пароль"},
            status_code=status.HTTP_400_BAD_REQUEST,
        )

    request.session["user_id"] = user.id
    request.session["role"] = user.role
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)


@router.post("/logout", include_in_schema=False)
def logout(request: Request):
    request.session.clear()
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

