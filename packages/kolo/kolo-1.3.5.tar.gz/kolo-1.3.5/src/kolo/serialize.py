import gzip
import json
import os
import types
from collections.abc import Iterator
from contextlib import contextmanager
from typing import Any, Dict, Tuple, TYPE_CHECKING, Union


CWD = os.getcwd()


if TYPE_CHECKING:
    # TypedDict only exists on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import TypedDict

    from django.http import HttpResponse, StreamingHttpResponse

    class UserCodeCallSite(TypedDict):
        line_number: int
        call_frame_id: str


@contextmanager
def monkeypatch_queryset_repr():
    try:
        from django.db.models import QuerySet
    except ImportError:  # pragma: no cover
        yield
        return

    old_repr = QuerySet.__repr__

    def new_repr(queryset):
        if queryset._result_cache is None:
            return f"Unevaluated queryset for: {queryset.model}"
        return old_repr(queryset)

    QuerySet.__repr__ = new_repr  # type: ignore
    try:
        yield
    finally:
        QuerySet.__repr__ = old_repr  # type: ignore


def _serialize_local(local: object) -> object:
    if isinstance(local, Iterator):
        return f"Iterator object (type: {type(local)})"

    try:
        json.dumps(local)
    except (TypeError, OverflowError, ValueError):
        try:
            return str(local)
        except Exception:
            return "SerializationError"
    return local


def serialize_celery_args(args: Tuple[Any, ...]) -> Tuple[Any, ...]:
    return tuple([_serialize_local(arg) for arg in args])


def serialize_celery_kwargs(kwargs: Dict[str, Any]) -> Dict[str, Any]:
    return {key: _serialize_local(value) for key, value in kwargs.items()}


def serialize_locals(locals: Dict[str, object]) -> str:
    serialized_locals = {key: _serialize_local(value) for key, value in locals.items()}
    return json.dumps(serialized_locals, indent=2)


def serialize_potential_json(arg: object) -> str:
    if arg is None:
        return str(arg)

    if isinstance(arg, Iterator):
        return f"Iterator object (type: {type(arg)})"

    try:
        return json.dumps(arg)
    except (TypeError, OverflowError, ValueError):
        return str(arg)


def is_json_serializable(data: Any):
    try:
        json.dumps(data)
    except TypeError:
        return False
    return True


def decode_header_value(bytes_or_str: Union[bytes, str]) -> str:
    """
    Convert a bytes header value to text.

    Valid header values are expected to be ascii in modern times, but
    ISO-8859-1 (latin1) has historically been allowed.

    https://datatracker.ietf.org/doc/html/rfc7230#section-3.2.4
    """
    if isinstance(bytes_or_str, bytes):
        return bytes_or_str.decode("latin1")
    return bytes_or_str


def get_call_frame(
    frame: types.FrameType, filepath: str, co_name: str
) -> types.FrameType:
    """Search back in a frame's stack for the triggering user code frame"""

    while True:
        assert frame.f_back is not None
        frame = frame.f_back
        if frame.f_code.co_filename == filepath and frame.f_code.co_name == co_name:
            return frame


def get_callsite_data(
    frame: types.FrameType, call_frame_data: Dict[str, str]
) -> "UserCodeCallSite":
    """
    Find the parent user code frame and return its frame_id and line number

    We already have the frame_id available in call_frame_data, but we don't
    know the currently active line number, so we search back in the frame
    stack using the filepath and co_name until we find the call frame itself.
    """
    call_frame = get_call_frame(
        frame, call_frame_data["filepath"], call_frame_data["co_name"]
    )
    return {
        "call_frame_id": call_frame_data["frame_id"],
        "line_number": call_frame.f_lineno,
    }


def frame_path(frame: types.FrameType) -> str:
    relative_path = frame.f_code.co_filename.replace(f"{CWD}/", "")
    return f"{relative_path}:{frame.f_lineno}"


def decode_body(body: Any) -> Any:
    """Convert a request body into a json-serializable form."""
    try:
        json.dumps(body)
    except TypeError:
        if isinstance(body, bytes):
            return body.decode("utf-8")
        return f"Error: Could not parse request body. Type: {type(body)}"
    return body


def get_content(response: Union["HttpResponse", "StreamingHttpResponse"]) -> str:
    if response.streaming:
        return "<Streaming Response>"

    content_encoding = response.get("Content-Encoding")
    if content_encoding == "gzip":
        content = gzip.decompress(response.content)
    else:
        content = response.content
    return content.decode(response.charset)
