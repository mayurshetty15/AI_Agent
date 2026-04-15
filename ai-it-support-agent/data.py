"""In-memory database for user storage."""

from typing import Dict, Optional

# In-memory user storage: email -> password
users_db: Dict[str, str] = {
    "admin": "admin",
    "john@company.com": "secure123",
}

# Session storage (simple in-memory auth)
sessions: Dict[str, str] = {}


def get_user(email: str) -> Optional[str]:
    """Get user password by email. Returns None if user not found."""
    return users_db.get(email)


def create_user(email: str, password: str) -> bool:
    """Create a new user. Returns True if successful, False if already exists."""
    if email in users_db:
        return False
    users_db[email] = password
    return True


def user_exists(email: str) -> bool:
    """Check if user exists."""
    return email in users_db


def reset_password(email: str, new_password: str = "default123") -> bool:
    """Reset user password. Returns True if successful, False if user not found."""
    if email not in users_db:
        return False
    users_db[email] = new_password
    return True


def list_all_users() -> Dict[str, str]:
    """Get all users (for debugging)."""
    return users_db.copy()
