from typing import List, Optional
from pydantic import BaseModel
from app.database.models import ProjectTable


class ExecutionResponseOutput(BaseModel):
    code: Optional[int]
    callback: str
    args: List[str]
    message: str


class ExecutionResponse(BaseModel):
    input: str
    output: Optional[ExecutionResponseOutput]
    error: str
    success: bool
    error_msg: Optional[str]


def create_table_and_migrate(project_table: ProjectTable):
    print("created")


def process_query(message: str, project_table: ProjectTable) -> ExecutionResponse:
    try:
        return ExecutionResponse(
            input = message,
            output=None,
            error=False,
            success=True,
        )
    except Exception as err:
        return ExecutionResponse(
            input = "",
            output=None,
            error=True,
            success=False,
            error=str(err),
        )
