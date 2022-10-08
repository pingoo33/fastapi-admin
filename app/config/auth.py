from dependency_injector.wiring import inject, Provide
from fastapi import Request, Cookie, Depends
from jose import jwt
from sqlalchemy.ext.asyncio import AsyncSession

from app.common.error.exception import UnauthorizedException, ErrorCode, NotFoundException
from app.config.consts import JWT_ALGORITHM, JWT_SECRET_KEY
from app.config.jwt import create_access_token, create_refresh_token
from app.container import Container, db
from app.schemas.user import UserRepository


class AuthenticationSubject:
    def __init__(self, subject, access_token, access_expire, refresh_token, refresh_expire):
        self.subject = subject
        self.access_token = access_token
        self.access_expire = access_expire
        self.refresh_token = refresh_token
        self.refresh_expire = refresh_expire


async def retrieve_user(session: AsyncSession, user_id, user_repository: UserRepository):
    user = await user_repository.find_by_id(session, user_id)

    if user is None:
        raise NotFoundException(code=ErrorCode.USER_NOT_FOUND, message="사용자를 찾을 수 없습니다.")

    return user


@inject
async def get_subject(session: AsyncSession, access_token: str, refresh_token: str,
                      user_repository: UserRepository = Depends(Provide[Container.user_repository])):
    if access_token is None or refresh_token is None:
        raise UnauthorizedException(code=ErrorCode.NOT_FOUND_TOKEN, message='다시 로그인 해주세요.')

    try:
        payload_access = jwt.decode(access_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        try:
            payload_refresh = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        except Exception:
            raise UnauthorizedException(code=ErrorCode.INVALID_TOKEN, message='다시 로그인 해주세요.')
        return AuthenticationSubject(await retrieve_user(session, payload_access['user_id'], user_repository),
                                     "", payload_access['exp'],
                                     "", payload_refresh['exp'])

    except jwt.ExpiredSignatureError:
        try:
            payload = jwt.decode(refresh_token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
            access_token, access_expire = create_access_token(payload['user_id'])
            refresh_token, refresh_expire = create_refresh_token(payload['user_id'])
            return AuthenticationSubject(await retrieve_user(session, payload['user_id'], user_repository),
                                         access_token, access_expire,
                                         refresh_token, refresh_expire)
        except Exception:
            raise UnauthorizedException(code=ErrorCode.INVALID_TOKEN, message='다시 로그인 해주세요.')
    except Exception:
        raise UnauthorizedException(code=ErrorCode.INVALID_TOKEN, message='다시 로그인 해주세요.')


class JWTProvider:
    async def __call__(self,
                       request: Request,
                       access_token: str = Cookie(None),
                       refresh_token: str = Cookie(None),
                       session: AsyncSession = Depends(db.get_db)):
        return await get_subject(session, access_token, refresh_token)
