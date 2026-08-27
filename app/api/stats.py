from fastapi import APIRouter
from app.models_pydantic import StatsOut
from app import firestore_crud as crud

router = APIRouter(prefix="/api/stats", tags=["Dashboard Statistics"])

@router.get("", response_model=StatsOut, summary="Get summary statistics from Firestore")
def get_stats():
    return crud.get_dashboard_stats()
