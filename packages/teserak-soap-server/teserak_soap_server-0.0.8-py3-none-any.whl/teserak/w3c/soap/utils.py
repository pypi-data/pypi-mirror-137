import inspect
from dataclasses import Field, dataclass, field, make_dataclass
from typing import Iterable, Optional, TypeVar, get_args

from starlette.applications import Starlette
from starlette.routing import Route
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import UserXmlParser

from teserak.w3c.soap.types import SoapVersion, XmlNamespace


class SoapService:
    def __init__(self, location=None, path="/"):
        self.location = location
        self.path = path
        self.registry = {}
        self.app = self.get_asgi_app()

    def __call__(self, *args, **kwargs):
        return self.app(*args, **kwargs)

    def get_asgi_app(self):
        from teserak.w3c.soap.handler import SoapHandler

        class Endpoint(SoapHandler):
            service = self

        app = Starlette(
            routes=[
                Route(self.path, Endpoint),
            ]
        )
        return app

    def action(self, action_name):
        def inner(func):
            class Action(SoapAction):
                soap_action = action_name
                input_request = func.__annotations__["request"]
                output_response = func.__annotations__["return"]

            self.register_action(
                SoapVersion.VERSION_11, Action(XmlNamespace.SOAP_11, func)
            )
            self.register_action(
                SoapVersion.VERSION_12, Action(XmlNamespace.SOAP_12, func)
            )

        return inner

    @classmethod
    def build_full_action_name(cls, version, action):
        return f"{version}|{action}"

    def register_action(self, version, action):
        action_with_version = self.build_full_action_name(version, action.soap_action)
        self.registry[action_with_version] = action

    def get_action(self, request_input):
        action = request_input.action_name
        version = request_input.soap_version
        action_with_version = self.build_full_action_name(version, action)
        return self.registry[action_with_version]

    def get_input(self, action_cls):
        return self.registry[action_cls.soap_action].input


class Envelope11:
    class Meta:
        name = "Envelope"
        namespace = XmlNamespace.SOAP_11


class Envelope12:
    class Meta:
        name = "Envelope"
        namespace = XmlNamespace.SOAP_12


def soap_body_factory(field_name, cls):
    target_field_name = getattr(cls.Meta, "name", cls.__name__)
    namespace = getattr(cls.Meta, "namespace", None)
    input_field = (
        field_name,
        Optional[cls],
        field(
            default=None,
            metadata={
                "name": target_field_name,
                "type": "Element",
                "namespace": namespace,
            },
        ),
    )
    return make_dataclass("Body", [input_field])


class HeaderMixin:
    action: Optional[str] = field(
        default=None,
        metadata={
            "name": "Action",
            "type": "Element",
            "namespace": XmlNamespace.WS_ADDRESSING,
        },
    )
    message_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "MessageID",
            "type": "Element",
            "namespace": XmlNamespace.WS_ADDRESSING,
        },
    )
    relates_to: Optional[str] = field(
        default=None,
        metadata={
            "name": "RelatesTo",
            "type": "Element",
            "namespace": XmlNamespace.WS_ADDRESSING,
        },
    )


@dataclass
class Header11(HeaderMixin):
    class Meta:
        namespace = XmlNamespace.SOAP_11
        name = 'header'


@dataclass
class Header12(HeaderMixin):
    class Meta:
        namespace = XmlNamespace.SOAP_12
        name = 'header'


T = TypeVar("T")


def parse_action(content, input_cls: T) -> T:
    context = XmlContext()
    parser = UserXmlParser(context=context)
    result: input_cls = parser.from_string(content, input_cls)
    return result


def soap_input_output_factory(field_name, soap_namespace, cls_name, cls):

    body_cls = soap_body_factory(field_name, cls)
    if soap_namespace == XmlNamespace.SOAP_11:
        Header = Header11
        Envelope = Envelope11
    else:
        Header = Header12
        Envelope = Envelope12
    fields: Iterable[str, type, Field] = [
        (
            "header",
            Optional[Header],
            field(
                default=None,
                metadata=dict(name="Header", type="Element", namespace=soap_namespace),
            ),
        ),
        (
            "body",
            Optional[body_cls],
            field(
                default=None,
                metadata=dict(name="Body", type="Element"),
            ),
        ),
    ]

    class Meta:
        name = "Envelope"
        namespace = soap_namespace

    return (
        make_dataclass(
            cls_name=cls_name,
            fields=fields,
            bases=(Envelope,),
            namespace={"Meta": Meta},
        ),
        body_cls,
    )


def soap_input_factory(soap_namespace, cls_name, cls):
    return soap_input_output_factory("input", soap_namespace, cls_name, cls)


def soap_output_factory(soap_namespace, cls_name, cls):
    return soap_input_output_factory("output", soap_namespace, cls_name, cls)


class SoapAction:
    transport = "http://schemas.xmlsoap.org/soap/http"
    input_request = None
    output_response = None
    style = "document"
    soap_namespace = None

    def __init__(self, soap_namespace, func):
        self.handler = func
        self.parameters = inspect.signature(func).parameters
        self.soap_namespace = soap_namespace
        self.input, self.input_body_class = soap_input_factory(
            self.soap_namespace, f"{self.__class__.__name__}Input", self.input_request
        )
        self.output, self.output_body_class = soap_output_factory(
            self.soap_namespace,
            f"{self.__class__.__name__}Output",
            self.output_response,
        )
