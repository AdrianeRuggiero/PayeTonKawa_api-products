"""Configuration du projet FastAPI + MongoDB + JWT + RabbitMQ pour l'API Products."""
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Paramètres de configuration chargés automatiquement via un fichier .env.
    """
    APP_NAME: str
    MONGO_URI: str
    DATABASE_NAME: str = "products_db"
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60

    # Pour Pydantic v2, indique le chemin relatif du .env par rapport à app/
    model_config = SettingsConfigDict(env_file=Path(__file__).parent.parent / ".env")

settings = Settings()
