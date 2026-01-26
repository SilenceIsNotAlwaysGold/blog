"""
Personal Blog System - FastAPI Backend
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.database import connect_to_database, close_database_connection
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

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
