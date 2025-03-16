from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
from sqlalchemy.orm import Boolean

Base = declarative_base()

class WorkoutLog(Base):
    __tablename__ = "workout_logs"

    id = Column(Integer, primary_key=True, index=True)
    exercise_name = Column(String, nullable=False)
    sets = Column(Integer, nullable=False)
    reps = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True,index = True,  nullable=False)
    hashed_password = Column(String, Unique = True, index = True, nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    
    
