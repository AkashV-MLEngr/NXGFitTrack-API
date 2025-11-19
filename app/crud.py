from sqlalchemy.orm import Session
from . import models, schemas, auth
from typing import List, Optional

# ----- Users -----
def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, email: str, password: str) -> models.User:
    hashed = auth.get_password_hash(password)
    user = models.User(email=email, password=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

# ----- Profiles -----
def get_profile(db: Session, user_id: int) -> Optional[models.UserProfile]:
    return db.query(models.UserProfile).filter(models.UserProfile.user_id == user_id).first()

def create_or_update_profile(db: Session, user_id: int, name: str, weight: float = None, height: float = None) -> models.UserProfile:
    profile = get_profile(db, user_id)
    if not profile:
        profile = models.UserProfile(user_id=user_id, name=name, weight=weight, height=height)
        db.add(profile)
    else:
        profile.name = name
        profile.weight = weight
        profile.height = height
    db.commit()
    db.refresh(profile)
    return profile

# ----- Workout Templates -----
def create_workout_template(db: Session, user_id: int, workout_name: str, description: str = None, exercise_id: int = None) -> models.WorkoutTemplate:
    tpl = models.WorkoutTemplate(user_id=user_id, workout_name=workout_name, description=description, exercise_id=exercise_id)
    db.add(tpl)
    db.commit()
    db.refresh(tpl)
    return tpl

def get_templates_for_user(db: Session, user_id: int) -> List[models.WorkoutTemplate]:
    return db.query(models.WorkoutTemplate).filter(models.WorkoutTemplate.user_id == user_id).all()

def get_template(db: Session, template_id: int) -> Optional[models.WorkoutTemplate]:
    return db.query(models.WorkoutTemplate).filter(models.WorkoutTemplate.id == template_id).first()
def update_workout_template(db: Session, template_id: int, workout_name: str = None, description: str = None) -> Optional[models.WorkoutTemplate]:
    tpl = db.query(models.WorkoutTemplate).filter(models.WorkoutTemplate.id == template_id).first()
    if not tpl:
        return None

    if workout_name is not None:
        tpl.workout_name = workout_name
    if description is not None:
        tpl.description = description

    db.commit()
    db.refresh(tpl)
    return tpl

def delete_workout_template(db: Session, template_id: int) -> bool:
    tpl = db.query(models.WorkoutTemplate).filter(models.WorkoutTemplate.id == template_id).first()
    if not tpl:
        return False

    db.delete(tpl)
    db.commit()
    return True

# ----- Template Exercises -----
def add_template_exercise(db: Session, template_id: int, exercise_name: str, sets: int = None, reps: int = None, weight: float = None, notes: str = None) -> models.TemplateExercise:
    te = models.TemplateExercise(template_id=template_id, exercise_name=exercise_name, sets=sets, reps=reps, weight=weight, notes=notes)
    db.add(te)
    db.commit()
    db.refresh(te)
    return te

def get_exercises_for_template(db: Session, template_id: int) -> List[models.TemplateExercise]:
    return db.query(models.TemplateExercise).filter(models.TemplateExercise.template_id == template_id).all()

def update_template_exercise(
    db: Session,
    exercise_id: int,
    exercise_name: str = None,
    sets: int = None,
    reps: int = None,
    weight: float = None,
    notes: str = None,
) -> Optional[models.TemplateExercise]:
    
    te = db.query(models.TemplateExercise).filter(models.TemplateExercise.id == exercise_id).first()
    if not te:
        return None

    if exercise_name is not None:
        te.exercise_name = exercise_name
    if sets is not None:
        te.sets = sets
    if reps is not None:
        te.reps = reps
    if weight is not None:
        te.weight = weight
    if notes is not None:
        te.notes = notes

    db.commit()
    db.refresh(te)
    return te

def delete_template_exercise(db: Session, exercise_id: int) -> bool:
    te = db.query(models.TemplateExercise).filter(models.TemplateExercise.id == exercise_id).first()
    if not te:
        return False

    db.delete(te)
    db.commit()
    return True

# ----- Completed History -----
def record_completed_history(db: Session, user_id: int, template_id: Optional[int], workout_name: str, total_volume: float = None) -> models.CompletedHistory:
    ch = models.CompletedHistory(user_id=user_id, template_id=template_id, workout_name=workout_name, total_volume=total_volume)
    db.add(ch)
    db.commit()
    db.refresh(ch)
    return ch

def list_completed_history(db: Session, user_id: int, limit: int = 50):
    return db.query(models.CompletedHistory).filter(models.CompletedHistory.user_id == user_id).order_by(models.CompletedHistory.completed_at.desc()).limit(limit).all()

def delete_all_history(db: Session, user_id: int) -> int:
    """Delete all completed history for a user. Returns number of deleted records."""
    deleted = db.query(models.CompletedHistory).filter(models.CompletedHistory.user_id == user_id).delete()
    db.commit()
    return deleted
