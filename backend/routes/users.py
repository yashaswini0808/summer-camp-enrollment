from typing import List, Optional
from fastapi import APIRouter, HTTPException, status
from backend.models_pydantic import UserOut, UserCreate, UserUpdate
from backend import firestore_crud as crud

router = APIRouter(prefix="/api/users", tags=["Users Management"])


@router.get("", response_model=List[UserOut], summary="GET /api/users - Retrieve users from Firestore")
def get_users():
    """
    Retrieves all user records from Firestore database.
    Flow: React -> FastAPI (routes/users.py) -> firestore_crud.py -> firebase.py -> Firestore
    """
    return crud.get_users()


@router.get("/{user_id}", response_model=UserOut, summary="GET /api/users/{user_id} - Get single user by ID")
def get_user(user_id: str):
    """Retrieves a single user record from Firestore by ID."""
    user = crud.get_user(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID '{user_id}' not found in Firestore."
        )
    return user


@router.post("", response_model=UserOut, status_code=status.HTTP_201_CREATED, summary="POST /api/users - Create new user in Firestore")
def create_user(user: UserCreate):
    """
    Creates a new user record in Firestore database.
    Flow: React -> FastAPI (routes/users.py) -> firestore_crud.py -> firebase.py -> Firestore
    """
    return crud.create_user(user_data=user)


@router.put("/{user_id}", response_model=UserOut, summary="PUT /api/users/{user_id} - Update existing user")
def update_user(user_id: str, user: UserUpdate):
    """Updates an existing user record in Firestore in-place without creating duplicate documents."""
    return crud.update_user(user_id=user_id, user_data=user)


@router.delete("/{user_id}", status_code=status.HTTP_200_OK, summary="DELETE /api/users/{user_id} - Delete user")
def delete_user(user_id: str):
    """Deletes a user record from Firestore database."""
    crud.delete_user(user_id=user_id)
    return {"message": f"User ID '{user_id}' successfully removed from Firestore."}
