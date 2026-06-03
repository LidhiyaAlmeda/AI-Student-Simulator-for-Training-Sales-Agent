from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

users = {}

class RegisterRequest(BaseModel):
    name: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/register")
def register(data: RegisterRequest):

    if data.email in users:
        return {
            "success": False,
            "message": "Email already exists"
        }

    users[data.email] = {
        "name": data.name,
        "password": data.password
    }

    return {
        "success": True
    }


@router.post("/login")
def login(data: LoginRequest):

    user = users.get(data.email)

    if not user:
        return {
            "success": False,
            "message": "User not found"
        }

    if user["password"] != data.password:
        return {
            "success": False,
            "message": "Wrong password"
        }

    return {
        "success": True,
        "name": user["name"]
    }
