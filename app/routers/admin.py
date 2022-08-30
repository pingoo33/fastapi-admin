from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, status, Cookie, HTTPException
from fastapi.responses import RedirectResponse
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from starlette.templating import Jinja2Templates

from app.config.config import conf
from app.config.jwt import AdminJWTProvider, AuthenticationSubject, get_subject, add_jwt, delete_jwt
from app.container import Container, db
from app.service.admin import AdminService
from app.model.admin import AdminSignInRequestDto

router = APIRouter()

templates = Jinja2Templates(directory=conf().BASE_DIR + '/app/templates')


@cbv(router)
class AdminController:
    @inject
    def __init__(self, admin_service: AdminService = Depends(Provide[Container.admin_service])):
        self.admin_service = admin_service

    @router.get('/')
    async def get_home(self,
                       request: Request,
                       access_token: str = Cookie(None),
                       refresh_token: str = Cookie(None)):
        try:
            get_subject(access_token, refresh_token)
        except HTTPException:
            return RedirectResponse(url="/admin/sign-in", status_code=status.HTTP_303_SEE_OTHER)

        return templates.TemplateResponse('index.html',
                                          {'request': request})

    @router.get('/sign-in')
    async def get_sign_in_page(self, request: Request):
        return templates.TemplateResponse('admin_signin.html',
                                          {'request': request})

    @router.get('/me')
    async def retrieve_admin(self,
                             session: AsyncSession = Depends(db.get_db),
                             auth: AuthenticationSubject = Depends(AdminJWTProvider())):
        return await self.admin_service.retrieve_admin(session, auth.subject_id)

    @router.post('/sign-in')
    async def sign_in(self,
                      req: AdminSignInRequestDto,
                      session: AsyncSession = Depends(db.get_db)):
        access_token, refresh_token = await self.admin_service.sign_in(session, req)

        response = JSONResponse(content={}, status_code=status.HTTP_200_OK)
        response = add_jwt(response, access_token, refresh_token)

        return response

    @router.get('/sign-out')
    async def sign_out(self):
        response = RedirectResponse(url='/admin/sign-in', status_code=status.HTTP_303_SEE_OTHER)
        return delete_jwt(response)
