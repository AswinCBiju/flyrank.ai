from fastapi import APIRouter, Header
from fastapi.responses import JSONResponse
from supabase_client import supabase
from pydantic import BaseModel
from typing import Optional

router = APIRouter(prefix="/auth", tags=["Auth"])

class UserAuth(BaseModel):
    email: str
    password: str

@router.post("/signup")
def signup(user: UserAuth):
    if not user.email or not user.password:
        return JSONResponse(
            status_code=400,
            content={
                "error":"SignUp failed"
            }
        )
    try:
        res = supabase.auth.sign_up({
            "email": user.email,
            "password": user.password
        })

        if not res.user:
            return JSONResponse(
                status_code=400,
                content={
                    "error":"SignUp failed"
                }
            )
        
        user_data = res.user.model_dump() if hasattr(res.user, "model_dump") else res.user.__dict__

        return JSONResponse(
            status_code=201,
            content={
                "user":user_data
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "error":str(e)
            }
        )


@router.post("/login")
def login(user: UserAuth):
    if not user.email or not user.password:
        return JSONResponse(
            status_code=400,
            content={
                "error":"Email and password are required"
            }
        )
    
    try:
        res = supabase.auth.sign_in_with_password({
            "email": user.email,
            "password": user.password
        })

        return JSONResponse(
            status_code=200,
            content={
                "access_token": res.session.access_token,
                "refresh_token": res.session.refresh_token
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=400,
            content={
                "error":"Invalid Login credentials"
            }
        )


@router.get("/protected/profile")
def protectedInfo(authorization: Optional[str] = Header(None)):
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={
                "error": "Access Token required"
            }
        )
    token = authorization.split(" ")[1] if len(authorization.split(" ")) > 1 else ""

    if not token:
        return JSONResponse(
            status_code=401,
            content={
                "error": "Access Token required"
            }
        )
    
    user = supabase.auth.get_user(token).user
    
    return JSONResponse(
        status_code=200,
        content={
            "message": "Access granted to protected profile",
            "token": token,
            "user_metadata": user.user_metadata,
            "email": user.email,
            "id": user.id
        }
    )
