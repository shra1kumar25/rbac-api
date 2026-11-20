from fastapi import APIRouter, HTTPException, Depends
from app.models import users
from app.auth import create_token, get_current_user

router = APIRouter()

def admin_required(user):

    if user["role"] != "ADMIN":
        raise HTTPException(
            status_code=403,
            detail="Admin Access Required"
        )

@router.post("/login")
def login(data: dict):

    for user in users:
        if (
            user["username"] == data["username"]
            and
            user["password"] == data["password"]
        ):
            token = create_token(user)

            return {
                "access_token": token
            }

    raise HTTPException(
        status_code=401,
        detail="Invalid Credentials"
    )


# ADD THIS BELOW THE LOGIN API

@router.get("/admin/users")
def get_users(
    user=Depends(get_current_user)
):
    admin_required(user)

    return users
