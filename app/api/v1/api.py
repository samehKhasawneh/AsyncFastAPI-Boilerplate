from fastapi import APIRouter
from app.api.v1.endpoints import auth_router, users_router

api_router = APIRouter()

# Include other routers with prefixes
api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(users_router, prefix="/users", tags=["users"])
