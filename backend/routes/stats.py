from fastapi import APIRouter
from backend.models_pydantic import StatsOut
from backend import firestore_crud as crud

router = APIRouter(prefix="/api/stats", tags=["Dashboard Analytics"])


@router.get("", response_model=StatsOut, summary="Get dashboard metrics and popular sports")
def get_stats():
    return crud.get_dashboard_stats()
