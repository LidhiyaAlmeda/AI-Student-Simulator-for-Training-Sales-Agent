from fastapi import APIRouter
from pydantic import BaseModel
from database import get_user, create_user, update_password

router = APIRouter()

users = {}

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class ResetPasswordRequest(BaseModel):
    email: str
    new_password: str

@router.post("/register")
def register(data: dict):
    print("REGISTER REQUEST RECEIVED")
    print(data)

    try:
        create_user(
            data["name"],
            data["email"],
            data["password"]
        )

        return {
            "success": True
        }

    except Exception as e:
        return {
            "success": False,
            "message": str(e)
        }

@router.post("/login")
def login(data: dict):

    user = get_user(
        data["email"],
        data["password"]
    )

    if not user:
        return {
            "success": False,
            "message": "Invalid credentials"
        }

    return {
        "success": True,
        "user_id": user["id"],
        "name": user["name"],
        "email": user["email"]
    }

@router.post("/reset-password")
def reset_password(data: ResetPasswordRequest):

    updated = update_password(
        data.email,
        data.new_password
    )

    if not updated:
        return {
            "success": False,
            "message": "Email not found"
        }

    return {
        "success": True,
        "message": "Password updated"
    }
