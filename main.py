import asyncio

import nest_asyncio
import uvicorn
from fastapi import FastAPI, HTTPException

from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from starlette.responses import JSONResponse

from app.config.consts import SESSION_SECRET_KEY
from app.container import Container, db
from app.routers import admin

nest_asyncio.apply()

""" Initialize Database """
asyncio.run(db.create_database())


def create_app() -> FastAPI:
    app = FastAPI()
    container = Container()

    """ Define Container """
    container.wire(modules=[admin])
    app.container = container

    """ Define Routers """
    app.include_router(admin.router, prefix="/admin")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET_KEY)
    return app


app = create_app()


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(content={"message": str(exc.detail)}, status_code=exc.status_code)


if __name__ == "__main__":
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True)
