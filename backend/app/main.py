from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import api_router
from app.core.config import settings
from app.core.database import engine, Base

# Import models to register them with Base.metadata
from app.models import *  # noqa: F401, F403

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="ShortPlay API",
    description="AI 短剧生成平台 API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# API Router (no prefix - nginx handles /api routing)
app.include_router(api_router)


@app.get("/health")
def health_check():
    return {"status": "healthy"}


@app.get("/")
def root():
    return {"message": "ShortPlay API", "version": "1.0.0"}
