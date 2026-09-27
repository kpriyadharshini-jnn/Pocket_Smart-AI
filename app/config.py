import os
from functools import lru_cache


def _load_dotenv(path: str = ".env") -> None:
    """Load simple KEY=VALUE entries when pydantic-settings is unavailable."""
    if not os.path.isfile(path):
        return

    with open(path, encoding="utf-8") as env_file:
        for line in env_file:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip("'\""))


class Settings:

    def __init__(self) -> None:
        _load_dotenv()
        self.app_name = os.getenv("APP_NAME", "PocketSmart AI")
        self.secret_key = os.getenv("SECRET_KEY", "change-me")
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///./pocketsmart.db")
        self.gemini_api_key = os.getenv("GEMINI_API_KEY")
        self.gemini_model = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
        self.access_token_expire_minutes = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")
        )
        self.max_image_bytes = int(
            os.getenv("MAX_IMAGE_BYTES", str(5 * 1024 * 1024))
        )


@lru_cache
def get_settings() -> Settings:

    return Settings()