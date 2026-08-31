import os
import uvicorn
from pathlib import Path
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

# Load environment variables from backend/.env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Initialize FastAPI app
app = FastAPI(
    title="Summer Camp Sports & User Management API",
    description="FastAPI Backend API layer connecting React Frontend to Google Cloud Firestore Database.",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# --------------------------------------------------------------------------
# Requirement 3: Enable CORS for React Frontend (Local Development & Network)
# --------------------------------------------------------------------------
cors_origins_raw = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:8000,http://127.0.0.1:8000,http://192.168.29.165:8000"
)
origins = [origin.strip() for origin in cors_origins_raw.split(",") if origin.strip()]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Firebase Database Client
from backend.firebase import initialize_firebase
initialize_firebase()

# Include Routers (Requirement 3 & 7 Architecture Flow)
from backend.routes import users, sports, enrollments, stats
app.include_router(users.router)
app.include_router(sports.router)
app.include_router(enrollments.router)
app.include_router(stats.router)

# Mount React static build files if present
frontend_dist = Path(__file__).resolve().parent.parent / "frontend" / "dist"
if frontend_dist.exists() and (frontend_dist / "index.html").exists():
    app.mount("/assets", StaticFiles(directory=str(frontend_dist / "assets")), name="assets")

    @app.get("/{full_path:path}", include_in_schema=False)
    async def serve_react_app(full_path: str):
        if full_path.startswith("api/"):
            return JSONResponse({"detail": "Not Found"}, status_code=404)
        file_path = frontend_dist / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(frontend_dist / "index.html")

@app.get("/health", tags=["System Health"])
def health_check():
    return {
        "status": "healthy",
        "service": "FastAPI Summer Camp & User Management Backend",
        "version": "2.0.0"
    }

if __name__ == "__main__":
    host = os.getenv("BACKEND_HOST", "0.0.0.0")
    port = int(os.getenv("BACKEND_PORT", 8000))
    print(f"==================================================")
    print(f"FASTAPI BACKEND SERVER RUNNING AT:")
    print(f"  Local API Docs:   http://localhost:{port}/docs")
    print(f"  Users API:        http://localhost:{port}/api/users")
    print(f"  Sports API:       http://localhost:{port}/api/sports")
    print(f"==================================================")
    uvicorn.run("backend.main:app", host=host, port=port, reload=True)
