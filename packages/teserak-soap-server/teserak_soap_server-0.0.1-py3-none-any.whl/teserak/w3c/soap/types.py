import typing
from dataclasses import dataclass, field

R = typing.TypeVar("R")


class SoapRequest(typing.Generic[R]):
    input: R

    def get_input_type(cls):
        return cls.__orig_bases__[0]


@dataclass
class SoapRequestInput:
    action_name: str
    body: str
    parts: typing.Dict[str, typing.Any] = field(default_factory=dict)


@dataclass
class MultipartResponse:
    body: str
    parts: typing.Dict[str, typing.Any]
