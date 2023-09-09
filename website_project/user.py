from typing import Optional

from flask_login import UserMixin
from flask_login.mixins import AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from abc import ABC, abstractmethod


class User(ABC):
    @property
    @abstractmethod
    def username(self) -> str:
        """User username."""

    @property
    @abstractmethod
    def password(self) -> str:
        """User password."""

    def get_id(self):
        """Returns username as user unique id."""
        return self.username

    def has_password(self, password: str) -> bool:
        """Verifies user password."""
        return check_password_hash(self.password, password)


class RegisteredUser(User, UserMixin):
    def __init__(self, username: str, password: str) -> None:
        self._username = username
        self._password = generate_password_hash(password, "sha256")

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password


class GuestUser(User, AnonymousUserMixin):
    def __init__(self):
      self._username = "guest"
      self._password = ""

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password


user_collection = [RegisteredUser("root", "root")]


# TODO: Create separate query object for database e.g.
#   db.user.find_by_username
#   db.user.register
#   db.user.exists
def find_user_by_username(username: str) -> Optional[User]:
    """Find user by username."""
    resp = None
    for user in user_collection:
        resp = user if user.username == username else None

    return resp


def register_user(user: User) -> None:
    """Registers new user."""
    user_collection.append(user)


def user_exists(user: User) -> bool:
    """Returns info if given user already exists."""
    return bool(find_user_by_username(user.username))
