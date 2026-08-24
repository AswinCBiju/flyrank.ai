from fastapi import APIRouter
from supabase_client import supabase

router = APIRouter(prefix="/auth", tags=["Auth"])
