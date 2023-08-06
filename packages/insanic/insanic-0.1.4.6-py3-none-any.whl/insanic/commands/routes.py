from typing import Any

from insanic.commands import Command
from insanic.utils import load_application

class RoutesCommand(Command):
    help = 'Prints all registered routes'

    def execute(self, *args: Any, **kwargs: Any) -> None:
        application = load_application()

        for route in application.router.routes_all.values():
            print(route.uri)
