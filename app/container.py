from dataclasses import asdict

from dependency_injector import containers, providers

from app.config.config import conf
from app.schemas.admin import AdminRepository
from app.schemas.conn import Database
from app.service.admin import AdminService

db = Database(db_url=asdict(conf())['DB_URL'])


class Container(containers.DeclarativeContainer):
    """ Repository """
    admin_repository = providers.Factory(AdminRepository)

    """ Service """
    admin_service = providers.Factory(AdminService,
                                      admin_repository=admin_repository)
