import os


os.environ["DATABASE_URL"] = (
    "sqlite:///./test_pocketsmart.db"
)

os.environ["SECRET_KEY"] = (
    "test-secret-key"
)


from fastapi.testclient import TestClient

from app.main import app

from app.database import Base
from app.database import engine


Base.metadata.drop_all(
    bind=engine
)

Base.metadata.create_all(
    bind=engine
)


client = TestClient(
    app
)


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"



def test_register():

    response = client.post(

        "/api/auth/register",

        json={

            "full_name":
                "Test User",

            "email":
                "testuser@example.com",

            "password":
                "secret123"

        }
    )


    assert response.status_code in (
        200,
        409
    )



def test_login_and_home_plan():

    response = client.post(

        "/api/auth/login",

        json={

            "email":
                "testuser@example.com",

            "password":
                "secret123"

        }
    )


    assert response.status_code == 200


    response = client.post(

        "/api/generate-home",

        json={

            "budget":
                20000,

            "rooms": [
                "Living Room"
            ],

            "items": {

                "Lights": 2,

                "Table": 1

            },

            "style":
                "Modern",

            "notes":
                "Keep it simple"

        }
    )


    assert response.status_code == 200


    data =
        response.json()


    assert data[
        "planner_type"
    ] == "home"


    assert data[
        "budget"
    ] == 20000



def test_party_requires_login():

    client.post(
        "/api/auth/logout"
    )


    response = client.post(

        "/api/generate-party",

        json={

            "budget":
                10000,

            "guests":
                20,

            "event_type":
                "Birthday",

            "venue":
                "Home",

            "city":
                "Chennai",

            "preferences":
                ""

        }
    )


    assert response.status_code == 401