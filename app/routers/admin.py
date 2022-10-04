from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, status
from fastapi.responses import RedirectResponse
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse

from app.config.auth import AuthenticationSubject, JWTProvider
from app.config.jwt import add_jwt, delete_jwt
from app.container import Container, db
from app.service.admin import AdminService
from app.model.admin import AdminSignInRequestDto

router = APIRouter()


@cbv(router)
class AdminController:
    @inject
    def __init__(self, admin_service: AdminService = Depends(Provide[Container.admin_service])):
        self.admin_service = admin_service

    @router.get('/me')
    async def retrieve_admin(self,
                             auth: AuthenticationSubject = Depends(JWTProvider())):
        return await self.admin_service.retrieve_admin(auth.subject)

    @router.post('/sign-in')
    async def sign_in(self,
                      req: AdminSignInRequestDto,
                      session: AsyncSession = Depends(db.get_db)):
        access_token, refresh_token = await self.admin_service.sign_in(session, req)

        response = JSONResponse(content={}, status_code=status.HTTP_200_OK)
        response = add_jwt(response, access_token, refresh_token)

        return response

    @router.get('/sign-out')
    async def sign_out(self,
                       auth: AuthenticationSubject = Depends(JWTProvider())):
        response = RedirectResponse(url='/admin/sign-in', status_code=status.HTTP_303_SEE_OTHER)
        return delete_jwt(response)
