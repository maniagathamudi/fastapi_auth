from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # -------------------------
    # Email Configuration
    # -------------------------
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_FROM: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_STARTTLS: bool
    MAIL_SSL_TLS: bool

    # -------------------------
    # Auth0 Configuration
    # -------------------------
    AUTH0_DOMAIN: str
    AUTH0_CLIENT_ID: str
    AUTH0_CLIENT_SECRET: str
    AUTH0_CALLBACK_URL: str

    # -------------------------
    # API Token Verification
    # -------------------------
    AUTH0_AUDIENCE: str
    AUTH0_ALGORITHMS: str

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()