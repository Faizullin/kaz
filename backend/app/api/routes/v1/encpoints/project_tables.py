from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.repositories.projects import projects_repository
from app.schemas.projects import ProjectInfo, ProjectCreate

router = APIRouter()


@router.post("/projects/{project_id}", response_model=ProjectInfo, status_code=201)
def create_project_table(project_id: int, input_data: ProjectCreate, db: Session = Depends(get_db)):
    project_obj = projects_repository.get(db, project_id)

    return projects_repository.create(db, new_obj)


@router.get("/projects/{project_id}/databases", response_model=List[ProjectInfo], name="projects my")
def get_all_project_table_tables(project_id: int, db: Session = Depends(get_db)):
    project_obj = projects_repository.get(db, project_id)
    if project_obj is None:
        raise HTTPException(status_code=404, detail="Project not found")

    return projects
