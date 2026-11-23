from fastapi import APIRouter
from pydantic import BaseModel
from app.modules.memory.memory_store import fetch_memory
from app.core.agent_tools import tool_memory_manager

router = APIRouter()


class MemoryItem(BaseModel):
    key: str
    value: str


@router.get("/history")
def get_history(limit: int = 50):
    return {"history": fetch_memory(limit)}


@router.get("/list")
def list_memories():
    return tool_memory_manager("list")


@router.post("/add")
def add_memory(item: MemoryItem):
    return tool_memory_manager("save", key=item.key, value=item.value)


@router.delete("/delete/{key}")
def delete_memory(key: str):
    return tool_memory_manager("delete", key=key)
