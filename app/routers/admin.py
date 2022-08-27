from typing import Optional

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Cookie, Request, status
from fastapi_utils.cbv import cbv
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse, RedirectResponse
from starlette.templating import Jinja2Templates

from app.config.config import conf
from app.config.jwt import get_subject, delete_jwt
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
                       access_token: Optional[str] = Cookie(None),
                       refresh_token: Optional[str] = Cookie(None)):
        if access_token is not None and refresh_token is not None:
            try:
                get_subject(access_token, refresh_token)
            except Exception:
                response = RedirectResponse(url='/admin/', status_code=status.HTTP_303_SEE_OTHER)
                return delete_jwt(response)

            return templates.TemplateResponse('index.html',
                                              {'request': request})
        else:
            return templates.TemplateResponse('admin_signin.html',
                                              {'request': request})

    @router.post('/sign-in')
    async def sign_in(self,
                      req: AdminSignInRequestDto,
                      session: AsyncSession = Depends(db.get_db)):
        access_token, refresh_token = await self.admin_service.sign_in(session, req)

        response = JSONResponse(content={}, status_code=status.HTTP_200_OK)
        response.set_cookie(key='access_token', value=access_token)
        response.set_cookie(key='refresh_token', value=refresh_token)

        return response
