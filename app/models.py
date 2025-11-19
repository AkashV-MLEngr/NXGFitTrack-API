from sqlalchemy import Column, Integer, String, Text, Float, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    profile = relationship("UserProfile", back_populates="user", uselist=False)
    workout_templates = relationship("WorkoutTemplate", back_populates="user")
    completed_history = relationship("CompletedHistory", back_populates="user")


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    name = Column(String, nullable=False)
    weight = Column(Float)
    height = Column(Float)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="profile")


class WorkoutTemplate(Base):
    __tablename__ = "workout_templates"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    workout_name = Column(String, nullable=False)
    description = Column(Text)
    exercise_id = Column(Integer)   # optional; not FK now
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="workout_templates")
    template_exercises = relationship("TemplateExercise", back_populates="template")
    completed_history = relationship("CompletedHistory", back_populates="template")


class TemplateExercise(Base):
    __tablename__ = "template_exercises"

    id = Column(Integer, primary_key=True, index=True)
    template_id = Column(Integer, ForeignKey("workout_templates.id", ondelete="CASCADE"))

    exercise_name = Column(String, nullable=False)
    sets = Column(Integer)
    reps = Column(Integer)
    weight = Column(Float)
    notes = Column(Text)
    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    template = relationship("WorkoutTemplate", back_populates="template_exercises")


class CompletedHistory(Base):
    __tablename__ = "completed_history"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    template_id = Column(Integer, ForeignKey("workout_templates.id", ondelete="SET NULL"))

    workout_name = Column(String, nullable=False)
    total_volume = Column(Float)
    completed_at = Column(TIMESTAMP(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="completed_history")
    template = relationship("WorkoutTemplate", back_populates="completed_history")
