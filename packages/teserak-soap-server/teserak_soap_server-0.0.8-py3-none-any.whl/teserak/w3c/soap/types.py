import enum
import typing
from dataclasses import dataclass, field
from io import BytesIO

R = typing.TypeVar("R")


class SoapVersion(str, enum.Enum):
    VERSION_11 = "1.1"
    VERSION_12 = "1.2"


class XmlNamespace(str, enum.Enum):
    SOAP_11 = "http://schemas.xmlsoap.org/soap/envelope/"
    SOAP_12 = "http://www.w3.org/2003/05/soap-envelope"
    WS_ADDRESSING = "http://www.w3.org/2005/08/addressing"


@dataclass
class SoapRequest:
    parts: dict


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


class SoapUploadFile:
    def __init__(self, filename: str, content_type: str, headers: typing.Any):
        self.filename = filename
        self.content_type = content_type
        self.headers = headers
        self.file = BytesIO()

    async def write(self, data):
        self.file.write(data)

    async def seek(self, offset):
        self.file.seek(offset)

    async def read(self, *args):
        return self.file.read(*args)

    def __len__(self):
        return len(self.file.getvalue())
