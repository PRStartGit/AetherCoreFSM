from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base

# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_PREFIX}/openapi.json"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200", "http://localhost:8000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

# Create database tables
Base.metadata.create_all(bind=engine)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Welcome to Zynthio API",
        "version": settings.VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


# Import and include routers
from app.api.v1 import auth, organizations, sites, users, categories, tasks, task_fields, checklists, defects, dashboards

app.include_router(auth.router, prefix=settings.API_V1_PREFIX, tags=["Authentication"])
app.include_router(organizations.router, prefix=settings.API_V1_PREFIX, tags=["Organizations"])
app.include_router(sites.router, prefix=settings.API_V1_PREFIX, tags=["Sites"])
app.include_router(users.router, prefix=settings.API_V1_PREFIX, tags=["Users"])
app.include_router(categories.router, prefix=settings.API_V1_PREFIX, tags=["Categories"])
app.include_router(tasks.router, prefix=settings.API_V1_PREFIX, tags=["Tasks"])
app.include_router(task_fields.router, prefix=settings.API_V1_PREFIX, tags=["Task Fields"])
app.include_router(checklists.router, prefix=settings.API_V1_PREFIX, tags=["Checklists"])
app.include_router(defects.router, prefix=settings.API_V1_PREFIX, tags=["Defects"])
app.include_router(dashboards.router, prefix=settings.API_V1_PREFIX, tags=["Dashboards"])
