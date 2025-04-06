from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timedelta
from typing import List
from jose import jwt
from pydantic import BaseModel, EmailStr
from database import SessionLocal
import models
from models import WorkoutLogCreate, WorkoutCreate, User, WorkoutLogResponse
from auth import hash_password, verify_password
from dependencies import get_current_user
from jwt_handler import create_access_token

# Initialize FastAPI app
app = FastAPI()

# Correct the token URL to the login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login/")

# CORS settings (Allow all origins for now)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Seed categories and equipment into the database
def seed_data(db: Session):
    categories = ["Strength", "Cardio", "Flexibility"]
    equipment = ["Dumbbell", "Barbell", "Machine", "Bodyweight"]

    for category in categories:
        if not db.query(models.WorkoutCategory).filter_by(name=category).first():
            db.add(models.WorkoutCategory(name=category))

    for equip in equipment:
        if not db.query(models.Equipment).filter_by(name=equip).first():
            db.add(models.Equipment(name=equip))

    db.commit()

# === User Authentication ===

class UserCreate(BaseModel):
    email: EmailStr
    password: str

@app.post("/signup/")
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
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == form_data.username).first()
    
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid username or password")
    
    access_token = jwt.encode(
        {"sub": user.email, "exp": datetime.utcnow() + timedelta(minutes=30)},
        "SECRET_KEY",
        algorithm="HS256"
    )
    return {"access_token": access_token, "token_type": "bearer"}

# === Workout APIs ===

@app.post("/workouts/")
def create_workout(workout: WorkoutLogCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_workout = models.WorkoutLog(
        workout_id=workout.workout_id,
        sets=workout.sets,
        reps=workout.reps,
        weight=workout.weight,
        user_id=current_user["user_id"]
    )
    db.add(db_workout)
    db.commit()
    db.refresh(db_workout)
    return db_workout

@app.get("/workouts/", response_model=List[WorkoutLogResponse])
def read_workouts(db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    workouts = db.query(models.WorkoutLog).filter(models.WorkoutLog.user_id == current_user["user_id"]).all()
    return workouts

@app.put("/workouts/{workout_id}", response_model=WorkoutLogResponse)
def update_workout(workout_id: int, workout: WorkoutLogCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_workout = db.query(models.WorkoutLog).filter(models.WorkoutLog.id == workout_id).first()
    if db_workout is None:
        raise HTTPException(status_code=404, detail="Workout log not found")
    
    if db_workout.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Not authorized to update this workout")

    db_workout.workout_id = workout.workout_id
    db_workout.sets = workout.sets
    db_workout.reps = workout.reps
    db_workout.weight = workout.weight

    db.commit()
    db.refresh(db_workout)
    return db_workout

@app.delete("/workouts/{workout_id}")
def delete_workout(workout_id: int, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    db_workout = db.query(models.WorkoutLog).filter(models.WorkoutLog.id == workout_id, models.WorkoutLog.user_id == current_user["user_id"]).first()
    if db_workout is None:
         raise HTTPException(status_code=404, detail="Workout log not found")

    db.delete(db_workout)
    db.commit()
    return {"message": f"Workout log {workout_id} deleted successfully."}

# === Voice Command (Mock Implementation) ===

@app.post("/voice-log/")
async def voice_log(file: UploadFile = File(...), current_user: dict = Depends(get_current_user)):
    # In future: process file with AI (Whisper, Google, etc.)
    mock_response = {
        "exercise_name": "Push Ups",
        "sets": 3,
        "reps": 10,
        "weight": 0,
        "note": "Generated from voice command"
    }
    return {"message": "Voice command processed successfully.", "parsed_workout": mock_response}

@app.get("/")
def read_root():
    return {"message": "Welcome to Voice Fitness API! Check /docs for full API."}

@app.on_event("startup")
def startup_event():
    db = SessionLocal()
    try:
        seed_data(db)
    finally:
        db.close()