import os
import threading
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse

from app.api import sports, enrollments, stats
from app.firestore_crud import seed_firestore_db

app = FastAPI(
    title="Summer Camp Sports Enrollment API (React & Google Firestore)",
    description="REST API for browsing summer camp sports activities, enrolling participants, and managing sports CRUD in Google Firestore.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Enable CORS for React frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routers
app.include_router(sports.router)
app.include_router(enrollments.router)
app.include_router(stats.router)

@app.get("/health", tags=["Health Check"])
def health_check():
    return {
        "status": "ok",
        "system": "Summer Camp Sports System (React + FastAPI + Google Firestore)",
        "version": "2.0.0"
    }

# Background thread for seeding on startup without blocking server launch
def async_seed_runner():
    try:
        seed_firestore_db()
    except Exception as e:
        print("[NOTICE] Seed check:", e)

@app.on_event("startup")
def startup_db():
    t = threading.Thread(target=async_seed_runner, daemon=True)
    t.start()

# Mount React static distribution if present
base_dir = os.path.dirname(os.path.abspath(__file__))
react_dist = os.path.join(base_dir, "frontend", "dist")

if os.path.exists(react_dist):
    assets_dir = os.path.join(react_dist, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")

    @app.get("/", response_class=HTMLResponse, tags=["Frontend React"])
    def serve_index():
        index_file = os.path.join(react_dist, "index.html")
        if os.path.exists(index_file):
            return FileResponse(index_file)
        return HTMLResponse("React frontend building...")
