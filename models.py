from pydantic import BaseModel, Field
from datetime import date, time
from typing import Optional

# Pydantic model for a user
class CreateUserRequest(BaseModel):
    id:int
    username: str
    email: str
    password: str
    created_at: Optional[date]

   

# Pydantic model for a calorie entry
class CalorieEntryModel(BaseModel):
    id:int
    date: date
    time: time
    text: Optional[str]
    calories: Optional[float] = Field(default=None)
    user_id: int

class Config:
        orm_mode = True

# Pydantic model for creating or updating a calorie entry
class CalorieEntryUpdate(BaseModel):
    date: Optional[date] = None 
    time: Optional[time] = None
    text: Optional[str] = None
    calories: Optional[float] = Field(default=None)
    user_id: Optional[int] = None

# A response model for a created user
class UserModel(BaseModel):
    username: str
    email: str
    