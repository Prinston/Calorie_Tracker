from sqlalchemy import create_engine, Column, Integer, String, Float,ForeignKey, Date, Time, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.sql import func
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


# Get database credentials from environment variables
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "1234")
DB_SERVER = os.getenv("DB_SERVER", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "postgres")


# Create the database URL
DB_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_SERVER}/{DB_NAME}"

# Create a SQLAlchemy engine
engine = create_engine(DB_URL)

# Create a base class for declarative class definitions
Base = declarative_base()

# Define the User model
class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, server_default=func.now())

    calorie_entries = relationship("CalorieEntry", back_populates="user")

# Define the CalorieEntry model
class CalorieEntry(Base):
    __tablename__ = 'calorie_entries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)
    text = Column(String)
    calories = Column(Float, nullable=True)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", back_populates="calorie_entries")

# Create the tables in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
SessionLocal = sessionmaker(autoflush=False, autocommit=False,bind=engine)

