#!/usr/bin/env python3
"""This module defines functionn that hashed the password"""
from bcrypt import hashpw, gensalt, checkpw
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from user import User
from uuid import uuid4
from typing import Union


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
                raise ValueError(f"User with email {email} already exists.")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            new_user = self._db.add_user(email, hashed_password)
            return new_user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates Logi Credentials"""
        try:
            user = self._db.find_user_by(email=email)
            return checkpw(password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def create_session(self, email: str) -> str:
        """returns session id as string"""
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id)
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Union[User, None]:
        """return a corresponding user or None"""
        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, session_id: str) -> None:
        """Destroy the session for a user by setting the session id to None"""
        user = self._db.find_user_by(session_id)
        self._db.update_user(user_id, session_id=None)
        return None

    def get_reset_password_token(self, email: str) -> str:
        """
        Generates a password reset token

        Return
            The reset token
        """

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        token = self._generate_uuid()
        self._db.update_user(user.id, reset_token=token)

        return token

    def _generate_uuid() -> str:
        """Generate uuid"""
        return str(uuid4())

    def update_password(self, reset_token: str, password: str) -> None:
        """
        Updates a user's password

        Return
            None
        """

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        hashed_password = self._hash_password(password)

        self._db.update_user(user.id, hashed_password)
        self._db.update_user(user.id, reset_token=None)

    def _hash_password(self, password: str) -> bytes:
        """Return a hashed password using bcrypt"""
        return hashpw(password.encode('utf-8'), gensalt())
