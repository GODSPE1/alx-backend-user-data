#!/usr/bin/env python3
"""This module define the Session Authentication"""
from api.v1.auth.auth import Auth
import uuid
from models.user import User


class SessionAuth(Auth):
    """Authenticate a user using the sassion authentication"""

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Generates a session ID for the user"""
        if not user_id or not isinstance(user_id, str):
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """This Function returs a user ID Based on the session ID
        Parameter:
            -session_id: the session id for a user
        Return:
            returs a user ID based on the session ID
        """
        if not session_id or not isinstance(session_id, str):
            return None

        user_id = self.user_id_by_session_id.get(session_id)
        return user_id

    def current_user(self, request=None):
        """Fetch an istance value based on a cookie value"""

        if request is not None:
            # retrieves the session ID from the request's cookies
            extracted_session_id = self.session_cookie(request)

            # retreives user ID associated with that session ID
            user_id = self.user_id_by_session_id(extracted_session_id)

            # fetches the user from the database using the user ID
            user = User.get(user_id)

            return user

        return None
