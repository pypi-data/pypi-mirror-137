from argparse import ArgumentParser
from typing import Any

class Command:
    help: str | None = None
    parser: ArgumentParser = ArgumentParser()

    def add_arguments(self, parser: ArgumentParser) -> None:
        pass

    def execute(self, *args: Any, **kwargs: Any) -> None:
        raise NotImplementedError()
