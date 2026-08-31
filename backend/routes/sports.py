from typing import List, Optional
from fastapi import APIRouter, Query, status, HTTPException
from backend.models_pydantic import SportOut, SportCreate, SportUpdate
from backend import firestore_crud as crud

router = APIRouter(prefix="/api/sports", tags=["Sports Activities"])


@router.get("", response_model=List[SportOut], summary="List sports activities from Firestore")
def list_sports(
    category: Optional[str] = Query(None, description="Filter by category"),
    age: Optional[int] = Query(None, description="Filter by age suitability"),
    search: Optional[str] = Query(None, description="Search keyword in title, coach, description"),
    active_only: bool = Query(True, description="Return active sports only")
):
    return crud.get_sports(category=category, age=age, search=search, active_only=active_only)


@router.get("/{sport_id}", response_model=SportOut, summary="Get single sport activity by ID")
def get_sport(sport_id: str):
    sport = crud.get_sport_by_id(sport_id)
    if not sport:
        raise HTTPException(status_code=404, detail=f"Sport ID '{sport_id}' not found in Firestore.")
    return sport


@router.post("", response_model=SportOut, status_code=status.HTTP_201_CREATED, summary="ADD new sport activity")
def create_sport(sport: SportCreate):
    return crud.create_sport(sport_data=sport)


@router.put("/{sport_id}", response_model=SportOut, summary="EDIT / UPDATE existing sport activity in-place")
def update_sport(sport_id: str, sport: SportUpdate):
    return crud.update_sport(sport_id=sport_id, sport_data=sport)


@router.delete("/{sport_id}", status_code=status.HTTP_200_OK, summary="DELETE / Deactivate sport activity")
def delete_sport(sport_id: str):
    crud.delete_sport(sport_id=sport_id)
    return {"message": f"Sport ID '{sport_id}' successfully removed from Firestore."}
