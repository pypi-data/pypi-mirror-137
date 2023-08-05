# -*- coding: utf-8 -*-
from calendar import timegm
from datetime import datetime
from enum import Enum
from typing import List, Literal

from pydantic import BaseModel


class TokenState(Enum):
    UNSET = 0
    SET = 1
    MODIFIED = 2


def unix_now():
    return timegm(datetime.utcnow().utctimetuple())


class JWTConfig(BaseModel):
    """
    JWT configuration

    :cvar secret:
        A secret key for JWT encryption
    """
    secret: str
    algorithm: str = "HS256"
    allowed_issuer: List[str] = None
    allowed_audience: str = None

    # following settings must be set to generate JWT access tokens
    cookie_name: str = 'access_token'
    path: str = '/'
    https_only: bool = True
    samesite: Literal['lax', 'strict', 'none'] = 'strict'
    # note: it's None just to work if generation is not used, however to generate cookie it must be set
    domain: str = None
    validity: int = None
    issuer: str = None
    audience: List[str] = None

