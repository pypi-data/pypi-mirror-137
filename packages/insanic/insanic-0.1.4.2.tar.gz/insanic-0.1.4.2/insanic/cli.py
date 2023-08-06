import os
import sys
from inspect import iscoroutinefunction
from typing import Any

from insanic.commands import Command, ArgumentParser
from insanic.commands.routes import RoutesCommand
from insanic.commands.server import ServerCommand
from insanic.utils import application_context, run_async

def load_commands() -> dict[str, Command]:
    return {
        'routes': RoutesCommand(),
        'server': ServerCommand(),
    }

async def execute_async_command(command: Command, *args: Any, **kwargs: Any) -> None:
    async with application_context():
        await command.execute(*args, **kwargs)  # type: ignore[func-returns-value]

def execute() -> None:
    # Adding `./src` into sys path to be able to import relative modules
    app_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'src')
    sys.path = [app_path] + sys.path

    parser = ArgumentParser(prog='Insanic CLI')
    subparsers = parser.add_subparsers(dest='command_name')

    commands = load_commands()

    # @TODO: Sort commands
    for name, command in commands.items():
        subparser = subparsers.add_parser(name, help=command.help)
        command.add_arguments(subparser)

    cli_args = parser.parse_args().__dict__

    command_name = cli_args.pop('command_name', None)
    if not command_name:
        parser.print_help()
        sys.exit()

    # @TODO: Handle error
    command = commands[command_name]

    # Async commands will create a loop
    # and "boot up" application with all initializers
    # Sync command will run in a "cold" mode
    if iscoroutinefunction(command.execute):
        run_async(execute_async_command(command, **cli_args))
    else:
        command.execute(**cli_args)
