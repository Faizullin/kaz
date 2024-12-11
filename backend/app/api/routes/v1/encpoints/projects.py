from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import Project
from app.repositories.projects import projects_repository
from app.schemas.projects import ProjectInfo, ProjectCreate

router = APIRouter()


@router.post("/projects/new", response_model=ProjectInfo, status_code=201)
def create_project(input_data: ProjectCreate, db: Session = Depends(get_db)):
    """
    Create a new project
    """
    new_obj = Project(
        title=input_data.title,
        owner_id=1,
    )
    return projects_repository.create(db, new_obj)


@router.get("/projects/my/", response_model=List[ProjectInfo], name="projects my")
def get_all_projects(db: Session = Depends(get_db)):
    """
    Get my projects.
    """
    projects = projects_repository.list(db)
    return projects
