from pathlib import Path

from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware

from fastapi.staticfiles import StaticFiles

from .config import get_settings
from .database import init_db

from .routers import auth
from .routers import pages
from .routers import planners


settings = get_settings()


app = FastAPI(

    title=settings.app_name,

    version="1.0.0",

    description=
        "PocketSmart AI budget-aware lifestyle recommendation assistant."
)


app.add_middleware(

    CORSMiddleware,

    allow_origins=[
        "http://127.0.0.1:8000",
        "http://localhost:8000"
    ],

    allow_credentials=True,

    allow_methods=["*"],

    allow_headers=["*"]
)


app.mount(

    "/static",

    StaticFiles(
        directory=Path(
            "app/static"
        )
    ),

    name="static"
)


app.include_router(
    pages.router
)

app.include_router(
    auth.router
)

app.include_router(
    planners.router
)


@app.on_event("startup")
def startup():

    init_db()


@app.get(
    "/health",
    tags=["System"]
)
def health():

    return {

        "status": "ok",

        "service":
            settings.app_name,

        "gemini_configured":
            bool(
                settings.gemini_api_key
            )
    }