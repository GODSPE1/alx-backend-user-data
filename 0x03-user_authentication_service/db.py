#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError, SQLAlchemyError
from user import Base, User
from typing import Dict


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Parameter:
            - email:
            - hashed_password
        Return: return a user object
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs: Dict) -> User:
        """Find a user by email or hashed password"""
        try:
            user = self._session.query(User).filter_by(kwargs).first()
            if user is None:
                raise NoResultFound
            return user
        except NoResultFound as e:
            raise e
        except InvalidRequestError as e:
            raise e

    def update_user(self, user_id: int, **kwargs: Dict) -> None:
        """Locate the user by id, update and commit to database
        Parameter:
            user_id - id of user to update
            **kwargs - key, value pairs of attribute to update

        Raises: raises value error if invalid attribute is passed
        """
        try:
            user = self.find_user_by(id=user_id)
        except NoResultFound:
            raise ValueError(f"User with id {user_id} not found")

        for key, value in kwargs.items():
            if not hasattr(user, key):
                raise ValueError(f"Invalid attribute: {key}")
            setattr(user, key, value)
        try:
            self._session.commit()
        except SQLAlchemyError as e:
            self._session.rollback()
            raise e
