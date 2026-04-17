import re


def is_valid_email(email: str) -> bool:
    """Check if a string looks like a valid email address."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def is_valid_phone(phone: str) -> bool:
    """Check if a string looks like a valid phone number (with country code)."""
    pattern = r'^\+\d{10,15}$'
    cleaned = re.sub(r'[\s\-()]', '', phone)
    return bool(re.match(pattern, cleaned))


def is_valid_filename(name: str) -> bool:
    """Check if a filename is safe."""
    invalid_chars = r'[<>:"/\\|?*]'
    if not name or len(name) > 255:
        return False
    return not bool(re.search(invalid_chars, name))
