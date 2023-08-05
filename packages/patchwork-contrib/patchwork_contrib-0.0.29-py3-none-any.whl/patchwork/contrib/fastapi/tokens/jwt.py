# -*- coding: utf-8 -*-
import uuid
from types import MappingProxyType
from typing import Mapping, Any, Union

from jose import jwt

from patchwork.contrib.fastapi.tokens.utils import TokenState, unix_now
from patchwork.core.utils import cached_property


class JWTToken:

    _payload: dict

    def __init__(self, config,  raw: str = None):
        self.config = config

        if raw is not None:
            self._decode(raw)
            self.__state = TokenState.SET
        else:
            self._payload = {}
            self.__state = TokenState.UNSET

    @cached_property
    def payload(self) -> Mapping:
        return MappingProxyType(self._payload)

    @property
    def is_set(self):
        return self._state != TokenState.UNSET

    @property
    def is_modified(self):
        return self._state == TokenState.MODIFIED

    @property
    def _state(self):
        return self.__state

    @_state.setter
    def _state(self, value):
        if self.__state == TokenState.UNSET:
            self._init_token()

        self.__state = value

    @property
    def sub(self):
        """
        Subject of the JWT (the user)
        :return:
        """
        return self.payload.get('sub')

    @property
    def exp(self):
        """
        Time after which the JWT expires
        :return:
        """
        return self.payload.get('exp')

    @property
    def iss(self):
        """
        Issuer of the JWT
        :return:
        """
        return self.payload.get('iss')

    @property
    def aud(self):
        """
        Recipient for which the JWT is intended
        :return:
        """
        return self.payload.get('aud')

    @property
    def nbf(self):
        """
        Time before which the JWT must not be accepted for processing
        :return:
        """
        return self.payload.get('nbf')

    @property
    def iat(self):
        """
        Time at which the JWT was issued; can be used to determine age of the JWT
        :return:
        """
        return self.payload.get('iat')

    @property
    def jti(self):
        """
        Unique identifier; can be used to prevent the JWT from being replayed (allows a token to be used only once)
        :return:
        """
        return self.payload.get('jti')

    def get(self) -> Union[str, None]:
        if not self.is_set:
            return None

        assert self.exp is not None, "token validity must be set"

        return jwt.encode(self._payload, self.config.secret, algorithm=self.config.algorithm)

    def update(self, data: dict):
        self._payload.update(data)
        self._state = TokenState.MODIFIED

    def set(self, claim: str, value: Any):
        self._payload[claim] = value
        self._state = TokenState.MODIFIED

    def refresh(self):
        self._payload['iat'] = unix_now()
        self._payload['exp'] = self._payload['iat'] + self.config.validity
        self._state = TokenState.MODIFIED

    def invalidate(self):
        self._payload = {}
        self._state = TokenState.UNSET

    def _init_token(self):
        data = self._payload
        if 'iss' not in data and self.config.issuer is not None:
            data['iss'] = self.config.issuer

        if 'aud' not in data and self.config.audience is not None:
            data['aud'] = self.config.audience

        if 'iat' not in data:
            data['iat'] = unix_now()

        if 'exp' not in data:
            data['exp'] = data['iat'] + self.config.validity

        if 'jti' not in data:
            data['jti'] = str(uuid.uuid4())

    def _decode(self, raw: str = None):

        self._payload = jwt.decode(
            token=raw,
            key=self.config.secret,
            algorithms=[self.config.algorithm],
            audience=self.config.allowed_audience,
            issuer=self.config.allowed_issuer,
            options={
                'require_aud': self.config.allowed_audience is not None,
                'require_iss': self.config.allowed_issuer is not None,
                'require_exp': True
            }
        )


