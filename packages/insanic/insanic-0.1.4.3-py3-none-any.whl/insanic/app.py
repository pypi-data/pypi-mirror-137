from __future__ import annotations

import importlib
from asyncio import AbstractEventLoop
from typing import Any

from sanic import Sanic

from insanic.config import DEFAULT_CONFIG
from insanic.db import init_db_connection, close_db_connection

class Application(Sanic):
    def __init__(self, *args: Any, **kwargs: Any):
        # @TODO: Implement custom error handler
        # @TODO: Implement proper logging
        # @TODO: Implement custom Request class
        kwargs['strict_slashes'] = True
        super().__init__(*args, **kwargs)

        self.load_configuration()

        self.register_listener(self.boot, 'before_server_start')
        self.register_listener(self.shutdown, 'after_server_stop')

    def load_configuration(self) -> None:
        # Default configuration
        self.config.update_config(DEFAULT_CONFIG)

        # Application configuration
        try:
            application_config = importlib.import_module('config', package='src') # importing src/config.py
            self.config.update_config(application_config)
        except ModuleNotFoundError as _error:
            pass  # @TODO: Log that application is using default config

        # Applying ENV config
        self.config.load_environment_vars(prefix='INSANIC_')

    async def boot(self, _application: Application, _loop: AbstractEventLoop) -> None: # pylint: disable=no-self-use
        await init_db_connection()

    async def shutdown(self, _application: Application, _loop: AbstractEventLoop) -> None: # pylint: disable=no-self-use
        await close_db_connection()
