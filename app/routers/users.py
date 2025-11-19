from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=schemas.UserResponse)
def read_me(current_user = Depends(get_current_user)):
    return current_user


@router.get("/me/profile", response_model=schemas.UserProfileResponse)
def get_my_profile(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    profile = crud.get_profile(db, current_user.id)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.post("/me/profile", response_model=schemas.UserProfileResponse)
def create_or_update_profile(payload: schemas.UserProfileCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    # ensure user_id matches token user
    if payload.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot modify other user's profile")
    profile = crud.create_or_update_profile(db, user_id=payload.user_id, name=payload.name, weight=payload.weight, height=payload.height)
    return profile
