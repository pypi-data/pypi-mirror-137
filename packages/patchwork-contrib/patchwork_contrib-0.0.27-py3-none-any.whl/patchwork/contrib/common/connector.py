# -*- coding: utf-8 -*-

from typing import Literal, Union, Type, Any, TypeVar

import aiohttp
from patchwork.core import Component
from pydantic import BaseModel, Protocol


class ConnectorError(Exception):
    pass


class ConnectorBadData(ConnectorError):
    def __init__(self, response):
        self.response = response


class ConnectorTooManyAttempts(ConnectorError):
    def __init__(self, retry_after: int):
        self.retry_after = retry_after


T = TypeVar('T')


class HTTPConnector(Component):

    class Config(Component.Config):
        timeout: int = 60
        max_conn_limit: int = 100
        user_agent: str = None
        endpoint_url: str

    session: aiohttp.ClientSession

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._timeout = aiohttp.ClientTimeout(total=self.settings.timeout)

    async def _start(self) -> bool:
        connector = aiohttp.TCPConnector(limit=self.settings.max_conn_limit)

        headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }
        if self.settings.user_agent:
            headers['user-agent'] = self.settings.user_agent

        self.session = aiohttp.ClientSession(
            connector=connector,
            timeout=self._timeout,
            headers=headers,
            base_url=self.settings.endpoint_url,
            raise_for_status=False,
            cookie_jar=aiohttp.DummyCookieJar()     # do not store any cookies for inter-services communication
        )
        return True

    async def _stop(self) -> bool:
        await self.session.close()
        return False

    async def send(
            self,
            method: Literal['get', 'post', 'put', 'delete'],
            url: str = '/',
            *,
            payload: BaseModel = None,
            response_model: Type[T] = Any,
            **options,
    ) -> Union[T, None]:

        if payload is not None:
            # use pydantic JSON encoder instead of aiohttp, as pydantic one supports all types
            # supported by pydantic
            payload = payload.json().encode('utf-8')

        if method == 'get':
            assert payload is None, \
                'payload forbidden on GET method'
            response = await self.session.get(url, **options)
        elif method == 'post':
            response = await self.session.post(url, data=payload, **options)
        elif method == 'put':
            response = await self.session.put(url, data=payload, **options)
        elif method == 'patch':
            response = await self.session.patch(url, data=payload, **options)
        elif method == 'delete':
            assert payload is None, \
                "payload is forbidden on DELETE method"
            response = await self.session.delete(url, **options)
        else:
            raise NotImplementedError('not supported HTTP method')

        try:
            return await self._handle_response(response, response_model)
        finally:
            if not response.closed:
                response.close()

    async def _handle_response(
            self,
            response: aiohttp.ClientResponse,
            response_model: Union[Type[BaseModel], Any, None]
    ) -> Union[BaseModel, None]:

        if response.status in {200, 201, 202}:
            if response_model is Any:
                return None
            elif response_model is None:
                if response.content_length is not None:
                    raise ValueError('empty response expected')
                return None

            if not response.content_length:
                raise ValueError('missing data')

            data = await response.read()
            return response_model.parse_raw(data, proto=Protocol.json)
        elif response.status == 204:
            if response_model is not Any and response_model is not None:
                raise ValueError('response data expected, but 204 No Content response received')
            return None
        elif response.status == 422:
            raise ConnectorBadData(await response.json())
        elif response.status == 429:
            raise ConnectorTooManyAttempts(int(response.headers.get('Retry-After', '0')))
        else:
            raise ConnectorError()
