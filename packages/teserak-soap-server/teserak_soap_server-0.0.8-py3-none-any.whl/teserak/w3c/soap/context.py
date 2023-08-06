import contextvars
import inspect
import typing
from contextlib import contextmanager
from functools import wraps

from teserak.w3c.soap.types import SoapRequest

SOAP_CONTEXT = contextvars.ContextVar("context")


T = typing.TypeVar("T")


@contextmanager
def set_soap_context(ctx: SoapRequest):
    token = SOAP_CONTEXT.set(ctx)
    try:
        yield token
    finally:
        SOAP_CONTEXT.reset(token)


def get_soap_context() -> SoapRequest:
    return SOAP_CONTEXT.get()


def soap_context(func):
    @wraps(func)
    def wrapper(*args, **kw):
        parameters = inspect.signature(func).parameters
        for param, resolver in parameters.items():
            try:
                kw[param] = injector.resolve(resolver.annotation)
            except KeyError:
                pass
        return func(*args, **kw)

    return wrapper


class Injector:
    registry: typing.Dict[typing.Type[T], typing.Callable[[], T]] = {}

    def register(self, data_type: typing.Type[T], value: typing.Callable[[], T]):
        self.registry[data_type] = value

    def resolve(self, data_type: typing.Type[T]) -> T:
        resolver = self.registry[data_type]
        return resolver()


injector = Injector()
injector.register(SoapRequest, get_soap_context)
