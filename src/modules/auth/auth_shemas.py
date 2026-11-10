import re
from datetime import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    field_validator,
    model_validator,
)


def validate_password_strength(v: str) -> str:
    if not re.search(r"[A-Z]", v):
        raise ValueError("A senha deve ter ao menos uma letra maiúscula.")
    if not re.search(r"[0-9]", v):
        raise ValueError("A senha deve ter ao menos um número.")
    return v


class RegisterClientSchema(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    password: str = Field(min_length=6)
    phone: str | None = Field(default=None, min_length=1)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password_strength(v)


class LoginClientSchema(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


class SendPasswordResetSchema(BaseModel):
    email: EmailStr = Field(min_length=6)


class CheckPasswordResetSchema(BaseModel):
    user_token_id: str = Field(min_length=1)
    code: str = Field(min_length=1)


class ResetPasswordSchema(BaseModel):
    reset_token: str = Field(min_length=1)
    new_password: str = Field(min_length=6)
    confirm_new_password: str = Field(min_length=6)

    @field_validator("new_password", "confirm_new_password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        return validate_password_strength(v)

    @model_validator(mode="after")
    def passwords_match(self):
        if self.new_password != self.confirm_new_password:
            raise ValueError("As senhas não conferem.")
        return self


class RefreshTokenSchema(BaseModel):
    refresh_token: str = Field(min_length=1)


class LogoutSchema(BaseModel):
    refresh_token: str = Field(min_length=1)
    logout_all_devices: bool = False



class ORMModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ProfileResponseSchema(ORMModel):
    full_name: str
    phone: str | None
    avatar_image: str | None
    created_at: datetime


class RegisterResponseSchema(ORMModel):
    public_id: str
    email: EmailStr
    created_at: datetime
    updated_at: datetime
    profile: ProfileResponseSchema


class LoginUserSchema(ORMModel):
    public_id: str
    email: EmailStr
    profile: ProfileResponseSchema


class LoginResponseSchema(ORMModel):
    access_token: str
    refresh_token: str
    user: LoginUserSchema


class RefreshTokenResponseSchema(ORMModel):
    access_token: str
    refresh_token: str


class LogoutResponseSchema(ORMModel):
    success: bool


class SendPasswordResetResponseSchema(ORMModel):
    email: EmailStr
    user_token_id: str | None
    expires_at: datetime


class CheckPasswordResetResponseSchema(ORMModel):
    reset_token: str


class ResetPasswordUserSchema(ORMModel):
    public_id: str
    email: EmailStr
    profile: ProfileResponseSchema


class ResetPasswordResponseSchema(ORMModel):
    access_token: str
    refresh_token: str
    user: ResetPasswordUserSchema