from sqlalchemy import (
    Column,
    String,
    Integer,
    select,
    and_
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.conn import Base


class User(Base):
    __tablename__ = "tb_user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=50), nullable=False, unique=True)
    password = Column(String(length=100), nullable=False)
    role = Column(String(length=50), nullable=False)


class UserRepository:
    @staticmethod
    async def find_by_id(session: AsyncSession, user_id: int):
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalars().one_or_none()

    @staticmethod
    async def admin_sign_in(session: AsyncSession, email: str):
        result = await session.execute(select(User).where(and_(User.email == email, User.role == "admin")))
        return result.scalars().one_or_none()

    @staticmethod
    async def save(session: AsyncSession, entity: User):
        session.add(entity)
        await session.commit()
        await session.refresh(entity)
        return entity
