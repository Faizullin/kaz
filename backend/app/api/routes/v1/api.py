from fastapi import APIRouter

# from .endpoints.admin import router as admin_router
from .encpoints.auth import router as auth_router
# from .encpoints.chat import router as chat_router
from .encpoints.projects import router as projects_router
from .encpoints.project_databases import router as project_databases_router

api_router = APIRouter(
    prefix="/api/v1",
    tags=["api/v1"]
)
api_router.include_router(auth_router)
api_router.include_router(projects_router)
api_router.include_router(project_databases_router)
# api_router.include_router(chat_router)
