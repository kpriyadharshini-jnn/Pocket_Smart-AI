from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response

from sqlalchemy import select
from sqlalchemy.orm import Session

from ..auth import COOKIE_NAME
from ..auth import create_access_token
from ..auth import current_user
from ..auth import hash_password
from ..auth import verify_password

from ..database import get_db

from ..models import User

from ..schemas import LoginRequest
from ..schemas import RegisterRequest


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)


@router.post("/register")
def register(
    data: RegisterRequest,
    db: Session = Depends(get_db)
):

    email = data.email.lower()

    existing_user = db.scalar(
        select(User).where(
            User.email == email
        )
    )

    if existing_user:

        raise HTTPException(
            status_code=409,
            detail="An account with this email already exists."
        )

    user = User(
        email=email,
        full_name=data.full_name.strip(),
        password_hash=hash_password(
            data.password
        )
    )

    db.add(user)

    db.commit()

    db.refresh(user)

    return {
        "message": "Registration successful.",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email
        }
    }


@router.post("/login")
def login(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db)
):

    user = db.scalar(
        select(User).where(
            User.email == data.email.lower()
        )
    )

    if not user:

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    if not verify_password(
        data.password,
        user.password_hash
    ):

        raise HTTPException(
            status_code=401,
            detail="Invalid email or password."
        )

    token = create_access_token(
        user.id
    )

    response.set_cookie(
        COOKIE_NAME,
        token,
        httponly=True,
        samesite="lax",
        secure=False,
        max_age=60 * 60 * 24
    )

    return {
        "message": "Login successful.",
        "user": {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email
        }
    }


@router.post("/logout")
def logout(
    response: Response
):

    response.delete_cookie(
        COOKIE_NAME
    )

    return {
        "message": "Logged out."
    }


@router.get("/me")
def me(
    user: User = Depends(current_user)
):

    return {
        "id": user.id,
        "full_name": user.full_name,
        "email": user.email
    }