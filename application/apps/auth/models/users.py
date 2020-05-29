"""User class for applications"""

from passlib.apps import custom_app_context

from apps import database
from src.config import table_prefix
from sqlalchemy.ext.hybrid import hybrid_property
from hashlib import sha256

class User(database.Model):
    """User Model"""
    __tablename__ = f'{table_prefix}_users'

    id = database.Column(database.Integer)
    username = database.Column(database.String(32), primary_key=True, index=True)
    _password = database.Column(database.String(64))
    active = database.Column(database.Boolean)
    authenticated = database.Column(database.Boolean)

    @hybrid_property
    def password(self):
        return self.password

    @password.setter
    def password(self, password: str) -> None:
        """
        Hash the password
        :param password: password to hash
        """
        self._password = sha256(password.encode()).hexdigest()

    def verify_password(self, password: str) -> bool:
        """
        Verify the password
        :param password: password to verify with the user password
        :return: Are they equal or not
        """
        return sha256(password.encode()).hexdigest() == self.password
