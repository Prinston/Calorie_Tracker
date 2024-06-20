from datetime import timedelta, datetime
from utils import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import User as User_DB
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
import logging
import os
from dotenv import load_dotenv



# Load environment variables from .env file
load_dotenv()

# Create a new APIRouter instance for authentication routes
auth_router = APIRouter(prefix="/auth", tags=['auth'])

# Secret key and algorithm for JWT token
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

# Create a password context for hashing passwords
pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

# Create an OAuth2PasswordBearer instance for token management
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='auth/token')


# Pydantic model for token response
class Token(BaseModel):
    access_token: str
    token_type: str


# Endpoint to generate an access token for authentication
@auth_router.post("/token", response_model=Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user")
        token = access_token(user.username, user.id, timedelta(minutes=60))
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        logging.error(f"Error generating access token: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Internal Server Error")


# Function to authenticate a user
def authenticate_user(username:str, password:str, db:Session):
    user = db.query(User_DB).filter(User_DB.username == username).first()
    if not user or not pwd_context.verify(password,user.hashed_password):
        return None
    return user


# Function to create an access token
def access_token(username: str, user_id: int, expires_delta: timedelta):
    # Create the payload with the username and user_id
    encode = {"sub": username, "id": user_id}
    
    # Calculate the expiration time
    expires = datetime.now() + expires_delta
    encode.update({"exp": expires})
    
    # Encode the token
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


# Function to get the current user using the access token
def get_current_user(token:str = Depends(oauth2_bearer)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        user_id = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not Validate User")
        return {"username": username, "id":user_id}
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not Validate User")