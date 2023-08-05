# -*- coding: utf-8 -*-
from typing import Union, Type

from fastapi import Depends, HTTPException
from jose import JWTError
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request
from starlette.websockets import WebSocket

from patchwork.core import AsyncPublisher
from .settings import is_tortoise_installed
from .tokens.jwt import JWTToken


class PublisherWrapper:

    def __init__(self):
        self._publisher = None

    def __call__(self) -> AsyncPublisher:
        from .settings import settings
        if settings.publisher is None:
            raise RuntimeError("unable to use publisher as it's not configured")

        if self._publisher is None:
            self._publisher = settings.publisher.instantiate()
        return self._publisher


get_publisher = PublisherWrapper()


def Publisher():
    return Depends(get_publisher)


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
)


def get_token(name: str, optional: bool = False):
    def _get(request: Request = None, websocket: WebSocket = None):
        request = request or websocket
        try:
            token = request['token'][name]
        except KeyError:
            raise credentials_exception

        if not token.is_set and not optional:
            raise credentials_exception

        return token

    return _get


def Token(name: str, *, optional: bool = False):
    return Depends(get_token(name, optional))


def current_user_id(token_name: str, *, optional: bool = False):
    async def _get(token: JWTToken = Token(token_name, optional=optional)) -> Union[int, None]:
        if not token.is_set:
            if optional:
                return None
            else:
                raise credentials_exception

        try:
            user_id = token.sub
            if user_id is None:
                if not optional:
                    raise credentials_exception
                return None
            else:
                return int(user_id)
        except (JWTError, TypeError):
            raise credentials_exception

    return _get


def CurrentUserId(*, optional: bool = False, token_name: str = 'access_token'):
    return Depends(current_user_id(token_name, optional=optional))


if is_tortoise_installed:
    from tortoise.exceptions import DoesNotExist

    def current_user(model: Type[BaseModel] = None, *, optional: bool = False, token_name: str = 'access_token'):

        async def _get(cuid: Union[int, None] = CurrentUserId(token_name=token_name, optional=optional)):
            nonlocal model

            if model is None:
                from .settings import settings
                model = settings.user_model.type_

            if cuid is None:
                if optional:
                    return None
                else:
                    raise credentials_exception

            try:
                return await model.get(pk=cuid)
            except DoesNotExist:
                if optional:
                    return None
                else:
                    raise credentials_exception

        return _get

else:
    def current_user(*args, **kwargs):
        raise RuntimeError('no supported ORM installed')


def CurrentUser(*, optional: bool = False, token_name: str = 'access_token', model: Type[BaseModel] = None):
    return Depends(current_user(model, optional=optional, token_name=token_name))
