import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from models import Base  # Make sure you import Base from your models.py

# Load environment variables from .env file
load_dotenv()

# Replace with your actual DATABASE_URL from Render (with ?sslmode=require)
DATABASE_URL = os.getenv("DATABASE_URL")

# Create the engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables
Base.metadata.create_all(bind=engine)
print("✅ All tables created successfully!")
