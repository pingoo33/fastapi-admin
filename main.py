import asyncio

import nest_asyncio
import uvicorn
from fastapi import FastAPI

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.common.error.handler import add_http_exception_handler
from app.config import auth
from app.config.consts import SESSION_SECRET_KEY
from app.container import Container, db
from app.routers import admin, index

nest_asyncio.apply()

""" Initialize Database """
asyncio.run(db.create_database())


def create_app() -> FastAPI:
    app = FastAPI()
    container = Container()

    """ Define Container """
    container.wire(modules=[auth, index, admin])
    app.container = container

    """ Define Routers """
    app.include_router(index.router)

    app.include_router(admin.router, prefix="/admin")

    """ Define middlewares """
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )
    app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)

    """ Define exception handler """
    add_http_exception_handler(app)

    return app


app = create_app()


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
