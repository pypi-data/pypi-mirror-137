import inspect

from multipart.multipart import parse_options_header
from starlette.endpoints import HTTPEndpoint
from starlette.responses import Response
from xsdata.formats.dataclass.serializers import XmlSerializer
from xsdata.formats.dataclass.serializers.config import SerializerConfig

from teserak.w3c.soap.context import set_soap_context
from teserak.w3c.soap.multipart import SoapMultipartParser
from teserak.w3c.soap.types import (
    SoapRequest,
    SoapRequestInput,
    SoapVersion,
    XmlNamespace,
)
from teserak.w3c.soap.utils import parse_action


def build_input_request(input_cls, request_input: SoapRequestInput):
    return parse_action(request_input.body, input_cls).body.input


async def call_action(service, request_input: SoapRequestInput):
    action = service.get_action(request_input)

    input_cls = action.input
    output_cls = action.output
    action_handler = action.handler

    soap_request = SoapRequest(request_input.parts)
    action_kwargs = {}
    input_request = build_input_request(input_cls, request_input)
    kwargs = {"request": input_request, "context": soap_request}
    for parameter in action.parameters.keys():
        action_kwargs[parameter] = kwargs.get(parameter, ...)

    with set_soap_context(soap_request):
        result = await action_handler(**action_kwargs)
    return output_cls(body=action.output_body_class(result))


async def render_response(response_instance):
    config = SerializerConfig(pretty_print=True)
    serializer = XmlSerializer(config=config)
    response_content = serializer.render(response_instance)
    return response_content


class SoapParser:
    namespace = None
    version = None

    def get_action_name(self, headers, options) -> str:
        ...

    async def get_body(self, stream) -> str:
        body = b""
        async for chunk in stream:
            body += chunk
        return body.decode("utf-8")

    async def parse(self, headers: dict, stream) -> SoapRequestInput:
        content_type_header = headers["content-type"]
        content_type, options = parse_options_header(content_type_header)
        action_name = self.get_action_name(headers, options)
        if b"boundary" in options:
            parser = SoapMultipartParser()
            multipart_request = await parser.parse(options, stream)
            body = multipart_request.body
            parts = multipart_request.parts
        else:
            body = await self.get_body(stream)
            parts = {}
        return SoapRequestInput(
            action_name=action_name, soap_version=self.version, body=body, parts=parts
        )


class SoapParser11(SoapParser):
    version = SoapVersion.VERSION_11
    namespace = XmlNamespace.SOAP_11

    def get_action_name(self, headers, options):
        return headers["soapaction"].strip('"')


class SoapParser12(SoapParser):
    version = SoapVersion.VERSION_12
    namespace = XmlNamespace.SOAP_12

    def get_action_name(self, headers, options):
        return options[b"action"].decode("utf-8")


class XmlResponse(Response):
    media_type = "application/xml"


def get_soap_parser(headers: dict):

    if "application/soap+xml" in headers["content-type"]:
        parser = SoapParser12()
    else:
        parser = SoapParser11()
    return parser


async def parse_input(headers: dict, stream) -> SoapRequestInput:
    parser = get_soap_parser(headers)

    return await parser.parse(headers, stream)


class SoapHandler(HTTPEndpoint):
    service = None

    async def post(self, request):
        headers = request.headers
        body = await request.body()
        soap_request_input = await parse_input(request.headers, request.stream())
        response_instance = await call_action(self.service, soap_request_input)
        response_content = await render_response(response_instance)
        return XmlResponse(response_content)
