import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from models import Base  # Make sure you import Base from your models.py

# Load environment variables from .env file
load_dotenv()

# Read DATABASE_URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")  

# Create the PostgreSQL database connection
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Create all tables in the PostgreSQL database
if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    print("✅ All tables created successfully!")
