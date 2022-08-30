from sqlalchemy import (
    Column,
    String,
    Integer,
    select
)
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.conn import Base


class Admin(Base):
    __tablename__ = "tb_admin"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(length=50), nullable=False, unique=True)
    password = Column(String(length=100), nullable=False)


class AdminRepository:
    @staticmethod
    async def find_by_id(session: AsyncSession, admin_id: int):
        result = await session.execute(select(Admin).where(Admin.id == admin_id))
        return result.scalars().one_or_none()

    @staticmethod
    async def sign_in(session: AsyncSession, email: str):
        result = await session.execute(select(Admin).where(Admin.email == email))
        return result.scalars().one_or_none()

    @staticmethod
    async def save(session: AsyncSession, entity: Admin):
        session.add(entity)
        await session.commit()
        await session.refresh(entity)
        return entity
