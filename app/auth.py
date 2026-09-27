from datetime import datetime
from datetime import timedelta
from datetime import timezone

from fastapi import Depends
from fastapi import HTTPException
from fastapi import Request
from fastapi import status

from jose import JWTError
from jose import jwt

from sqlalchemy.orm import Session

from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash

from .config import get_settings
from .database import get_db
from .models import User


settings = get_settings()

ALGORITHM = "HS256"

COOKIE_NAME = "access_token"


def hash_password(password: str) -> str:

    return generate_password_hash(
        password
    )


def verify_password(
    password: str,
    password_hash: str
) -> bool:

    return check_password_hash(
        password_hash,
        password
    )


def create_access_token(
    user_id: int
) -> str:

    expire = (
        datetime.now(timezone.utc)
        + timedelta(
            minutes=settings.access_token_expire_minutes
        )
    )

    payload = {
        "sub": str(user_id),
        "exp": expire
    }

    return jwt.encode(
        payload,
        settings.secret_key,
        algorithm=ALGORITHM
    )


def get_user_from_request(
    request: Request,
    db: Session
):

    token = request.cookies.get(
        COOKIE_NAME
    )

    if not token:

        authorization = request.headers.get(
            "Authorization",
            ""
        )

        if authorization.startswith("Bearer "):

            token = authorization[7:]

    if not token:

        return None

    try:

        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[ALGORITHM]
        )

        user_id = int(
            payload["sub"]
        )

    except (
        JWTError,
        KeyError,
        ValueError
    ):

        return None

    return db.get(
        User,
        user_id
    )


def current_user(
    request: Request,
    db: Session = Depends(get_db)
):

    user = get_user_from_request(
        request,
        db
    )

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication required"
        )

    return user