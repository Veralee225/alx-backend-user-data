#!/usr/bin/env python3
"""The BasicAuth class inherits from Auth """
from typing import Tuple, TypeVar
from api.v1.auth.auth import Auth
from models.user import User
import base64
import binascii
import re


class BasicAuth(Auth):
    """BasicAuth class """

    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """Get the Base64 part of the Authorization header for a Basic Authentication"""
        if not authorization_header:
            return None
        if not isinstance(authorization_header, str):
            return None
        if not authorization_header.startwith('Basic '):
            return None
        return authorization_header[len('Basic '):]
    