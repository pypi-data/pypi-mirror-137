from dataclasses import dataclass, field
from typing import Optional

from teserak.w3c.soap.context import soap_context
from teserak.w3c.soap.types import SoapRequest


@dataclass
class Base64Binary:
    class Meta:
        name = "base64Binary"
        target_namespace = "http://www.w3.org/2005/05/xmlmime"

    value: Optional[bytes] = field(
        default=None,
        metadata={
            "required": True,
            "format": "base64",
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "contentType",
            "type": "Attribute",
            "namespace": "http://www.w3.org/2005/05/xmlmime",
        },
    )

    @soap_context
    async def read(self, context: SoapRequest):
        cid_value = self.value.replace("cid:", "").strip()
        attachment = context.parts.get(cid_value, None)
        if attachment:
            return await attachment.read()
        return None


@dataclass
class HexBinary:
    class Meta:
        name = "hexBinary"
        target_namespace = "http://www.w3.org/2005/05/xmlmime"

    value: str = field(
        default="",
        metadata={
            "required": True,
        },
    )
    content_type: Optional[str] = field(
        default=None,
        metadata={
            "name": "contentType",
            "type": "Attribute",
            "namespace": "http://www.w3.org/2005/05/xmlmime",
        },
    )
