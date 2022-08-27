from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config.jwt import create_jwt
from app.model.admin import AdminSignInRequestDto
from app.schemas.admin import AdminRepository


class AdminService:
    def __init__(self, admin_repository: AdminRepository):
        self.admin_repository = admin_repository

    async def sign_in(self, session: AsyncSession, req: AdminSignInRequestDto):
        admin = await self.admin_repository.sign_in(session, req.email)

        if admin.password != req.password:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="잘못된 비밀번호 입니다.")

        token = create_jwt(str(admin.id))

        return token["access_token"], token["refresh_token"]
