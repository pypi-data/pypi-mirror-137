import inspect
from collections.abc import Callable
from typing import Any

from sanic.blueprints import Blueprint as SanicBlueprint

__all__ = (
    'Blueprint',
)

# Wrapper for class method routes.
# Inits class instance and executes method
# @TODO: Implement `before_method` for class based views
def wrap_class_handler(view_class: type, handler: Callable) -> Callable:
    def dispatcher(*args: Any, **kwargs: Any) -> Any:
        view = view_class()
        return handler(view, *args, **kwargs)

    # @TODO: Ugly hack and I don't remember for what!
    dispatcher.target = handler  # type: ignore[attr-defined]
    return dispatcher

class Blueprint(SanicBlueprint):  # pylint: disable=abstract-method
    def route_method(self, handler: Callable, *args: Any, http_method: str | None = None, **kwargs: Any) -> None:
        # Support for class methods routes like `ClassName.MethodName`
        # "staticmethod" stlye but with class initialization (see `wrap_class_handler`)
        if inspect.signature(handler).parameters.get('self'):
            handler_module = inspect.getmodule(handler)
            handler_class_name = handler.__qualname__.split('.<locals>', 1)[0].rsplit('.', 1)[0]
            handler_class = getattr(handler_module, handler_class_name)
            handler = wrap_class_handler(handler_class, handler)

        http_method = http_method or 'GET'
        kwargs['methods'] = [http_method]
        self.route(*args, **kwargs)(handler)

    def route_get(self, *args: Any, **kwargs: Any) -> None:
        kwargs['http_method'] = 'GET'
        self.route_method(*args, **kwargs)
