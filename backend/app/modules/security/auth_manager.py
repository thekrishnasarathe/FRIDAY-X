import json
import os
import hashlib
from datetime import datetime
from app.utils.logger import log_error

AUTH_FILE = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "data", "auth.json"
))

DEFAULT_AUTH = {
    "passphrase_hash": "",
    "is_locked": False,
    "failed_attempts": 0,
    "last_login": None,
}


def _load_auth() -> dict:
    os.makedirs(os.path.dirname(AUTH_FILE), exist_ok=True)
    if not os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "w") as f:
            json.dump(DEFAULT_AUTH, f, indent=4)
        return DEFAULT_AUTH.copy()
    with open(AUTH_FILE, "r") as f:
        return json.load(f)


def _save_auth(data: dict):
    with open(AUTH_FILE, "w") as f:
        json.dump(data, f, indent=4, default=str)


def is_authenticated() -> bool:
    """Check if the system is unlocked."""
    auth = _load_auth()
    return not auth.get("is_locked", False)


def lock_assistant() -> str:
    """Lock the assistant (requires passphrase to unlock)."""
    auth = _load_auth()
    if not auth.get("passphrase_hash"):
        return "Set a passphrase first with the security setup command."
    auth["is_locked"] = True
    _save_auth(auth)
    return "FRIDAY is now locked. Use your passphrase to unlock."


def unlock_assistant(passphrase: str) -> str:
    """Unlock the assistant with a passphrase."""
    auth = _load_auth()
    if not auth.get("is_locked"):
        return "FRIDAY is already unlocked."

    hashed = hashlib.sha256(passphrase.encode()).hexdigest()
    if hashed == auth.get("passphrase_hash"):
        auth["is_locked"] = False
        auth["failed_attempts"] = 0
        auth["last_login"] = datetime.now().isoformat()
        _save_auth(auth)
        return "Welcome back, Boss. FRIDAY unlocked."

    auth["failed_attempts"] = auth.get("failed_attempts", 0) + 1
    _save_auth(auth)
    return f"Wrong passphrase. Attempts: {auth['failed_attempts']}"


def set_passphrase(passphrase: str) -> str:
    """Set or update the security passphrase."""
    if len(passphrase) < 4:
        return "Passphrase too short. Use at least 4 characters."

    auth = _load_auth()
    auth["passphrase_hash"] = hashlib.sha256(passphrase.encode()).hexdigest()
    _save_auth(auth)
    return "Security passphrase set. Remember it — you'll need it to unlock FRIDAY."


def get_security_status() -> str:
    """Get current security status."""
    auth = _load_auth()
    locked = "LOCKED" if auth.get("is_locked") else "UNLOCKED"
    has_pass = "Yes" if auth.get("passphrase_hash") else "No"
    last = auth.get("last_login", "Never")
    return (
        f"Security Status:\n"
        f"  State: {locked}\n"
        f"  Passphrase set: {has_pass}\n"
        f"  Last login: {last}\n"
        f"  Failed attempts: {auth.get('failed_attempts', 0)}"
    )
