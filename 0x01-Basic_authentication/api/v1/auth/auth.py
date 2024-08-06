#!/usr/bin/env python3
"""
Auth module for the API
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class for managing API authentication"""
    
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if authentication is required for a given path.

        Args:
            path (str): The path to check.
            excluded_paths (List[str]): A list of paths that do not require authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None:
            return True
        if excluded_paths is None or not excluded_paths:
            return True
        
        # Ensure path ends with a slash for comparison
        if not path.endswith('/'):
            path += '/'
        
        # Check if the path is in excluded_paths
        for excluded_path in excluded_paths:
            if excluded_path.endswith('/') and path == excluded_path:
                return False
        
        return True

    def authorization_header(self, request=None) -> str:
        """
        Returns the value of the Authorization header from the request.
        Currently returns None.

        Args:
            request: The Flask request object.

        Returns:
            str: None (placeholder).
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns the current user from the request.
        Currently returns None.

        Args:
            request: The Flask request object.

        Returns:
            TypeVar('User'): None (placeholder).
        """
        return None
