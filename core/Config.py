from pydantic import BaseSettings

class Settings(BaseSettings):
    SECRET_KEY: str = "change-me-to-a-strong-one"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60*24
    DATABASE_URL: str = "sqlite:///./ultra_email.db"
    CREDENTIALS_FILE: str = "credentials.json"
    OAUTH_REDIRECT_URI: str = "http://localhost:8000/gmail/callback"

settings = Settings()
