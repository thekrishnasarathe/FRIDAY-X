import hashlib
from app.modules.security.auth_manager import _load_auth


def verify_passphrase(passphrase: str) -> bool:
    """Verify a passphrase against stored hash."""
    auth = _load_auth()
    stored_hash = auth.get("passphrase_hash", "")
    if not stored_hash:
        return True  # No passphrase set = open access

    return hashlib.sha256(passphrase.encode()).hexdigest() == stored_hash


def is_passphrase_set() -> bool:
    """Check if a passphrase has been set."""
    auth = _load_auth()
    return bool(auth.get("passphrase_hash"))
