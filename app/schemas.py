from pydantic import BaseModel
from pydantic import EmailStr
from pydantic import Field


class RegisterRequest(BaseModel):

    full_name: str = Field(
        min_length=2,
        max_length=120
    )

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=128
    )


class LoginRequest(BaseModel):

    email: EmailStr

    password: str = Field(
        min_length=6,
        max_length=128
    )


class HomeRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    rooms: list[str] = Field(
        min_length=1
    )

    items: dict[str, int] = Field(
        default_factory=dict
    )

    style: str = Field(
        default="modern",
        max_length=100
    )

    notes: str = Field(
        default="",
        max_length=1000
    )


class PartyRequest(BaseModel):

    budget: float = Field(
        gt=0,
        le=10_000_000
    )

    guests: int = Field(
        gt=0,
        le=10_000
    )

    event_type: str = Field(
        min_length=2,
        max_length=100
    )

    venue: str = Field(
        default="Home",
        max_length=200
    )

    city: str = Field(
        default="",
        max_length=100
    )

    preferences: str = Field(
        default="",
        max_length=1000
    )


class RecommendationItem(BaseModel):

    name: str

    category: str

    platform: str

    estimated_price: float

    quantity: int = 1

    reason: str

    link: str = ""


class RecommendationResponse(BaseModel):

    planner_type: str

    title: str

    budget: float

    estimated_total: float

    budget_remaining: float

    summary: str

    allocations: dict[str, float]

    recommendations: list[RecommendationItem]

    tips: list[str]

    source_mode: str