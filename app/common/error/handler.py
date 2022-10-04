from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from app.common.error.exception import BadRequestException, UnauthorizedException, NotFoundException


def add_http_exception_handler(app: FastAPI) -> None:
    @app.exception_handler(BadRequestException)
    async def bad_request_exception_handler(request: Request, exc: BadRequestException):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content={"code": exc.code.value, "message": exc.message})

    @app.exception_handler(UnauthorizedException)
    async def unauthorized_exception_handler(request: Request, exc: UnauthorizedException):
        return JSONResponse(status_code=status.HTTP_401_UNAUTHORIZED,
                            content={"code": exc.code.value, "message": exc.message})

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content={"code": exc.code.value, "message": exc.message})
