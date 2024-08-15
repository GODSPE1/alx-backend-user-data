#!/usr/bin/env python3
"""This module defines functionn that hashed the password"""
from bcrypt import hashpw, gensalt
from db import DB
from sqlalchemy.orm.exc import NoResultFound


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        """Function initializer"""
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """
        Parameters:
            email: The users email
            password: The users password
        Return:
            the created object user
        Raises:
            ValueError: if a user with the same email already exist
        """

        try:
            existing_user = self._db.find_user_by(email=email)
            if existing_user:
                raise ValueError
        except NoResultFound:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def _hash_password(self, password: str) -> bytes:
        """Return a hashed password using bcryt"""
        hashed_password = password.encode('utf-8')
        salt_password = gensalt()
        return hashpw(hashed_password, salt_password)
