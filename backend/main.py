import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from backend.database import init_db
from backend.seed_data import seed_database
from backend.routers import students, drives, diagnostics, github_validator

app = FastAPI(
    title="CampusPulse AI",
    description="Intelligent Campus Placement & Career Management Ecosystem",
    version="1.0.0"
)

# Enable CORS for frontend client
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API Routers
app.include_router(students.router)
app.include_router(drives.router)
app.include_router(diagnostics.router)
app.include_router(github_validator.router)

# Mount frontend static files if directory exists
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.on_event("startup")
def startup_event():
    init_db()
    seed_database()


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": "CampusPulse AI",
        "version": "1.0.0",
        "features_active": [
            "Eligibility & Free Resource Curator",
            "State Improvement Level-Up Planner",
            "GitHub & Project Authenticity Inspector",
            "Company Drive Forensics (Battle Cards)"
        ]
    }
