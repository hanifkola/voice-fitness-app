from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from pydantic import BaseModel

Base = declarative_base()

# Category Model
class WorkoutCategory(Base):
    __tablename__ = "workout_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    workouts = relationship("Workout", back_populates="category")


# Equipment Model
class Equipment(Base):
    __tablename__ = "equipment"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)

    workouts = relationship("Workout", back_populates="equipment")


# Workout Model
class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)
    exercise_name = Column(String, nullable=False)
    category_id = Column(Integer, ForeignKey("workout_categories.id"))
    equipment_id = Column(Integer, ForeignKey("equipment.id"))
    body_part = Column(String, nullable=False)  # e.g., Chest, Legs, Back

    category = relationship("WorkoutCategory", back_populates="workouts")
    equipment = relationship("Equipment", back_populates="workouts")


# Workout Log Model
class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Link to user
    workout_id = Column(Integer, ForeignKey("workouts.id"), nullable=False)  # Link to workout
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    workout = relationship("Workout")
    user = relationship("User")


# User Model
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)


# Pydantic Models (for API)
class WorkoutCreate(BaseModel):
    exercise_name: str
    category_id: int
    equipment_id: int
    body_part: str


class WorkoutLogCreate(BaseModel):
    workout_id: int
    sets: int
    reps: int
    weight: float


class WorkoutResponse(BaseModel):
    id: int
    exercise_name: str
    category_id: int
    equipment_id: int
    body_part: str

    class Config:
        from_attributes = True


class WorkoutLogResponse(BaseModel):
    id: int
    workout_id: int
    sets: int
    reps: int
    weight: float
    timestamp: str

    class Config:
        from_attributes = True
