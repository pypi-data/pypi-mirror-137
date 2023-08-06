from typing import Any

from insanic.commands import Command, ArgumentParser
from insanic.utils import load_application

class ServerCommand(Command):
    help = 'Runs application server'

    def add_arguments(self, parser: ArgumentParser) -> None:
        parser.add_argument('-p', help='Server port')

    def execute(self, *args: Any, **kwargs: Any) -> None:
        application = load_application()

        server_config = {
            'host': application.config.APPLICATION_HOST,
            'port': application.config.APPLICATION_PORT,

            'debug': application.config.APPLICATION_DEBUG,
            'auto_reload': application.config.APPLICATION_DEBUG,
            'access_log': application.config.APPLICATION_DEBUG,

            'workers': application.config.APPLICATION_WORKERS,
        }
        application.run(**server_config)
