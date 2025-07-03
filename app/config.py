"""Configuration du projet FastAPI + MongoDB + JWT + RabbitMQ pour l'API Products."""
from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    """
    Paramètres de configuration chargés automatiquement via un fichier .env.
    
    Permet de centraliser et de sécuriser toutes les variables sensibles
    et spécifiques à l'environnement (dev, prod, etc.).
    """

    APP_NAME: str
    MONGO_URI: str
    DATABASE_NAME: str = "products_db"
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    RABBITMQ_URL: str = "amqp://guest:guest@localhost/"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    class Config:
        """Indique le chemin du fichier .env pour charger les variables d'environnement."""
        env_file = ".env"

# Instance globale des paramètres, accessible dans tout le projet
settings = Settings()
