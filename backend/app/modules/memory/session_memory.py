import json
import os
from datetime import datetime

MEMORY_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 
                           "..", "data", "memory.json")
# Normalize path
MEMORY_FILE = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 
    "..", "..", "data", "memory.json"
))


def save_command(command: str, response: str):
    """Save a command-response pair to persistent memory."""
    entry = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "command": command,
        "response": response
    }

    try:
        _ensure_file()

        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        data.append(entry)

        # Keep only last 500 entries to prevent file bloat
        if len(data) > 500:
            data = data[-500:]

        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    except Exception as e:
        print(f"Memory save error: {e}")


def get_command_history(limit: int = 50) -> list:
    """Get the command history, most recent first."""
    try:
        _ensure_file()

        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)

        return data[-limit:]

    except Exception as e:
        print(f"Memory read error: {e}")
        return []


def get_recent_context(n: int = 5) -> str:
    """Get recent commands as a summary string for AI context."""
    history = get_command_history(n)
    if not history:
        return ""

    lines = []
    for entry in history:
        lines.append(f"User said: {entry['command']} → FRIDAY did: {entry['response']}")

    return "\n".join(lines)


def _ensure_file():
    """Ensure the memory file exists."""
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    if not os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)