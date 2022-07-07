import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    secret_key: str = os.environ.get('SECRET_KEY', '79c3d4450c7d3038d64d00c337e4f2539471750a9ba314bad00d95c9291dfed8')
    access_token_expires_in_minutes: int = os.environ.get('ACCESS_TOKEN_EXPIRES_IN_MINUTES', 180)

    swagger_user: str = os.environ.get('SWAGGER_USER', 'admin')
    swagger_password: str = os.environ.get('SWAGGER_PASS', '12345')

    db_user: str = os.environ.get('DB_USER', 'admin')
    db_password: str = os.environ.get('DB_PASS', '12345678')
    db_name: str = os.environ.get('DB_NAME', 'joom_calendar')
    db_host: str = os.environ.get('DB_HOST', 'db')
    db_port: str = os.environ.get('DB_PORT', 5432)

    class Config:
        env_file = "core/.env"


settings = Settings()
