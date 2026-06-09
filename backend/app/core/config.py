from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Digital Twin Türkiye"

    DEFAULT_GDP: float = 21000
    DEFAULT_INFLATION: float = 52.0
    DEFAULT_INTEREST_RATE: float = 42.5
    DEFAULT_UNEMPLOYMENT: float = 8.8
    DEFAULT_USDTRY: float = 38.0

    class Config:
        env_file = ".env"


settings = Settings()