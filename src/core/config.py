import sys
from collections import defaultdict
from typing import Literal, Optional
from pydantic import AnyHttpUrl, EmailStr, Field, ValidationError, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  
    )

    NODE_ENV: Literal["development", "production", "test"] = "development"
    PORT: int = 8080

    DATABASE_URL: str

   
    JWT_SECRET: str = Field(min_length=16)
    JWT_EXPIRATION: str = "15m"
    JWT_SECRET_REFRESH: Optional[str] = Field(default=None, min_length=16)
    JWT_SECRET_REFRESH_EXPIRATION: str = "30d"

    @computed_field
    @property
    def is_dev(self) -> bool:
        return self.NODE_ENV == "development"


def validate_env() -> Settings:
    try:
        return Settings()
    except ValidationError as err:
        sys.stderr.write("❌ Variáveis de ambiente inválidas:\n\n")
        errors_by_field: dict[str, list[str]] = defaultdict(list)
        for error in err.errors():
            field_name = ".".join(str(loc) for loc in error["loc"])
            errors_by_field[field_name].append(error["msg"])

        for field, messages in errors_by_field.items():
            sys.stderr.write(f"  {field}:\n")
            for msg in messages:
                sys.stderr.write(f"    - {msg}\n")

        sys.exit(1)

env = validate_env()