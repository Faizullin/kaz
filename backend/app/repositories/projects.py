from .base import BaseRepository
from ..database.models import Project


class ProjectsRepository(BaseRepository[Project]):
    def __init__(self):
        super().__init__(Project)


projects_repository = ProjectsRepository()
