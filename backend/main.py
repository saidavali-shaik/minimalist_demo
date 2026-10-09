from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from database import get_connection


app = FastAPI(title="Minimalist Demo API")


# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Contact(BaseModel):
    name: str
    email: str
    message: str


@app.get("/")
def home():
    return {
        "message": "Minimalist Demo API is running"
    }


@app.post("/api/contact")
def create_contact(contact: Contact):

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        query = """
        INSERT INTO contacts (name, email, message)
        VALUES (%s, %s, %s)
        RETURNING id, name, email, message, created_at;
        """

        cursor.execute(
            query,
            (
                contact.name,
                contact.email,
                contact.message
            )
        )

        result = cursor.fetchone()

        connection.commit()

        return {
            "success": True,
            "message": "Contact form submitted successfully",
            "data": {
                "id": result[0],
                "name": result[1],
                "email": result[2],
                "message": result[3],
                "created_at": result[4]
            }
        }

    except Exception as e:

        if connection:
            connection.rollback()

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()


@app.get("/api/contacts")
def get_contacts():

    connection = None
    cursor = None

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("""
            SELECT id, name, email, message, created_at
            FROM contacts
            ORDER BY id DESC;
        """)

        rows = cursor.fetchall()

        contacts = []

        for row in rows:
            contacts.append({
                "id": row[0],
                "name": row[1],
                "email": row[2],
                "message": row[3],
                "created_at": row[4]
            })

        return contacts

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )

    finally:

        if cursor:
            cursor.close()

        if connection:
            connection.close()