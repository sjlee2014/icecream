from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.core.database import init_db
from backend.api import chat, faq

# Initialize FastAPI app
app = FastAPI(
    title="고객 상담 챗봇 API",
    description=f"{settings.BUSINESS_NAME} 고객 상담 챗봇 시스템",
    version="1.0.0",
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router)
app.include_router(faq.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": f"{settings.BUSINESS_NAME} 고객 상담 챗봇 API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
        "business_hours": settings.BUSINESS_HOURS,
        "contact": {
            "email": settings.SUPPORT_EMAIL,
            "phone": settings.SUPPORT_PHONE,
        }
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_RELOAD,
    )
