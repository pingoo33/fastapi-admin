from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Request, status, Cookie, HTTPException
from fastapi.responses import RedirectResponse
from fastapi_utils.cbv import cbv
from starlette.templating import Jinja2Templates

from app.config.auth import get_subject
from app.config.config import conf
from app.container import Container
from app.service.admin import AdminService

router = APIRouter()

templates = Jinja2Templates(directory=conf().BASE_DIR + '/app/templates')


@cbv(router)
class IndexController:
    @inject
    def __init__(self, admin_service: AdminService = Depends(Provide[Container.admin_service])):
        self.admin_service = admin_service

    @router.get('/')
    async def get_home(self,
                       request: Request,
                       access_token: str = Cookie(None),
                       refresh_token: str = Cookie(None)):
        try:
            await get_subject(access_token, refresh_token)
        except HTTPException:
            return RedirectResponse(url="/admin/sign-in", status_code=status.HTTP_303_SEE_OTHER)

        return templates.TemplateResponse('index.html',
                                          {'request': request})

    @router.get('/sign-in')
    async def get_sign_in_page(self, request: Request):
        return templates.TemplateResponse('admin_signin.html',
                                          {'request': request})
