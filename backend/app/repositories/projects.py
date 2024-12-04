from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..database.models import Project, ProjectDatabase, ProjectTable
from ..schemas.projects import ProjectCreate, ProjectUpdate


class ProjectsRepository:
    def create_project(self, db: Session, project_input: ProjectCreate, user_id: int):
        new_pobj = Project(
            title=project_input.title,
            owner_id=user_id,
        )
        db.add(new_pobj)
        db.commit()
        db.refresh(new_pobj)
        return new_pobj

    def get_project_by_id(self, db: Session, project_id: int) -> Project:
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        return project

    def update_project(self, db: Session, project_id: int, project_data: ProjectUpdate):
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")

        for field, value in project_data.model_dump(exclude_unset=True).items():
            setattr(project, field, value)

        try:
            db.commit()
            db.refresh(project)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Error updating project")
        return project

    def delete_project(self, db: Session, project_id: int):
        project = db.query(Project).filter(Project.id == project_id).first()
        if not project:
            raise HTTPException(status_code=404, detail="Project not found")
        db.delete(project)
        db.commit()
        return project

    def get_projects_by_farmer_id(self, db: Session, farmer_id: int):
        """Retrieve all projects associated with a specific farmer."""
        projects = db.query(Project).filter(
            Project.farmer_id == farmer_id).all()
        return projects

    def get_all_projects(self, db: Session):
        """Retrieve all projects."""
        return db.query(Project).all()
