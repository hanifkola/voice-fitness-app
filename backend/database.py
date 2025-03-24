import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Put your exact connection string here for testing
DATABASE_URL = "postgresql://hanif:YbA3QHGX8CYNR2WtJYKfzzsx6Z4HpzaI@dpg-cvfc81ggph6c73bbi1lg-a.oregon-postgres.render.com/vftest"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Base.metadata.create_all(bind=engine)
