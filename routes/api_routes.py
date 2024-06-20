from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from models import CalorieEntryModel, CalorieEntryUpdate, CreateUserRequest, UserModel
from utils import get_db, get_calories_from_api
from database import CalorieEntry as CalorieEntry_DB, User as User_DB 
import logging
from routes.auth_route import pwd_context

api_router = APIRouter(prefix="/api", tags=['Calorie Entry'])



# Endpoint to create a new user
@api_router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserModel)
def create_user(user: CreateUserRequest, db: Session = Depends(get_db)):
    try:
        existing_user = db.query(User_DB).filter(User_DB.email == user.email).first()
        if existing_user:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User Already Exists")

        new_user = User_DB(username=user.username, email=user.email, hashed_password=pwd_context.hash(user.password))
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        logging.error(f"Error creating user: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


# Endpoint to Get all calorie entries from the database.
@api_router.get("/calories", status_code=status.HTTP_200_OK, response_model=list[CalorieEntryModel])
async def get_entries(db: Session = Depends(get_db)):
    try:
        calorie_entries = db.query(CalorieEntry_DB).all()
        return calorie_entries
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


# Endpoint to Get a calorie entry by its ID.
@api_router.get("/calories/{id}", status_code=status.HTTP_200_OK, response_model=CalorieEntryModel)
async def get_by_id(id: int, db: Session = Depends(get_db)):

    calorie_entry = db.query(CalorieEntry_DB).filter(CalorieEntry_DB.id == id).first()
    if not calorie_entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calorie Entry Not Found")
    return calorie_entry


#Endpoint to Create a new calorie entry.
@api_router.post("/calories", status_code=status.HTTP_201_CREATED, response_model=CalorieEntryModel)
async def create_entry(entry: CalorieEntryModel, db: Session = Depends(get_db)):
    # Check if the user exists
    user = db.query(User_DB).filter(User_DB.id == entry.user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User Not Found")

    # Get Calories from External API if not Provided
    if entry.calories is None:
        logging.info("Calories not provided, fetching from API")
        fetched_calories = get_calories_from_api(entry.text)
        if fetched_calories is None:
            entry.calories = 0
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Calories information not found")
        entry.calories = fetched_calories
        logging.info(f"Calories fetched from API: {fetched_calories}")

    # Create new calorie entry
    new_entry = CalorieEntry_DB(
        date=entry.date,
        time=entry.time,
        text=entry.text,
        calories=entry.calories,
        user_id=entry.user_id
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
    logging.info(f"New entry created: {new_entry}")
    return new_entry


# Endpoint to Update a calorie entry by its ID.
@api_router.put("/calories/{id}", status_code=status.HTTP_200_OK, response_model=CalorieEntryModel)
async def update_entry(id: int, entry_update: CalorieEntryUpdate, db: Session = Depends(get_db)):
   
    entry = db.query(CalorieEntry_DB).filter(CalorieEntry_DB.id == id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calorie Entry Not Found")
    
    try:
        # Update each field if the new value is not None or an empty string
        for field in ["date", "time", "text", "calories"]:
            new_value = getattr(entry_update, field)
            if new_value is not None and new_value != "":
                setattr(entry, field, new_value)

        db.commit()
        db.refresh(entry)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail="Calorie Entry Not Updated")
    return entry


# Endpoint to Delete a calorie entry by its ID.
@api_router.delete("/calories/{id}", status_code=status.HTTP_200_OK)
async def delete_entry(id: int, db: Session = Depends(get_db)):

    entry = db.query(CalorieEntry_DB).filter(CalorieEntry_DB.id == id).first()
    if not entry:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Calorie Entry Not Found")
    
    db.delete(entry)
    db.commit()

    return {"Message": "Entry Deleted Successfully"}




        