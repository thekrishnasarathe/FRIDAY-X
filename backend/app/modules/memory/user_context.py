import json
import os
from app.utils.logger import log_error

USER_PREFS_FILE = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "..", "data", "user_profiles.json"
))


DEFAULT_PREFS = {
    "name": "Krishna",
    "favorite_apps": [],
    "favorite_sites": [],
    "contacts": {},
    "preferences": {
        "voice_enabled": True,
        "voice_speed": 170,
        "default_mode": "assistant"
    }
}


def get_user_prefs() -> dict:
    """Load user preferences from disk."""
    try:
        _ensure_file()
        with open(USER_PREFS_FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()
            if not content:
                return DEFAULT_PREFS.copy()
            return json.loads(content)
    except Exception as e:
        log_error("get_user_prefs", e)
        return DEFAULT_PREFS.copy()


def save_user_prefs(prefs: dict):
    """Save user preferences to disk."""
    try:
        os.makedirs(os.path.dirname(USER_PREFS_FILE), exist_ok=True)
        with open(USER_PREFS_FILE, "w", encoding="utf-8") as f:
            json.dump(prefs, f, indent=4, ensure_ascii=False)
    except Exception as e:
        log_error("save_user_prefs", e)


def get_user_name() -> str:
    """Get the user's name."""
    prefs = get_user_prefs()
    return prefs.get("name", "User")


def set_user_name(name: str) -> str:
    """Set the user's name."""
    prefs = get_user_prefs()
    prefs["name"] = name
    save_user_prefs(prefs)
    return f"Got it. I'll call you {name} from now on."


def add_contact(name: str, phone: str) -> str:
    """Add a contact to the user's contact book."""
    prefs = get_user_prefs()
    prefs.setdefault("contacts", {})[name.lower()] = phone
    save_user_prefs(prefs)
    return f"Contact '{name}' saved with number {phone}."


def get_contacts() -> dict:
    """Get all saved contacts."""
    prefs = get_user_prefs()
    return prefs.get("contacts", {})


def _ensure_file():
    """Ensure the user profiles file exists."""
    os.makedirs(os.path.dirname(USER_PREFS_FILE), exist_ok=True)
    if not os.path.exists(USER_PREFS_FILE):
        with open(USER_PREFS_FILE, "w", encoding="utf-8") as f:
            json.dump(DEFAULT_PREFS, f, indent=4)
