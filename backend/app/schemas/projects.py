from typing import List, Optional

from pydantic import BaseModel


class ProjectCreate(BaseModel):
    title: str


class ProjectInfo(BaseModel):
    id: int
    title: str

    class Config:
         pass


class ProjectUpdate(BaseModel):
    title: Optional[str] = None


class ProjectDatabaseCreate(BaseModel):
    title: str
    connection_user: str
    connection_password: str
    connection_url: str
    project_id: int


class ProjectDatabaseInfo(BaseModel):
    id: int
    title: str
    connection_user: str
    connection_password: str
    connection_url: str
    project_id: int
    owner_id: int

    class Config:
         pass


class ProjectDatabaseUpdate(BaseModel):
    title: Optional[str] = None
    connection_user: Optional[str] = None
    connection_password: Optional[str] = None
    connection_url: Optional[str] = None


class ProjectTableCreate(BaseModel):
    title: str
    project_database_id: int


class ProjectTableInfo(BaseModel):
    id: int
    title: str
    project_database_id: int

    class Config:
         pass


class ProjectTableUpdate(BaseModel):
    title: Optional[str] = None