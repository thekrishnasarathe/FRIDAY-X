from app.modules.memory.session_memory import get_command_history


def fetch_memory(limit: int = 50):
    """Fetch command history from memory."""
    return get_command_history(limit)