from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import pymysql
from fastapi import Request
import traceback

# Create FastAPI app instance
app = FastAPI()

# Set up Jinja2 for HTML templating
templates = Jinja2Templates(directory="templates")

# Database connection settings
db_settings = {
    "host": "localhost",
    "user": "root",  
    "password": "Hima2003",  
    "database": "project" 
}


@app.get("/", response_class=HTMLResponse)
async def registration_form(request: Request):
    try:
        return templates.TemplateResponse("registration_form.html", {"request": request})
    except Exception as e:
        print(f"Error rendering form: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error loading form")


@app.post("/register")
async def register(
    name: str = Form(...),
    lastname: str = Form(...),
    age: int = Form(...),
    contact: str = Form(...),
    gender: str = Form(...),
):
    try:
        # Connect to the database
        db = pymysql.connect(**db_settings)
        cursor = db.cursor()

        # Insert data into the database
        cursor.execute(
            "INSERT INTO users (name, lastname, age, contact, gender) VALUES (%s, %s, %s, %s, %s)",
            (name, lastname, age, contact, gender),
        )
        db.commit()
        cursor.close()
        db.close()

        return {"message": "User registered successfully"}

    except Exception as e:
        print(f"Error registering user: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error - Unable to register user")


@app.get("/users", response_class=HTMLResponse)
async def show_users(request: Request):
    try:
        # Connect to the database
        db = pymysql.connect(**db_settings)
        cursor = db.cursor()

        # Fetch all users from the database
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()

        cursor.close()
        db.close()

        return templates.TemplateResponse("user_list.html", {"request": request, "users": users})

    except Exception as e:
        print(f"Error fetching users: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Error fetching user data")


@app.post("/update")
async def update_user(
    id: int = Form(...),
    name: str = Form(...),
    lastname: str = Form(...),
    age: int = Form(...),
    contact: str = Form(...),
    gender: str = Form(...),
):
    try:
        db = pymysql.connect(**db_settings)
        cursor = db.cursor()

        cursor.execute(
            """
            UPDATE users 
            SET name = %s, lastname = %s, age = %s, contact = %s, gender = %s
            WHERE id = %s
            """,
            (name, lastname, age, contact, gender, id),
        )
        db.commit()
        cursor.close()
        db.close()

        return {"message": "User updated successfully"}

    except Exception as e:
        print(f"Error updating user: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error - Unable to update user")


@app.post("/delete")
async def delete_user(id: int = Form(...)):
    try:
        db = pymysql.connect(**db_settings)
        cursor = db.cursor()

        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        db.commit()

        cursor.close()
        db.close()

        return {"message": "User deleted successfully"}

    except Exception as e:
        print(f"Error deleting user: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail="Internal Server Error - Unable to delete user")
