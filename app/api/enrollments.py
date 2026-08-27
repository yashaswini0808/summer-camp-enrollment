from typing import List, Optional, Union
from fastapi import APIRouter, Query, HTTPException, status
from app.models_pydantic import EnrollmentCreate, EnrollmentOut
from app import firestore_crud as crud

router = APIRouter(prefix="/api/enrollments", tags=["Enrollments"])

@router.post("", response_model=EnrollmentOut, status_code=status.HTTP_201_CREATED, summary="Enroll student in a sport activity")
def create_enrollment(payload: EnrollmentCreate):
    """
    Submits a new participant enrollment to Firestore. Performs validations:
    - Sport document must exist and be active
    - Participant age must be between sport's min_age and max_age
    - Sport must have capacity remaining
    - Duplicate check for same participant + sport in Firestore
    """
    return crud.create_enrollment(data=payload)

@router.get("", response_model=List[EnrollmentOut], summary="List enrollments from Firestore")
def list_enrollments(
    email: Optional[str] = Query(None, description="Filter by parent email"),
    phone: Optional[str] = Query(None, description="Filter by parent phone"),
    participant: Optional[str] = Query(None, description="Filter by participant name"),
    sport_id: Optional[str] = Query(None, description="Filter by sport ID"),
    status: Optional[str] = Query(None, description="Filter by status (CONFIRMED / CANCELLED / ALL)")
):
    return crud.get_enrollments(
        email=email,
        phone=phone,
        participant=participant,
        sport_id=sport_id,
        status_filter=status
    )

@router.get("/{code}", response_model=EnrollmentOut, summary="Lookup single enrollment by code")
def get_enrollment_by_code(code: str):
    enrollment = crud.get_enrollment_by_code(code=code)
    if not enrollment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Enrollment code '{code}' not found in Firestore."
        )
    return enrollment

@router.put("/{enrollment_id}/cancel", response_model=EnrollmentOut, summary="Cancel an enrollment & update capacity")
def cancel_enrollment(enrollment_id: str):
    return crud.cancel_enrollment(enrollment_id=enrollment_id)
