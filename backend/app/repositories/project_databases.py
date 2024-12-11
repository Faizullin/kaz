from sqlmodel import Session, select

from .base import BaseRepository
from ..database.models import ProjectDatabase


class ProjectDatabasesRepository(BaseRepository[ProjectDatabase]):
    def __init__(self):
        super().__init__(ProjectDatabase)

    def list(self, db: Session, project_id: int):
        statement = select(self.model).where(ProjectDatabase.project_id == project_id)
        return db.exec(statement)


project_databases_repository = ProjectDatabasesRepository()
