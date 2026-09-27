from fastapi import APIRouter
from fastapi import Depends
from fastapi import Request

from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse

from fastapi.templating import Jinja2Templates

from ..auth import get_user_from_request
from ..database import get_db


router = APIRouter()

templates = Jinja2Templates(
    directory="app/templates"
)


def page_context(
    request,
    db
):

    return {
        "request": request,
        "user": get_user_from_request(
            request,
            db
        )
    }


@router.get(
    "/",
    response_class=HTMLResponse
)
def home(
    request: Request,
    db=Depends(get_db)
):

    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context=page_context(
        request,
        db
    )
)


@router.get(
    "/login",
    response_class=HTMLResponse
)
def login_page(
    request: Request,
    db=Depends(get_db)
):

    return templates.TemplateResponse(
    request=request,
    name="login.html",
    context=page_context(
        request,
        db
    )
)


@router.get(
    "/register",
    response_class=HTMLResponse
)
def register_page(
    request: Request,
    db=Depends(get_db)
):

    return templates.TemplateResponse(
    request=request,
    name="register.html",
    context=page_context(
        request,
        db
    )
)


@router.get(
    "/dashboard",
    response_class=HTMLResponse
)
def dashboard(
    request: Request,
    db=Depends(get_db)
):

   return templates.TemplateResponse(
    request=request,
    name="dashboard.html",
    context=page_context(
        request,
        db
    )
)


@router.get(
    "/planner/{planner_type}",
    response_class=HTMLResponse
)
def planner(
    request: Request,
    planner_type: str,
    db=Depends(get_db)
):

    if planner_type not in {
        "home",
        "party",
        "jewelry"
    }:

        return RedirectResponse("/")

    return templates.TemplateResponse(
    request=request,
    name=f"{planner_type}_planner.html",
    context=page_context(
        request,
        db
    )
)


@router.get(
    "/history",
    response_class=HTMLResponse
)
def history(
    request: Request,
    db=Depends(get_db)
):

    return templates.TemplateResponse(
    request=request,
    name="history.html",
    context=page_context(
        request,
        db
    )
)