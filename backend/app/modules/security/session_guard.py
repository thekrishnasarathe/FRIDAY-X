import json
import os
from datetime import datetime
from app.utils.logger import log_error

SESSION_FILE = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "data", "sessions.json"
))

_current_session = {
    "session_id": None,
    "started_at": None,
    "command_count": 0,
    "is_active": False,
}


def start_session() -> str:
    """Start a new assistant session."""
    global _current_session
    _current_session = {
        "session_id": datetime.now().strftime("%Y%m%d_%H%M%S"),
        "started_at": datetime.now().isoformat(),
        "command_count": 0,
        "is_active": True,
    }
    _save_session()
    return f"Session {_current_session['session_id']} started."


def end_session() -> str:
    """End the current session."""
    global _current_session
    if not _current_session.get("is_active"):
        return "No active session."

    _current_session["is_active"] = False
    _current_session["ended_at"] = datetime.now().isoformat()
    _save_session()

    session_id = _current_session["session_id"]
    cmd_count = _current_session["command_count"]
    return f"Session {session_id} ended. Total commands: {cmd_count}."


def increment_command():
    """Track a command in the current session."""
    global _current_session
    _current_session["command_count"] = _current_session.get("command_count", 0) + 1


def get_session_info() -> str:
    """Get current session info."""
    if not _current_session.get("is_active"):
        return "No active session."

    return (
        f"Session: {_current_session['session_id']}\n"
        f"  Started: {_current_session['started_at']}\n"
        f"  Commands: {_current_session['command_count']}\n"
        f"  Status: Active"
    )


def _save_session():
    """Save session data."""
    try:
        os.makedirs(os.path.dirname(SESSION_FILE), exist_ok=True)

        sessions = []
        if os.path.exists(SESSION_FILE):
            with open(SESSION_FILE, "r") as f:
                content = f.read().strip()
                if content:
                    sessions = json.loads(content)

        # Update or append
        updated = False
        for i, s in enumerate(sessions):
            if s.get("session_id") == _current_session.get("session_id"):
                sessions[i] = _current_session
                updated = True
                break
        if not updated:
            sessions.append(_current_session)

        # Keep last 50 sessions
        sessions = sessions[-50:]

        with open(SESSION_FILE, "w") as f:
            json.dump(sessions, f, indent=4, default=str)

    except Exception as e:
        log_error("save_session", e)
