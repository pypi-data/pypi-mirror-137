# -*- coding: utf-8 -*-
from typing import Any, Type, Mapping, List

from fastapi import FastAPI
from pydantic import BaseModel, root_validator

from patchwork.contrib.fastapi.tokens.utils import JWTConfig
from patchwork.core.config import PublisherConfig
from patchwork.core.typing import ClassPath

try:
    from tortoise import models
except ImportError:
    is_tortoise_installed = False
else:
    is_tortoise_installed = True


class PatchworkFastAPISettings(BaseModel):
    """
    Settings for FastAPI and Patchwork integration

    :cvar publisher:
        Optional config for publisher
    :cvar jwt:
        Optional config for JWT
    :cvar user_model:
        Optional path to user model class which must be a Tortoise ORM model
    """

    publisher: PublisherConfig = None

    jwt: List[JWTConfig] = None

    if is_tortoise_installed:
        user_model: ClassPath[Type[models.Model]] = None
    else:
        user_model: Any = None

    @root_validator(pre=True)
    def check_installed_deps(cls, values):
        if 'user_model' in values:
            assert is_tortoise_installed, \
                "can't use `user_model` option without Tortoise ORM installed"

        return values


settings: PatchworkFastAPISettings


def register_patchwork(app: FastAPI, api_settings: Mapping):
    api_settings = PatchworkFastAPISettings(**api_settings)
    global settings
    settings = api_settings

    if settings.publisher is not None:
        from patchwork.contrib.fastapi.dependencies import get_publisher
        publisher = get_publisher()
        app.on_event('startup')(publisher.run)
        app.on_event('shutdown')(publisher.terminate)

    if settings.jwt is not None:
        from patchwork.contrib.fastapi.tokens.middleware import AccessTokenMiddleware
        app.add_middleware(
            AccessTokenMiddleware,
            config=settings.jwt
        )
