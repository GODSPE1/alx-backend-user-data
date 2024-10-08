#!/usr/bin/env python3
"""This module is for authentification usin BasicAuth"""
from api.v1.auth.auth import Auth
import base64
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """returns the Base64 part of the Authorization
    header for a Basic Authentication"""
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """"returns the Base64 part of the Authorization
        header for a Basic Authentication
        """

        if not authorization_header or not\
                isinstance(authorization_header, str):
            return None
        if not authorization_header.startswith("Basic "):
            return None
        else:
            token = authorization_header.find(" ")
            final_token = authorization_header[token + 1:]
            return final_token

    def decode_base64_authorization_header(
                            self, base64_authorization_header: str) -> str:
        """return the decoded Base64 part of the authorization header for
    a Basic Authentication"""
        if not base64_authorization_header or not\
                isinstance(base64_authorization_header, str):
            return None
        try:
             decodede_base64 = base64.b4decode(base64_authorization_header).decode('utf-8')
             print(decodede_base64)
             return decodede_base64
        except Exception:
            return None

    def extract_user_credentials(
            self, decoded_base64_authorization_header: str) -> (str, str):
        """returns the user email and password
        from the Base64 decoded value."""
        if not decoded_base64_authorization_header or\
                not isinstance(decoded_base64_authorization_header, str):
            return (None, None)

        return tuple(decoded_base64_authorization_header.split(":", 1))

    def user_object_from_credentials(self, user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """returns the User instance based on his email and password."""
        if not user_email or not isinstance(user_email, str):
            return None
        if not user_pwd or not isinstance(user_pwd, str):
            return None
        try:
            users = User.search({"email": user_email})
            if not users or users == []:
                return None
            for user in users:
                if user.is_valid_password(user_pwd):
                    return user
            return None
        except Exception:
            return None
       
    def current_user(self, request=None) -> TypeVar('User'):
        """The Purpose of this method is to determine the who
        the current user is based on the incoming request
        """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            token = self.extract_base64_authorization_header(auth_header)
            if token is not None:
                decoded = self.decode_base64_authorization_header(token)
                if decoded is not None:
                    email, password = self.extract_user_credentials(
                        decoded)
                    if email is not None:
                        return self.user_object_from_credentials(
                            email, password)

        return
