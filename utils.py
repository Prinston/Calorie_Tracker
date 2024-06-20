
from database import SessionLocal
import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()

APP_ID = os.getenv("APP_ID")
APP_KEY = os.getenv("APP_KEY")

API_URL = "https://trackapi.nutritionix.com/v2/natural/nutrients"





# Function to get a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
    

# Function to fetch calorie information from an external API
def get_calories_from_api(text: str):
    try:
         # URL and parameters for the API request
        url = API_URL
        headers = {
            "Content-Type": "application/json",
            "x-app-id": APP_ID,
            "x-app-key": APP_KEY
        }
        data = {
            "query": text
        }

        response = requests.post(url, headers=headers, json=data)

        response.raise_for_status()

        data = response.json()
        


        if data and "foods" in data  and  len(data["foods"])>0:
            calories = data["foods"][0]["nf_calories"]
            return calories
            

        else:
            logging.error(f"No calorie data found for food item: {text}")
            return None
        
    except requests.RequestException as e:
        logging.error(f"Error fetching calories from API: {e}")
        return None

