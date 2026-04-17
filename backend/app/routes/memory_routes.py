from fastapi import APIRouter
from app.modules.memory.memory_store import fetch_memory

router = APIRouter()

@router.get("/history")
def get_history():
    return {"history": fetch_memory()}