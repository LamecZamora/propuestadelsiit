from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql://siit:siit@localhost:5432/siit"
    JWT_SECRET_KEY: str = "changeme-generate-a-real-secret"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    CURRENT_PERIODO: str = "Enero – Junio 2026"
    CORS_ORIGINS: list[str] = ["http://localhost:5173"]


settings = Settings()
