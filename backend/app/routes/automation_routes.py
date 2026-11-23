from fastapi import APIRouter
from app.core.command_router import route_command

router = APIRouter()

@router.get("/execute")
def execute_command(command: str):
    result = route_command(command)
    if not result:
        result = "Command acknowledged."
    return {"command": command, "result": result}