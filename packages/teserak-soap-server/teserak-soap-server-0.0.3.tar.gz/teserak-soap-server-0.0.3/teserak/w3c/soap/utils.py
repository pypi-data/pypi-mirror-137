from dataclasses import Field, dataclass, field, make_dataclass
from typing import Iterable, Optional, TypeVar, get_args

from starlette.applications import Starlette
from starlette.routing import Route
from xsdata.formats.dataclass.context import XmlContext
from xsdata.formats.dataclass.parsers import UserXmlParser


class BaseService:
    registry = {}

    def __init__(self, location=None):
        self.location = location
        
    def get_asgi_app(self):
        from teserak.w3c.soap.handler import SoapHandler

        class Endpoint(SoapHandler):
            service = self

        app = Starlette(routes=[
            Route('/', Endpoint),
        ])
        return app

    def action(self, action_name):
        def inner(func):
            class Action(SoapService):
                soap_action = action_name
                soap_request_type = func.__annotations__["request"]
                input_request = get_args(soap_request_type)[0]
                output_response = func.__annotations__["return"]
                handler = func

            self.register_action(Action)

        return inner

    def register_action(self, action):
        self.registry[action.soap_action] = action

    def get_action(self, action):
        return self.registry[action]

    def get_input(self, action_cls):
        return self.registry[action_cls.soap_action].input


def soap_output_factory(field_name, soap_namespace, cls_name, cls):
    # return CalculatorSoapAddOutput
    return soap_input_factory(field_name, soap_namespace, cls_name, cls)


class Envelope:
    class Meta:
        name = "Envelope"
        namespace = "http://www.w3.org/2003/05/soap-envelope"


def soap_body_factory(field_name, cls):
    input_field = (
        field_name,
        Optional[cls],
        field(
            default=None,
            metadata={
                "name": cls.__name__,
                "type": "Element",
                "namespace": cls.Meta.namespace,
            },
        ),
    )
    return make_dataclass("Body", [input_field])


@dataclass
class Header:
    class Meta:
        namespace = "http://www.w3.org/2003/05/soap-envelope"

    action: Optional[str] = field(
        default=None,
        metadata={
            "name": "Action",
            "type": "Element",
            "namespace": "http://www.w3.org/2005/08/addressing",
        },
    )
    message_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "MessageID",
            "type": "Element",
            "namespace": "http://www.w3.org/2005/08/addressing",
        },
    )
    relates_to: Optional[str] = field(
        default=None,
        metadata={
            "name": "RelatesTo",
            "type": "Element",
            "namespace": "http://www.w3.org/2005/08/addressing",
        },
    )


T = TypeVar("T")


def parse_action(content, input_cls: T) -> T:
    context = XmlContext()
    parser = UserXmlParser(context=context)
    result: input_cls = parser.from_string(content, input_cls)
    return result


def soap_input_factory(field_name, soap_namespace, cls_name, cls):
    body_cls = soap_body_factory(field_name, cls)
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
                metadata=dict(name="Body", type="Element", namespace=soap_namespace),
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


class SoapService:
    transport = "http://schemas.xmlsoap.org/soap/http"
    input_request = None
    output_response = None
    style = "document"
    soap_namespace = "http://www.w3.org/2003/05/soap-envelope"

    def __init_subclass__(cls, scm_type=None, name=None, **kwargs):
        cls.input, cls.input_body_class = soap_input_factory(
            "input", cls.soap_namespace, f"{cls.__name__}Input", cls.input_request
        )
        cls.output, cls.output_body_class = soap_output_factory(
            "output", cls.soap_namespace, f"{cls.__name__}Output", cls.output_response
        )
