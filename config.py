from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    redis_host: str = "localhost"
    redis_port: int = 6379
    redis_password: str | None = None
    redis_db: int = 0

    worker_concurrency: int = 10
    request_timeout: int = 30

    model_config = {"env_file": ".env"}


settings = Settings()
