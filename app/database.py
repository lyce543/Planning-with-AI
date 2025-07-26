import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv(dotenv_path="F:/python/calendar/app/.env")

# Get the database URL from the .env file
DATABASE_URL = os.getenv("DATABASE_URL")

# Check if DATABASE_URL is set
if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please check your .env file.")

# If you're using SQLite, you need special connect_args
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Create the database engine
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Create session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
