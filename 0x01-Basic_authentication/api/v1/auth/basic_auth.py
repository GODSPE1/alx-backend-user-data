#!/usr/bin/env python3
"""This module is for authentification usin BasicAuth"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """"""
    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        if authorization_header is None:
            return None
        if type(authorization_header) != str:
            return None
        if not  authorization_header.startswith("Basic "):
            return None
        else:
            token = authorization_header.find(" ")
            final_token = authorization_header[token + 1:]
            return final_token
