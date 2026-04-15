"""
Personal Blog System - FastAPI Backend
Main application entry point
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.database import connect_to_database, close_database_connection
from app.middleware.error_handler import register_exception_handlers
from app.api.v1 import (
    auth,
    articles,
    categories,
    tags,
    skills,
    projects,
    likes,
    email,
    images,
    search,
    statistics
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    await connect_to_database()
    yield
    # Shutdown
    await close_database_connection()


app = FastAPI(
    title="Personal Blog API",
    description="A dual-board personal blog system with life and tech sections",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware - use configured origins
cors_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",") if origin.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register global exception handlers
register_exception_handlers(app)

# Register API routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(articles.router, prefix="/api/v1")
app.include_router(categories.router, prefix="/api/v1")
app.include_router(tags.router, prefix="/api/v1")
app.include_router(skills.router, prefix="/api/v1")
app.include_router(projects.router, prefix="/api/v1")
app.include_router(likes.router, prefix="/api/v1")
app.include_router(email.router, prefix="/api/v1")
app.include_router(images.router, prefix="/api/v1")
app.include_router(search.router, prefix="/api/v1")
app.include_router(statistics.router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint"""
    return {"message": "Personal Blog API", "version": "1.0.0"}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
    )
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
