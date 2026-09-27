import json

from fastapi import APIRouter
from fastapi import Depends
from fastapi import File
from fastapi import Form
from fastapi import HTTPException
from fastapi import UploadFile

from sqlalchemy.orm import Session

from ..auth import current_user
from ..config import get_settings
from ..database import get_db
from ..models import Recommendation
from ..models import User

from ..schemas import HomeRequest
from ..schemas import PartyRequest
from ..schemas import RecommendationResponse

from ..services.recommendation_service import create_plan


router = APIRouter(
    prefix="/api",
    tags=["Planners"]
)


def save_history(
    db: Session,
    user: User,
    planner_type: str,
    request_data: dict,
    result: dict
):

    record = Recommendation(
        user_id=user.id,
        planner_type=planner_type,
        request_json=json.dumps(
            request_data,
            ensure_ascii=False
        ),
        response_json=json.dumps(
            result,
            ensure_ascii=False
        )
    )

    db.add(record)

    db.commit()


@router.post(
    "/generate-home",
    response_model=RecommendationResponse
)
def generate_home(
    data: HomeRequest,
    user: User = Depends(current_user),
    db: Session = Depends(get_db)
):

    payload = data.model_dump()

    result = create_plan(
        "home",
        payload
    )

    save_history(
        db,
        user,
        "home",
        payload,
        result
    )

    return result


@router.post(
    "/generate-party",
    response_model=RecommendationResponse
)
def generate_party(
    data: PartyRequest,
    user: User = Depends(current_user),
    db: Session = Depends(get_db)
):

    payload = data.model_dump()

    result = create_plan(
        "party",
        payload
    )

    save_history(
        db,
        user,
        "party",
        payload,
        result
    )

    return result


@router.post(
    "/generate-jewelry",
    response_model=RecommendationResponse
)
async def generate_jewelry(
    budget: float = Form(...),
    occasion: str = Form(...),
    style: str = Form("minimal"),
    notes: str = Form(""),
    outfit_image: UploadFile | None = File(
        default=None
    ),
    user: User = Depends(current_user),
    db: Session = Depends(get_db)
):

    if budget <= 0:

        raise HTTPException(
            status_code=422,
            detail="Budget must be greater than zero."
        )

    image_bytes = None
    image_mime = None

    if outfit_image:

        allowed_types = {
            "image/jpeg",
            "image/png",
            "image/webp"
        }

        if outfit_image.content_type not in allowed_types:

            raise HTTPException(
                status_code=415,
                detail="Only JPG, PNG or WebP images are supported."
            )

        image_bytes = await outfit_image.read()

        settings = get_settings()

        if len(image_bytes) > settings.max_image_bytes:

            raise HTTPException(
                status_code=413,
                detail="Image is too large."
            )

        image_mime = outfit_image.content_type

    payload = {
        "budget": budget,
        "occasion": occasion,
        "style": style,
        "notes": notes
    }

    result = create_plan(
        "jewelry",
        payload,
        image_bytes=image_bytes,
        image_mime=image_mime
    )

    save_history(
        db,
        user,
        "jewelry",
        payload,
        result
    )

    return result


@router.get("/history")
def history(
    user: User = Depends(current_user),
    db: Session = Depends(get_db)
):

    records = (
        db.query(Recommendation)
        .filter(
            Recommendation.user_id == user.id
        )
        .order_by(
            Recommendation.created_at.desc()
        )
        .limit(50)
        .all()
    )

    return [
        {
            "id": record.id,
            "planner_type": record.planner_type,
            "created_at": record.created_at.isoformat(),
            "request": json.loads(
                record.request_json
            ),
            "response": json.loads(
                record.response_json
            )
        }
        for record in records
    ]