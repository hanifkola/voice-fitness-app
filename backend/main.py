from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import WorkoutLog
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime
from fastapi import HTTPException, File, UploadFile
from models import User
from auth import hash_password, verify_password, get_current_user
from sqlalchemy.exc import IntegrityError
from pydantic import EmailStr
from jwt_handler import create_access_token, verify_access_token




# Initialize FastAPI app
app = FastAPI()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic model for incoming workout data
class WorkoutCreate(BaseModel):
    exercise_name: str = Field(..., min_length=2, max_length=100) #exercise name must be between 2 and 100 characters
    sets: int = Field(..., gt=0, lt=100)  # Must be greater than 0, less than 100
    reps: int = Field(..., gt=0, lt=100)  # Must be greater than 0, less than 100
    weight: float = Field(..., gt=0)      # Must be greater than 0

# Response model (what API returns to user)
class Workout(BaseModel):
    id: int
    exercise_name: str
    sets: int
    reps: int
    weight: float
    timestamp: str  # Or datetime, but string is fine for now

class Config:
        orm_mode = True  # To allow working with SQLAlchemy models directly
# API to add a new workout log
@app.post("/workouts/")
def create_workout(workout: WorkoutCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_workout = WorkoutLog(
        exercise_name=workout.exercise_name,
        sets=workout.sets,
        reps=workout.reps,
        weight=workout.weight,
        user_id=current_user["user_id"]  #user_id is the id of the user who is logged in
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

class workout(BaseModel):
    id: int
    exercise_name: str
    sets: int
    reps: int
    weight: float
    timestamp: datetime
class config:
    orm_mode = True #important to work with sqlalchemy models 
# GET API to fetch all workout logs 
@app.get("/workouts/", response_model=List[workout])
def read_workouts(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    workouts = db.query(WorkoutLog).filter(WorkoutLog.user_id == current_user["user_id"]).all()
    return workouts
# API to update an existing workout log
@app.put("/workouts/{workout_id}", response_model=Workout)
def update_workout(workout_id: int, workout: WorkoutCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_workout = db.query(WorkoutLog).filter(WorkoutLog.id == workout_id).first()
    if db_workout is None:
        raise HTTPException(status_code=404, detail="Workout log not found")

    db_workout.exercise_name = workout.exercise_name
    db_workout.sets = workout.sets
    db_workout.reps = workout.reps
    db_workout.weight = workout.weight

    db.commit()
    db.refresh(db_workout)
    return db_workout
# API to delete an existing workout log
@app.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_workout = db.query(WorkoutLog).filter(WorkoutLog.id == workout_id, WorkoutLog.user_id == current_user["user_id"]).first()
    if db_workout is None:
         raise HTTPException(status_code=404, detail="Workout log not found")

    db.delete(db_workout)
    db.commit()
    return {"message": f"Workout log {workout_id} deleted successfully."}
@app.get("/")
def read_root():
    return {"message": "Welcome to Voice Fitness API! Check /docs for full API."}
class UserCreate(BaseModel):
    email: EmailStr
    password: str

@app.post("signup/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    hashed_pw = hash_password(user.password)
    db_user = User(email=user.email, hashed_password=hashed_pw)

    db.add(db_user)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        return {"error": "Email already registered."}

    db.refresh(db_user)
    return {"message": "User created successfully", "user_id": db_user.id}

class UserLogin(BaseModel):
    email: EmailStr
    password: str

@app.post("/login/")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        return {"error": "Invalid email or password"}

    # Create JWT token
    access_token = create_access_token({"sub": db_user.email, "user_id": db_user.id, "is_admin": db_user.is_admin})
    return {"access_token": access_token, "token_type": "bearer"}

# Mock response for now
@app.post("/voice-log/")
async def voice_log(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    # In future: process file with AI (Whisper, Google, etc.)

    # For now: pretend we parsed it and return structured workout data
    mock_response = {
        "exercise_name": "Push Ups",
        "sets": 3,
        "reps": 10,
        "weight": 0,
        "note": "Generated from voice command"
    }

    return {
        "message": "Voice command processed successfully.",
        "parsed_workout": mock_response
    }