from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.core.config import settings
from backend.core.database import init_db
from backend.api import products, scraper

# Initialize FastAPI app
app = FastAPI(
    title="Icecream Mall Scraper API",
    description="API for scraping and analyzing products from i-screammall.co.kr",
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
app.include_router(products.router)
app.include_router(scraper.router)


@app.on_event("startup")
async def startup_event():
    """Initialize database on startup."""
    init_db()


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "message": "Icecream Mall Scraper API",
        "version": "1.0.0",
        "docs": "/docs",
        "status": "running",
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
