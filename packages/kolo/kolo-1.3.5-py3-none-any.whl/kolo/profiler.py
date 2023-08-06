import json
import logging
import subprocess
import sys
import time
import types
import uuid
from datetime import datetime, timezone
from itertools import chain
from pathlib import Path
from typing import Any, Dict, List, Optional, TYPE_CHECKING

import toolz

from . import __version__
from .db import save_invocation_in_sqlite
from .filters.attrs import attrs_filter
from .filters.celery import CeleryFilter
from .filters.core import build_frame_filter, exec_filter, import_filter, library_filter
from .filters.exception import ExceptionFilter
from .filters.huey import HueyFilter
from .filters.kolo import kolo_filter
from .filters.requests import ApiRequestFilter
from .filters.sql import SQLQueryFilter
from .serialize import (
    frame_path,
    get_callsite_data,
    get_content,
    is_json_serializable,
    monkeypatch_queryset_repr,
    serialize_locals,
    serialize_potential_json,
)


logger = logging.getLogger("kolo")


if TYPE_CHECKING:
    # TypedDict only exists on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import TypedDict

    from django.http import HttpRequest, HttpResponse

    from .filters.core import AdvancedFrameFilter, FrameFilter
    from .serialize import UserCodeCallSite

    class FrameInfo(TypedDict):
        id: str
        path: str
        co_name: str
        event: str
        arg: str
        locals: str
        timestamp: float
        user_code_call_site: Optional[UserCodeCallSite]


def data_merge(values):
    if all(isinstance(value, list) for value in values):
        return list(chain.from_iterable(values))
    return values[0]


class KoloProfiler:
    """
    Collect runtime information about code to view in VSCode.

    include_frames can be passed to enable profiling of standard library
    or third party code.

    ignore_frames can also be passed to disable profiling of a user's
    own code.

    The list should contain fragments of the path to the relevant files.
    For example, to include profiling for the json module the include_frames
    could look like ["/json/"].

    The list may also contain frame filters. A frame filter is a function
    (or other callable) that takes the same arguments as the profilefunc
    passed to sys.setprofile and returns a boolean representing whether
    to allow or block the frame.

    include_frames takes precedence over ignore_frames. A frame that
    matches an entry in each list will be profiled.
    """

    def __init__(self, db_path: Path, *, include_frames=(), ignore_frames=()) -> None:
        self.db_path = db_path
        self.timestamp = datetime.now(timezone.utc)
        self.invocation_id = f"inv_{uuid.uuid4()}"
        self.frames_of_interest: List[FrameInfo] = []
        self.request: Optional[Dict[str, Any]] = None
        self.response: Optional[Dict[str, Any]] = None
        self.include_frames = list(map(build_frame_filter, include_frames))
        self.ignore_frames = list(map(build_frame_filter, ignore_frames))
        self.default_include_frames: List[AdvancedFrameFilter] = [
            CeleryFilter(),
            HueyFilter(),
            ApiRequestFilter(),
            ExceptionFilter(),
            SQLQueryFilter(),
        ]
        self.default_ignore_frames: List[FrameFilter] = [
            library_filter,
            exec_filter,
            attrs_filter,
            import_filter,
            kolo_filter,
        ]
        self.call_frame_ids: List[Dict[str, str]] = []

    def initialize_request(self, request: "HttpRequest"):
        from django.db import reset_queries

        reset_queries()
        self.request = {
            "scheme": request.scheme,
            "method": request.method,
            "path_info": request.path_info,
            "body": request.body.decode("utf-8"),
            "headers": dict(request.headers),
            "url_pattern": None,
        }

    def set_url_pattern(self, request: "HttpRequest"):
        assert isinstance(self.request, dict)
        match = request.resolver_match
        # match can be None before url resolving, but we always
        # call set_url_pattern after resolving
        assert match
        self.request["url_pattern"] = {
            "namespace": match.namespace,
            "route": match.route,
            "url_name": match.url_name,
            "view_path": match._func_path,
        }

    def finalize_response(self, response: "HttpResponse") -> None:
        duration = datetime.now(timezone.utc) - self.timestamp

        self.response = {
            "ms_duration": round(duration.total_seconds() * 1000, 2),
            "status_code": response.status_code,
            "content": get_content(response),
            "headers": dict(response.items()),
        }

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> None:
        if event in ["c_call", "c_return"]:
            return

        with monkeypatch_queryset_repr():
            for frame_filter in self.include_frames:
                try:
                    if frame_filter(frame, event, arg):
                        self.process_frame(frame, event, arg)
                        return
                except Exception as e:
                    logger.debug(
                        "Unexpected exception in include_frames: %s",
                        frame_filter,
                        exc_info=e,
                    )
                    continue

            for frame_filter in self.ignore_frames:
                try:
                    if frame_filter(frame, event, arg):
                        return
                except Exception as e:
                    logger.debug(
                        "Unexpected exception in ignore_frames: %s",
                        frame_filter,
                        exc_info=e,
                    )
                    continue

            for frame_filter in self.default_include_frames:
                try:
                    if frame_filter(frame, event, arg):
                        if frame_filter.use_frames_of_interest:
                            self.process_frame(frame, event, arg)
                        frame_filter.process(frame, event, arg, self.call_frame_ids)
                        return
                except Exception as e:
                    logger.debug(
                        "Unexpected exception in default_include_frames: %s",
                        frame_filter,
                        exc_info=e,
                    )
                    continue

            for frame_filter in self.default_ignore_frames:
                try:
                    if frame_filter(frame, event, arg):
                        return
                except Exception as e:
                    logger.debug(
                        "Unexpected exception in default_ignore_frames: %s",
                        frame_filter,
                        exc_info=e,
                    )
                    continue

            try:
                self.process_frame(frame, event, arg)
            except Exception as e:
                logger.debug(
                    "Unexpected exception in KoloProfiler.process_frame",
                    exc_info=e,
                )

    def __enter__(self):
        sys.setprofile(self)

    def __exit__(self, *exc):
        sys.setprofile(None)

    def save_request_in_db(self) -> None:
        current_commit_sha = (
            subprocess.run(
                ["git", "rev-parse", "HEAD"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            .stdout.decode("utf-8")
            .strip()
        )
        json_data = {
            "request_id": self.invocation_id,
            "invocation_id": self.invocation_id,
            "current_commit_sha": current_commit_sha,
            "request": self.request,
            "response": self.response,
            "timestamp": str(self.timestamp),
            "frames_of_interest": self.frames_of_interest,
            "meta": {"version": __version__},
        }
        for frame_filter in self.default_include_frames:
            data = frame_filter.data
            if is_json_serializable(data):
                json_data = toolz.merge_with(data_merge, json_data, data)
            else:
                name = type(frame_filter).__name__
                logger.error(
                    f"Unexpected exception when serializing {name} data: {data}"
                )

        save_invocation_in_sqlite(
            self.db_path, self.invocation_id, json.dumps(json_data)
        )

    def process_frame(self, frame: types.FrameType, event: str, arg: object) -> None:
        user_code_call_site: Optional[UserCodeCallSite]
        if event == "call" and self.call_frame_ids:
            user_code_call_site = get_callsite_data(frame, self.call_frame_ids[-1])
        else:
            # If we are a return frame, we don't bother duplicating
            # information for the call frame.
            # If we are the first call frame, we don't have a callsite.
            user_code_call_site = None

        frame_id = f"frm_{uuid.uuid4()}"
        co_name = frame.f_code.co_name
        if event == "call":
            call_frame_data = {
                "frame_id": frame_id,
                "filepath": frame.f_code.co_filename,
                "co_name": co_name,
            }
            self.call_frame_ids.append(call_frame_data)
        elif event == "return":  # pragma: no branch
            self.call_frame_ids.pop()

        self.frames_of_interest.append(
            {
                "id": frame_id,
                "path": frame_path(frame),
                "co_name": co_name,
                "event": event,
                "arg": serialize_potential_json(arg),
                "locals": serialize_locals(frame.f_locals),
                "timestamp": time.time(),
                "user_code_call_site": user_code_call_site,
            }
        )
