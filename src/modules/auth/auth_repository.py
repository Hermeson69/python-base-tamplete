from sqlalchemy.ext.asyncio import AsyncSession

from .auth_models import ProfileModel, UserModel
from .auth_shemas import RegisterClientSchema


class AuthRepository:
    @staticmethod
    async def create_user(
        session: AsyncSession,
        user_data: RegisterClientSchema,
        password_hash: str,
    ) -> UserModel:
        new_user = UserModel(
            email=user_data.email,
            password_hash=password_hash,
            profile=ProfileModel(
                full_name=user_data.name,
                phone=user_data.phone,
            ),
        )
        session.add(new_user)
        await session.commit()
        await session.refresh(new_user)
        return new_user