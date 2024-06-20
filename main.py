from fastapi import FastAPI, status, Depends, HTTPException
from routes.api_routes import api_router
from routes.auth_route import auth_router, get_current_user
from utils import get_db
from sqlalchemy.orm import Session

# Create a FastAPI app instance
app = FastAPI()

# Define a route for the root path ("/")
@app.get("/", status_code=status.HTTP_200_OK)
def user(user: dict = Depends(get_current_user), db: Session = Depends(get_db)):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication Failed")
    return {"User": user}

# Include the API and authentication routers in the main app
app.include_router(api_router)
app.include_router(auth_router)
