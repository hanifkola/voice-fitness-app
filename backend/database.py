import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Put your exact connection string here for testing
DATABASE_URL = "postgresql://user123:password123@dpg-cvfc81ggph6c73bbi1lg-a.oregon-postgres.render.com:5432/voice_fitness_db"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)
