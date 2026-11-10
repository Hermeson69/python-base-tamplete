from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.engine import make_url

from ..core import BaseModel
from ..core.config import env

database_url = make_url(env.DATABASE_URL)
if database_url.drivername == "postgresql":
    database_url = database_url.set(drivername="postgresql+asyncpg")

connect_args = {}
if database_url.port == 6543 and "ssl" not in database_url.query:
    connect_args["ssl"] = "require"

async_engine = create_async_engine(
    database_url,
    echo=True,
    connect_args=connect_args,
)
async_sessionmaker = async_sessionmaker(async_engine, expire_on_commit=False)


async def get_async_session() -> AsyncGenerator[AsyncSession, Any]:
    """Get an async database session"""
    async with async_sessionmaker() as session:
        yield session


async def init_db() -> None:
    """Initialize the database with all tables"""
    from ..modules.auth import AuthModel, ProfileModel  

    async with async_engine.begin() as conn:
        print("Creating database tables...")
        await conn.run_sync(BaseModel.metadata.create_all)
        print("Database tables created successfully!")