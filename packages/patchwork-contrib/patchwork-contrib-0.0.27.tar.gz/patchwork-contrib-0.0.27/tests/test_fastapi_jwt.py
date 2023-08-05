# -*- coding: utf-8 -*-
import time
from http.cookies import SimpleCookie

import pytest
from async_asgi_testclient import TestClient
from fastapi import FastAPI
from jose import jwt
from starlette.websockets import WebSocket

from patchwork.contrib.fastapi import JWTToken, register_patchwork, Token
from patchwork.contrib.fastapi import JWTConfig


@pytest.mark.asyncio
async def test_jwt_usage():

    config = JWTConfig(
        secret='secret',
        validity=100
    )

    token = JWTToken(config)
    assert not token.is_set
    assert not token.is_modified

    token.set('sub', 'user')
    assert token.is_set
    assert token.is_modified

    raw = token.get()

    restored_token = JWTToken(config, raw)
    assert restored_token.is_set
    assert not restored_token.is_modified

    old_exp = restored_token.exp

    restored_token.update({
        'sub': 'foo'
    })

    assert restored_token.exp == old_exp, "changing token data should not affect expiration time"
    assert restored_token.is_modified

    restored_token.invalidate()
    assert not restored_token.is_set

    assert restored_token.get() is None


@pytest.mark.asyncio
async def test_token_websocket():
    app = FastAPI()

    register_patchwork(app, api_settings={
        'jwt': [{
            'secret': 'topsecret'
        }]
    })

    @app.websocket('/ws')
    async def ws_route(ws: WebSocket, token: JWTToken = Token('access_token')):
        await ws.accept()
        await ws.send_bytes(token.get() or b'')

    async with TestClient(app) as client:
        client.cookie_jar = SimpleCookie()
        token = jwt.encode({
            'sub': "1",
            'exp': time.time() + 300
        }, 'topsecret')
        client.cookie_jar['access_token'] = token

        async with client.websocket_connect('/ws') as ws:
            assert await ws.receive_bytes() == token
