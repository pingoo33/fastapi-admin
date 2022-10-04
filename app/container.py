from dataclasses import asdict

from dependency_injector import containers, providers

from app.config.config import conf
from app.schemas.user import UserRepository
from app.schemas.conn import Database
from app.service.admin import AdminService

db = Database(db_url=asdict(conf())['DB_URL'])


class Container(containers.DeclarativeContainer):
    """ Repository """
    user_repository = providers.Factory(UserRepository)

    """ Service """
    admin_service = providers.Factory(AdminService,
                                      user_repository=user_repository)
