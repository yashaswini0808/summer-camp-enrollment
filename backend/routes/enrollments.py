from typing import List, Optional
from fastapi import APIRouter, Query, status, HTTPException
from backend.models_pydantic import EnrollmentOut, EnrollmentCreate
from backend import firestore_crud as crud

router = APIRouter(prefix="/api/enrollments", tags=["Student Registrations"])


@router.get("", response_model=List[EnrollmentOut], summary="List all student registrations")
def list_enrollments(
    status: Optional[str] = Query("ALL", description="Filter by status (CONFIRMED, CANCELLED, ALL)")
):
    return crud.get_enrollments(status_filter=status)


@router.post("", response_model=EnrollmentOut, status_code=status.HTTP_201_CREATED, summary="Submit student registration")
def create_enrollment(data: EnrollmentCreate):
    return crud.create_enrollment(data=data)
