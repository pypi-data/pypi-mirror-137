import typing
from typing import TypeVar

from multipart.multipart import MultipartParser, parse_options_header
from starlette.formparsers import MultiPartMessage, _user_safe_decode

from teserak.w3c.soap.types import MultipartResponse, SoapRequestInput, SoapUploadFile


class SoapMultipartParser:
    def __init__(self):
        self.messages: typing.List[typing.Tuple[MultiPartMessage, bytes]] = []

    def on_part_begin(self) -> None:
        message = (MultiPartMessage.PART_BEGIN, b"")
        self.messages.append(message)

    def on_part_data(self, data: bytes, start: int, end: int) -> None:
        message = (MultiPartMessage.PART_DATA, data[start:end])
        self.messages.append(message)

    def on_part_end(self) -> None:
        message = (MultiPartMessage.PART_END, b"")
        self.messages.append(message)

    def on_header_field(self, data: bytes, start: int, end: int) -> None:
        message = (MultiPartMessage.HEADER_FIELD, data[start:end])
        self.messages.append(message)

    def on_header_value(self, data: bytes, start: int, end: int) -> None:
        message = (MultiPartMessage.HEADER_VALUE, data[start:end])
        self.messages.append(message)

    def on_header_end(self) -> None:
        message = (MultiPartMessage.HEADER_END, b"")
        self.messages.append(message)

    def on_headers_finished(self) -> None:
        message = (MultiPartMessage.HEADERS_FINISHED, b"")
        self.messages.append(message)

    def on_end(self) -> None:
        message = (MultiPartMessage.END, b"")
        self.messages.append(message)

    async def parse(self, options, stream) -> MultipartResponse:

        callbacks = {
            "on_part_begin": self.on_part_begin,
            "on_part_data": self.on_part_data,
            "on_part_end": self.on_part_end,
            "on_header_field": self.on_header_field,
            "on_header_value": self.on_header_value,
            "on_header_end": self.on_header_end,
            "on_headers_finished": self.on_headers_finished,
            "on_end": self.on_end,
        }

        content_disposition = None
        content_type = b""
        data = b""
        item_headers = []
        charset = options.get(b"charset", "utf-8")
        header_field = b""
        header_value = b""
        content_id = b""
        file: typing.Optional[SoapUploadFile] = None
        field_name = "b"
        body_fields = {}
        items: typing.List[typing.Tuple[str, typing.Union[str, SoapUploadFile]]] = []
        start_soap = options[b"start"].decode("utf-8")
        multipart_parser = MultipartParser(options[b"boundary"], callbacks)
        if multipart_parser:
            async for chunk in stream:
                messages = list(self.messages)
                self.messages.clear()
                multipart_parser.write(chunk)
                for message_type, message_bytes in messages:
                    if message_type == MultiPartMessage.PART_BEGIN:
                        content_disposition = None
                        content_type = b""
                        data = b""
                        item_headers = []
                    elif message_type == MultiPartMessage.HEADER_FIELD:
                        header_field += message_bytes
                    elif message_type == MultiPartMessage.HEADER_VALUE:
                        header_value += message_bytes
                    elif message_type == MultiPartMessage.HEADER_END:
                        field = header_field.lower()
                        if field == b"content-disposition":
                            content_disposition = header_value
                        elif field == b"content-type":
                            content_type = header_value
                        elif field == b"content-id":
                            content_id = header_value
                        item_headers.append((field, header_value))
                        header_field = b""
                        header_value = b""
                    elif message_type == MultiPartMessage.HEADERS_FINISHED:
                        disposition, options = parse_options_header(content_disposition)
                        if b"name" in options:
                            name = options[b"name"]
                            field_name = _user_safe_decode(name, charset)
                        else:
                            name = content_id
                            field_name = "cid:" + content_id.decode("utf-8").strip(
                                "<"
                            ).strip(">")
                        if b"filename" in options:
                            filename = _user_safe_decode(options[b"filename"], charset)
                            file = SoapUploadFile(
                                filename=filename,
                                content_type=content_type.decode("latin-1"),
                                headers=item_headers,
                            )
                        else:
                            file = None
                    elif message_type == MultiPartMessage.PART_DATA:
                        if file is None:
                            data += message_bytes
                        else:
                            await file.write(message_bytes)
                    elif message_type == MultiPartMessage.PART_END:
                        if file is None:
                            items.append((field_name, _user_safe_decode(data, charset)))
                        else:
                            await file.seek(0)
                            items.append((field_name, file))
            multipart_parser.finalize()
            body_fields = dict(items)
        new_start_soap = "cid:" + start_soap.strip("<").strip(">")
        body = body_fields[new_start_soap]
        del body_fields[new_start_soap]
        return MultipartResponse(body=body, parts=body_fields)


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
            parser = SoapMultipartParser()
            multipart_request = await parser.parse(options, stream)
            body = multipart_request.body
            parts = multipart_request.parts
        else:
            body = await self.get_body(stream)
            parts = {}
        return SoapRequestInput(action_name=action_name, body=body, parts=parts)


T = TypeVar("T")


class Provide(typing.Generic[T]):
    ...
