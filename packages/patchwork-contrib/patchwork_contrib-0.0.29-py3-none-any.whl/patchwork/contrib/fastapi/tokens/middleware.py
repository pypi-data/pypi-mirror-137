# -*- coding: utf-8 -*-
from types import MappingProxyType
from typing import List, Union

from jose import JWTError
from starlette.datastructures import MutableHeaders
from starlette.requests import HTTPConnection
from starlette.types import ASGIApp, Scope, Receive, Send, Message

from patchwork.contrib.fastapi.tokens.jwt import JWTToken
from patchwork.contrib.fastapi.tokens.utils import unix_now, JWTConfig


class AccessTokenMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        config: Union[JWTConfig, List[JWTConfig]]
    ) -> None:
        self.app = app
        if not isinstance(config, list):
            config = [config]

        self._tokens = {
            conf.cookie_name: conf for conf in config
        }

    def _set_token(self, token: JWTToken, headers: MutableHeaders):
        if not token.is_set:
            header_value = f"{token.config.cookie_name}=null; " \
                           f"path={token.config.path}; " \
                           f"expires=Thu, 01 Jan 1970 00:00:00 GMT; " \
                           f"max-age=0; " \
                           f"httponly; " \
                           f"{'secure; ' if token.config.https_only else ''}" \
                           f"samesite={token.config.samesite.lower()}; " \
                           f"domain={token.config.domain}"
            headers.append("Set-Cookie", header_value)
        elif token.is_modified:
            header_value = f"{token.config.cookie_name}={token.get()}; " \
                           f"path={token.config.path}; " \
                           f"max-age={max(int(token.exp - unix_now()), 0)}; " \
                           f"httponly; " \
                           f"{'secure; ' if token.config.https_only else ''}" \
                           f"samesite={token.config.samesite.lower()}; " \
                           f"domain={token.config.domain}"

            headers.append("Set-Cookie", header_value)

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        connection = HTTPConnection(scope)
        tokens = {}

        for name, config in self._tokens.items():
            if name not in connection.cookies:
                tokens[name] = JWTToken(config)
                continue

            data = connection.cookies[name]
            try:
                tokens[name] = JWTToken(config, data)
            except JWTError as e:
                tokens[name] = JWTToken(config)

        scope["token"] = MappingProxyType(tokens)

        async def send_wrapper(message: Message) -> None:
            if message["type"] == "http.response.start":

                headers = MutableHeaders(scope=message)
                for name, token in tokens.items():
                    if not token.is_set and name not in connection.cookies:
                        # if token was not set and still is unset, do not set a cookie
                        continue
                    self._set_token(token, headers)

            await send(message)

        await self.app(scope, receive, send_wrapper)
