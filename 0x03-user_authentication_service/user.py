#!/usr/bin/env python3
"""This is a User model using declarative mapping"""

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import MetaData

metadata = MetaData()
Base = declarative_base(metadata=metadata)


class User(Base):
    """This is the Userclass that inherits from the Base declarative class"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250))
    hashed_password = Column(String(250))
    session_id = Column(String(250))
    reset_token = Column(String(250))
