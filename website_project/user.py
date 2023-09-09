from flask_login import UserMixin
from flask_login.mixins import AnonymousUserMixin

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


class RegisteredUser(User, UserMixin):
    def __init__(self, username: str, password: str) -> None:
        self._username = username
        self._password = password

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
