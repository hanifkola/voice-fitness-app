from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

DATABASE_URL = "postgresql://hanif:YbA3QHGX8CYNR2WtJYKfzzsx6Z4HpzaI@dpg-cvfc81ggph6c73bbi1lg-a/vftest"

#create database engine
engine = create_engine(DATABASE_URL)

#create session local (for interacting with the database)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#delare base class for ORM models
Base = declarative_base()

#create all table in the database (if not exists)
Base.metadata.create_all(bind=engine)
