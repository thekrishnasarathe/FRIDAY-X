import time
import random
from fastapi import APIRouter
from app.core.command_router import route_command
from app.core.agent_tools import tool_system_diagnostics

router = APIRouter()


@router.get("/execute")
def execute_command(command: str):
    result = route_command(command)
    if not result:
        result = "Command acknowledged."
    return {"command": command, "result": result}


@router.get("/telemetry")
def get_telemetry():
    """Live telemetry payload for HUD radial gauges and sparklines."""
    data = tool_system_diagnostics()
    cpu_val = data["cpu"]
    ram_val = data["ram"]
    lat_val = data["latency_ms"]

    # Generate smooth 8-point mini sparkline trend
    cpu_spark = [max(10, min(95, int(cpu_val + random.uniform(-6, 6)))) for _ in range(8)]
    ram_spark = [max(20, min(90, int(ram_val + random.uniform(-2, 2)))) for _ in range(8)]
    lat_spark = [max(5, min(40, int(lat_val + random.uniform(-3, 3)))) for _ in range(8)]

    return {
        "status": "online",
        "cpu": cpu_val,
        "ram": ram_val,
        "latency": lat_val,
        "sparklines": {
            "cpu": cpu_spark,
            "ram": ram_spark,
            "latency": lat_spark
        },
        "summary": data["summary"]
    }
