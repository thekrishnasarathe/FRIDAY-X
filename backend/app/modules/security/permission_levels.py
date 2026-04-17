"""
Permission levels for FRIDAY commands.
Some commands are sensitive (shutdown, email, delete) and require higher auth.
"""

# Permission levels
OPEN = 0        # No auth needed (greetings, time, jokes)
STANDARD = 1    # Basic commands (open apps, search)
ELEVATED = 2    # Sensitive (email, whatsapp, file creation)
ADMIN = 3       # Dangerous (shutdown, restart, delete, lock)

# Command permission mapping
COMMAND_PERMISSIONS = {
    "greeting": OPEN,
    "conversation": OPEN,
    "time_date": OPEN,
    "weather": OPEN,
    "news": OPEN,
    "joke": OPEN,
    "identity": OPEN,

    "browser": STANDARD,
    "application": STANDARD,
    "search": STANDARD,
    "mode": STANDARD,

    "file": ELEVATED,
    "email": ELEVATED,
    "message": ELEVATED,

    "system": ADMIN,
}


def get_required_level(intent: str) -> int:
    """Get the required permission level for a command intent."""
    return COMMAND_PERMISSIONS.get(intent, STANDARD)


def check_permission(intent: str, user_level: int = STANDARD) -> bool:
    """Check if the user has permission to execute this intent."""
    required = get_required_level(intent)
    return user_level >= required


def get_level_name(level: int) -> str:
    """Get the name of a permission level."""
    names = {OPEN: "Open", STANDARD: "Standard", ELEVATED: "Elevated", ADMIN: "Admin"}
    return names.get(level, "Unknown")
