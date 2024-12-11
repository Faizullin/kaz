from typing import Annotated

from fastapi import Depends
from sqlmodel import Session

from app.database.database import get_db


# TokenDep = Annotated[str, Depends(reusable_oauth2)]
