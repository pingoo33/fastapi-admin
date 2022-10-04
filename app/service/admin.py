from sqlalchemy.ext.asyncio import AsyncSession

from app.common.error.exception import UnauthorizedException, ErrorCode, NotFoundException
from app.config.jwt import create_jwt
from app.model.admin import AdminSignInRequestDto, AdminResponseDto
from app.schemas.user import UserRepository, User


class AdminService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def sign_in(self, session: AsyncSession, req: AdminSignInRequestDto):
        admin = await self.user_repository.admin_sign_in(session, req.email)

        if admin is None:
            raise NotFoundException(code=ErrorCode.USER_NOT_FOUND, message="관리자를 찾을 수 없습니다.")

        if admin.password != req.password:
            raise UnauthorizedException(code=ErrorCode.INVALID_PASSWORD, message="잘못된 비밀번호 입니다.")

        token = create_jwt(admin.id)

        return token["access_token"], token["refresh_token"]

    async def retrieve_admin(self, user: User):
        return AdminResponseDto(
            email=user.email
        )
