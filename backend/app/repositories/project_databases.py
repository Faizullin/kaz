import os
from typing import List
from uuid import uuid4

from fastapi import HTTPException, UploadFile
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ..database.models import ProjectDatabase, ProjectTable
from ..schemas.projects import (ProjectDatabaseCreate, ProjectDatabaseUpdate,
                                ProjectTableCreate)


class ProjectDatabasesRepository:
    def generate_connection_url(self, user: str, password: str):
        return "posgresql:/{},{}".format(user, password)

    def create_project_database(self, db: Session, project_database_input: ProjectDatabaseCreate, user_id: int):
        new_obj = ProjectDatabase(
            title=project_database_input.title,
            owner_id=user_id,
            project_id=project_database_input.project_id,
            connection_user=project_database_input.connection_user,
            connection_password=project_database_input.connection_password,
            connection_url=self.generate_connection_url(
                project_database_input.connection_user, project_database_input.connection_password,
            )
        )
        db.add(new_obj)
        db.commit()
        db.refresh(new_obj)
        return new_obj

    def get_project_database_by_id(self, db: Session, project_database_id: int) -> ProjectDatabase:
        project_database = db.query(ProjectDatabase).filter(
            ProjectDatabase.id == project_database_id).first()
        if not project_database:
            raise HTTPException(
                status_code=404, detail="ProjectDatabase not found")
        return project_database

    def update_project_database(self, db: Session, project_database_id: int, project_database_data: ProjectDatabaseUpdate):
        project_database = db.query(ProjectDatabase).filter(
            ProjectDatabase.id == project_database_id).first()
        if not project_database:
            raise HTTPException(
                status_code=404, detail="ProjectDatabase not found")

        for field, value in project_database_data.model_dump(exclude_unset=True).items():
            setattr(project_database, field, value)

        try:
            db.commit()
            db.refresh(project_database)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Error updating project_database")
        return project_database

    def delete_project_database(self, db: Session, project_database_id: int):
        project_database = db.query(ProjectDatabase).filter(
            ProjectDatabase.id == project_database_id).first()
        if not project_database:
            raise HTTPException(
                status_code=404, detail="ProjectDatabase not found")
        db.delete(project_database)
        db.commit()
        return project_database

    def get_project_databases_by_farmer_id(self, db: Session, farmer_id: int):
        """Retrieve all project_databases associated with a specific farmer."""
        project_databases = db.query(ProjectDatabase).filter(
            ProjectDatabase.farmer_id == farmer_id).all()
        return project_databases

    def get_all_project_databases(self, db: Session):
        """Retrieve all project_databases."""
        return db.query(ProjectDatabase).all()

    def create_project_database_table(self, db: Session, project_table_input: ProjectTableCreate):
        new_obj = ProjectTable(
            title=project_table_input.title,
            project_database_id=project_table_input.project_database_id,
            migrated=False,
        )
        db.add(new_obj)
        db.commit()
        db.refresh(new_obj)
        return new_obj

    def delete_project_database_table(self, db: Session, project_table_id: int):
        obj = db.query(ProjectTable).filter(
            ProjectTable.id == project_table_id).first()
        if not obj:
            raise HTTPException(
                status_code=404, detail="ProjectTable not found")
        db.delete(obj)
        db.commit()
        return obj

    def migrate_project_database_table(self, db: Session, project_table_id: int):
        obj = db.query(ProjectTable).filter(
            ProjectTable.id == project_table_id).first()
        if not obj:
            raise HTTPException(
                status_code=404, detail="ProjectTable not found")
        if obj.migrated:
            raise HTTPException(
                status_code=403, detail="Already migrated")
        obj.migrated = True
        try:
            db.commit()
            db.refresh(obj)
        except IntegrityError:
            db.rollback()
            raise HTTPException(
                status_code=400, detail="Error updating ProjectTable")
        return obj
