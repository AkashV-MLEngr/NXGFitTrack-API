from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ============================
# User Schemas
# ============================

class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True


# ============================
# User Profile Schemas
# ============================

class UserProfileBase(BaseModel):
    name: str
    weight: Optional[float] = None
    height: Optional[float] = None


class UserProfileCreate(UserProfileBase):
    user_id: int


class UserProfileResponse(UserProfileBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


# ============================
# Template Exercise Schemas
# ============================

class TemplateExerciseBase(BaseModel):
    exercise_name: str
    sets: Optional[int] = None
    reps: Optional[int] = None
    weight: Optional[float] = None
    notes: Optional[str] = None


class TemplateExerciseCreate(TemplateExerciseBase):
    # template_id: int
    pass


class TemplateExerciseResponse(TemplateExerciseBase):
    id: int

    class Config:
        orm_mode = True


# ============================
# Workout Template Schemas
# ============================

class WorkoutTemplateBase(BaseModel):
    workout_name: str
    description: Optional[str] = None
    exercise_id: Optional[int] = None


class WorkoutTemplateCreate(WorkoutTemplateBase):
    user_id: int


class WorkoutTemplateResponse(WorkoutTemplateBase):
    id: int
    user_id: int
    template_exercises: List[TemplateExerciseResponse] = []

    class Config:
        orm_mode = True


# ============================
# Completed History Schemas
# ============================

class CompletedHistoryBase(BaseModel):
    workout_name: str
    total_volume: Optional[float] = None


class CompletedHistoryCreate(CompletedHistoryBase):
    user_id: int
    template_id: Optional[int] = None



class CompletedHistoryResponse(BaseModel):
    id: int
    user_id: int
    template_id: Optional[int] = None
    workout_name: str
    total_volume: Optional[float] = None
    completed_at: datetime  # <-- keep as datetime, Pydantic will convert to ISO string


    class Config:
        orm_mode = True
