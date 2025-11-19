from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/history", tags=["history"])


@router.post("/complete", response_model=schemas.CompletedHistoryResponse)
def record_complete(payload: schemas.CompletedHistoryCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if payload.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot record history for another user")
    ch = crud.record_completed_history(db, user_id=payload.user_id, template_id=payload.template_id, workout_name=payload.workout_name, total_volume=payload.total_volume)
    return ch


@router.get("/", response_model=List[schemas.CompletedHistoryResponse])
def list_history(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud.list_completed_history(db, current_user.id)

@router.delete("/all")
def delete_all_user_history(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    deleted_count = crud.delete_all_history(db, current_user.id)
    return {"message": f"Deleted {deleted_count} history record(s)"}
