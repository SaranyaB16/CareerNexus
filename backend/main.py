import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.database import init_db
from backend.seed_data import seed_database
from backend.routers import (
    students, drives, diagnostics, github_validator,
    alerts, mock_interview, recruiter, alumni,
    analytics, applications, auth
)

app = FastAPI(
    title="CareerNexus",
    description="Intelligent Campus Placement & Career Management Platform",
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

# Register All API Routers
app.include_router(students.router)
app.include_router(drives.router)
app.include_router(diagnostics.router)
app.include_router(github_validator.router)
app.include_router(alerts.router)
app.include_router(mock_interview.router)
app.include_router(recruiter.router)
app.include_router(alumni.router)
app.include_router(analytics.router)
app.include_router(applications.router)
app.include_router(auth.router)

# Mount frontend static files
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")


@app.on_event("startup")
def startup_event():
    init_db()
    seed_database()


@app.get("/")
def serve_index():
    index_file = os.path.join(frontend_dir, "index.html")
    if os.path.exists(index_file):
        return FileResponse(index_file)
    return {
        "app": "CareerNexus",
        "docs": "/docs",
        "message": "CareerNexus API is running smoothly!"
    }


@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": "CareerNexus",
        "version": "1.0.0",
        "features_active": [
            "Eligibility & Free Resource Curator",
            "State Improvement Level-Up Planner",
            "GitHub & Project Authenticity Inspector",
            "Placement Opportunity Alerts",
            "AI Mock Interview Coach",
            "Recruiter Reverse Pitch Sourcing",
            "Alumni Warm Referral Bridge",
            "TPO At-Risk Radar & Analytics"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("backend.main:app", host="0.0.0.0", port=port, reload=True)

