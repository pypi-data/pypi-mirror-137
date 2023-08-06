import enum
import typing
from dataclasses import dataclass, field

R = typing.TypeVar("R")


class SoapVersion(str, enum.Enum):
    VERSION_11 = '1.1'
    VERSION_12 = '1.2'


class SoapNamespace(str, enum.Enum):
    SOAP_VERSION_11 = 'http://schemas.xmlsoap.org/soap/envelope/'
    SOAP_VERSION_12 = 'http://www.w3.org/2003/05/soap-envelope'
    WS_ADDRESSING = 'http://www.w3.org/2005/08/addressing'


class SoapRequest(typing.Generic[R]):
    input: R

    def get_input_type(cls):
        return cls.__orig_bases__[0]


@dataclass
class SoapRequestInput:
    action_name: str
    body: str
    soap_version: str
    parts: typing.Dict[str, typing.Any] = field(default_factory=dict)


@dataclass
class MultipartResponse:
    body: str
    parts: typing.Dict[str, typing.Any]
