from contextlib import asynccontextmanager

from fastapi import FastAPI, APIRouter, HTTPException
from fastapi.responses import JSONResponse
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.api import api_router
from app.core.config import settings
from app.core.logging import logger
from app.db.session import sessionmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions (if any)
    logger.info("Server started!")
    yield
    # Shutdown actions
    logger.info("Server shutdown!")

    if sessionmanager._engine is not None:
        # Close the DB connection
        await sessionmanager.close()

app = FastAPI(
    title=settings.PROJECT_NAME, 
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    # Handle general exceptions
    return JSONResponse(
        status_code=500,
        content={"message": "An internal error occurred. Please try again later."},
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    # Handle HTTP-specific exceptions
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.detail},
    )

health_router = APIRouter()

@health_router.get("/health")
async def health_check():
    """
    Health check endpoint.
    Returns a JSON response indicating the service status.
    """
    return {"status": "ok"}

app.include_router(health_router)
app.include_router(api_router, prefix=settings.API_V1_STR)
