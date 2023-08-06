from multipart.multipart import parse_options_header
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response
from teserak.w3c.soap.types import SoapRequest, SoapRequestInput
from teserak.w3c.soap.utils import parse_action


def build_soap_request(input_cls, request_input):
    result = parse_action(request_input.body, input_cls)
    soap_request = SoapRequest[input_cls]()
    soap_request.input = result.body.input
    return soap_request


async def call_action(service, request_input: SoapRequestInput):
    action = service.get_action(request_input.action_name)

    input_cls = action.input
    output_cls = action.output
    action_handler = action.handler

    soap_request = build_soap_request(input_cls, request_input)
    result = await action_handler(soap_request)
    return output_cls(body=action.output_body_class(result))


async def render_response(response_instance):
    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    response_content = serializer.render(response_instance)
    return response_content


class SoapParser:
    namespace = None

    def get_action_name(self, headers, options) -> str:
        ...

    async def get_body(self, stream) -> str:
        body = b""
        async for chunk in stream:
            body += chunk
        return body.decode("utf-8")

    async def parse(self, headers: dict, stream):
        content_type_header = headers["content-type"]
        content_type, options = parse_options_header(content_type_header)
        action_name = self.get_action_name(headers, options)
        if b"boundary" in options:
            raise NotImplementedError()
        else:
            body = await self.get_body(stream)
            parts = {}
        return SoapRequestInput(action_name=action_name, body=body, parts=parts)


class SoapParser11(SoapParser):
    namespace = "http://schemas.xmlsoap.org/soap/envelope/"

    def get_action_name(self, headers, options):
        return headers["soapaction"].strip('"')


class SoapParser12(SoapParser):
    namespace = "http://www.w3.org/2003/05/soap-envelope"

    def get_action_name(self, headers, options):
        return options[b"action"].decode("utf-8")


class XmlResponse(Response):
    media_type = "application/xml"


def get_soap_parser(headers: dict):
    if "soapaction" in headers:
        parser = SoapParser11()
    else:
        parser = SoapParser12()
    return parser


async def parse_input(headers: dict, stream):
    parser = get_soap_parser(headers)

    return await parser.parse(headers, stream)


class SoapHandler(HTTPEndpoint):
    service = None

    async def post(self, request):
        soap_request_input = await parse_input(request.headers, request.stream())
        response_instance = await call_action(self.service, soap_request_input)
        response_content = await render_response(response_instance)
        return XmlResponse(response_content)
