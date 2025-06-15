# Calorie Tracker API

This is a RESTful API built with FastAPI and PostgreSQL that allows users to track their calorie intake. It supports user authentication using JWT, and offers endpoints for creating, reading, updating, and deleting meals.

## Features

- User registration and authentication (JWT)
- Add meals with calorie values
- View daily calorie summary
- Edit or delete meal entries
- FastAPI auto-generated Swagger docs

## Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- JWT (PyJWT)
- Alembic (for migrations)

## Setup Instructions

1. Clone the repository:
   ```
   git clone https://github.com/Prinston/calorie-tracker-api.git
   cd calorie-tracker-api
   ```

2. Create and activate a virtual environment:
   ```
   python -m venv env
   source env/bin/activate  # or `env\Scripts\activate` on Windows
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Set up the database:
   - Create a PostgreSQL database (e.g., `calorie_tracker`)
   - Configure your `.env` or `config.py` file with DB credentials

5. Run the app:
   ```
   uvicorn main:app --reload
   ```

## API Docs
Visit `http://127.0.0.1:8000/docs` for interactive Swagger UI.

## Future Improvements

- User dashboard with charts
- Meal categorization (breakfast, lunch, etc.)
- Email alerts for overconsumption
