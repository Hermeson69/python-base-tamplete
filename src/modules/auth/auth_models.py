
from typing import Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core import BaseModel
from ...shared import generate_id


class AuthModel(BaseModel):
    __tablename__ = "users"

    public_id: Mapped[str] = mapped_column(
        String, unique=True, index=True, default=generate_id
    )
    email: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    profile: Mapped["ProfileModel"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined",
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, email={self.email})>"


class ProfileModel(BaseModel):
    __tablename__ = "profiles"

    user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"), unique=True
    )
    full_name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[Optional[str]] = mapped_column(String(20), default=None)
    avatar_image: Mapped[Optional[str]] = mapped_column(String(255), default=None)

    user: Mapped[AuthModel] = relationship(back_populates="profile", lazy="joined")