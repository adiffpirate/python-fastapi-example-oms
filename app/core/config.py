import os


class Settings:
    app_name: str = "OMS API"
    debug: bool = True

    def __init__(self) -> None:
        self.auth_jwt_secret_key = self._load_auth_jwt_secret_key()

    @staticmethod
    def _load_auth_jwt_secret_key() -> str:
        key = os.environ.get("AUTH_JWT_SECRET_KEY")
        if not key:
            raise ValueError(
                "AUTH_JWT_SECRET_KEY environment variable is required and must not be empty"
            )
        return key


settings = Settings()
