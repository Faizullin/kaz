from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.database import get_db
from app.database.models import ProjectDatabase
from app.repositories.project_databases import project_databases_repository
from app.repositories.projects import projects_repository
from app.schemas.projects import ProjectDatabaseCreate, ProjectDatabaseInfo

router = APIRouter()


def get_project(project_id: int, db: Session = Depends(get_db)):
    project_obj = projects_repository.get(db, project_id)
    if not project_obj:
        raise HTTPException(status_code=404, detail="Project not found")
    return project_obj


@router.post("/projects/{project_id}/databases/new", response_model=ProjectDatabaseInfo, status_code=201)
def create_project_database(input_data: ProjectDatabaseCreate, db: Session = Depends(get_db),
                            project_obj=Depends(get_project)):
    """
    Create a new project database
    """
    connection_user = input_data.connection_user
    connection_password = input_data.connection_password
    connection_url = "{}:{}".format(connection_user, connection_password)
    new_obj = ProjectDatabase(
        title=input_data.title,
        owner_id=1,
        project_id=project_obj.id,
        connection_user=connection_user,
        connection_password=connection_password,
        connection_url=connection_url,
    )
    return project_databases_repository.create(db, new_obj)


@router.get("/projects/{project_id}/databases", response_model=List[ProjectDatabaseInfo], name="project databases")
def get_all_project_databases(db: Session = Depends(get_db), project_obj=Depends(get_project)):
    """
    Get all project databases
    """
    return project_databases_repository.list(db, project_id=project_obj.id)


@router.get("/projects/{project_id}/databases/{project_database_id}", response_model=ProjectDatabaseInfo, name="project database")
def get_project_database(project_database_id:int, db: Session = Depends(get_db), project_obj=Depends(get_project)):
    """
    Get a project database
    """
    project_database_obj = project_databases_repository.get(db, project_database_id)
    if not project_database_obj:
        raise HTTPException(status_code=404, detail="Project database not found")
    return project_database_obj