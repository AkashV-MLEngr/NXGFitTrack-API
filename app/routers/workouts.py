from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, crud, models
from ..deps import get_db, get_current_user

router = APIRouter(prefix="/workouts", tags=["workouts"])


@router.post("/templates", response_model=schemas.WorkoutTemplateResponse)
def create_template(payload: schemas.WorkoutTemplateCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    if payload.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Cannot create template for another user")
    tpl = crud.create_workout_template(db, user_id=payload.user_id, workout_name=payload.workout_name, description=payload.description, exercise_id=payload.exercise_id)
    return tpl


@router.get("/templates", response_model=List[schemas.WorkoutTemplateResponse])
def list_templates(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return crud.get_templates_for_user(db, current_user.id)


@router.put("/templates/{template_id}", response_model=schemas.WorkoutTemplateResponse)
def update_template(template_id: int, payload: schemas.WorkoutTemplateBase, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    tpl = crud.get_template(db, template_id)
    if not tpl or tpl.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Template not found")

    updated = crud.update_workout_template(
        db,
        template_id=template_id,
        workout_name=payload.workout_name,
        description=payload.description,
    )

    return updated

@router.delete("/templates/{template_id}")
def delete_template(template_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    tpl = crud.get_template(db, template_id)
    if not tpl or tpl.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Template not found")

    crud.delete_workout_template(db, template_id)
    return {"message": "Template deleted successfully"}

# ========= Exercise
@router.post("/templates/{template_id}/exercises", response_model=schemas.TemplateExerciseResponse)
def add_exercise(template_id: int, payload: schemas.TemplateExerciseCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    tpl = crud.get_template(db, template_id)
    if not tpl or tpl.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Template not found")
    te = crud.add_template_exercise(db, template_id=template_id, exercise_name=payload.exercise_name, sets=payload.sets, reps=payload.reps, weight=payload.weight, notes=payload.notes)
    return te


@router.get("/templates/{template_id}/exercises", response_model=List[schemas.TemplateExerciseResponse])
def list_template_exercises(template_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    tpl = crud.get_template(db, template_id)
    if not tpl or tpl.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Template not found")
    return crud.get_exercises_for_template(db, template_id)

@router.put("/exercises/{exercise_id}", response_model=schemas.TemplateExerciseResponse)
def update_exercise(exercise_id: int, payload: schemas.TemplateExerciseBase, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    te = db.query(models.TemplateExercise).filter(models.TemplateExercise.id == exercise_id).first()
    if not te or te.template.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Exercise not found")

    updated = crud.update_template_exercise(
        db,
        exercise_id=exercise_id,
        exercise_name=payload.exercise_name,
        sets=payload.sets,
        reps=payload.reps,
        weight=payload.weight,
        notes=payload.notes,
    )

    return updated

@router.delete("/exercises/{exercise_id}")
def delete_exercise(exercise_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    te = db.query(models.TemplateExercise).filter(models.TemplateExercise.id == exercise_id).first()
    if not te or te.template.user_id != current_user.id:
        raise HTTPException(status_code=404, detail="Exercise not found")

    crud.delete_template_exercise(db, exercise_id)
    return {"message": "Exercise deleted successfully"}
