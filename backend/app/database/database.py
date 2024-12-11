from typing import Generator, Annotated

from fastapi import Depends
from sqlmodel import create_engine, Session

from app.core.config import settings

engine = create_engine(str(settings.POSTGRESQL_DATABASE_URI))


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
