import logging
import types
from datetime import datetime, timezone
from typing import Dict, List, Optional, TYPE_CHECKING

from ..serialize import decode_body, decode_header_value


logger = logging.getLogger("kolo")


if TYPE_CHECKING:
    # TypedDict only exists on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import TypedDict

    class ApiRequest(TypedDict):
        method: str
        url: str
        method_and_full_url: str
        body: Optional[str]
        headers: Dict[str, str]
        timestamp: str

    class BaseApiResponse(TypedDict):
        timestamp: str
        status_code: int
        headers: Dict[str, str]

    class ApiResponse(BaseApiResponse, total=False):
        body: str

    class BaseApiInfo(TypedDict):
        request: ApiRequest

    class ApiInfo(BaseApiInfo, total=False):
        response: ApiResponse


def get_timestamp() -> str:
    return datetime.now(timezone.utc).isoformat()


class ApiRequestFilter:
    use_frames_of_interest = True

    def __init__(self) -> None:
        self.data: Dict[str, List[ApiInfo]] = {"api_requests_made": []}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        return (
            self.match_request(frame)
            or self.match_response(frame)
            or self.match_urllib(frame)
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        if event == "call" and self.match_request(frame):
            self.process_api_request_made(frame)
        elif event == "return" and self.match_response(frame):
            self.process_api_response(frame)
        elif self.match_urllib(frame):
            self.process_urllib(frame, event)

    def match_request(self, frame: types.FrameType) -> bool:
        filepath = frame.f_code.co_filename
        callable_name = frame.f_code.co_name
        return "urllib3/connectionpool" in filepath and callable_name == "urlopen"

    def match_response(self, frame: types.FrameType) -> bool:
        filepath = frame.f_code.co_filename
        callable_name = frame.f_code.co_name
        return (
            "urllib3/connectionpool" in filepath and callable_name == "urlopen"
        ) or ("requests/sessions" in filepath and callable_name == "request")

    def match_urllib(self, frame: types.FrameType) -> bool:
        filepath = frame.f_code.co_filename
        callable_name = frame.f_code.co_name
        return "urllib/request" in filepath and callable_name == "do_open"

    def process_api_request_made(self, frame: types.FrameType):
        frame_locals = frame.f_locals

        scheme = frame_locals["self"].scheme
        host = frame_locals["self"].host
        url = frame_locals["url"]
        full_url = f"{scheme}://{host}{url}"

        request_headers = {
            key: decode_header_value(value)
            for key, value in frame_locals["headers"].items()
        }

        method = frame_locals["method"].upper()
        method_and_full_url = f"{method} {full_url}"

        api_request: ApiInfo = {
            "request": {
                "method": method,
                "url": full_url,
                "method_and_full_url": method_and_full_url,
                "body": decode_body(frame_locals["body"]),
                "headers": request_headers,
                "timestamp": get_timestamp(),
            }
        }

        self.data["api_requests_made"].append(api_request)

    def process_api_response(self, frame: types.FrameType):
        if frame.f_code.co_name == "urlopen":
            response = frame.f_locals["response"]
            self.data["api_requests_made"][-1]["response"] = {
                "timestamp": get_timestamp(),
                "status_code": response.status,
                "headers": dict(response.headers),
            }
        else:
            response = frame.f_locals["resp"]
            self.data["api_requests_made"][-1]["response"]["body"] = response.text

    def process_urllib(self, frame: types.FrameType, event: str):
        if event == "call":
            request = frame.f_locals["req"]
            full_url = request.full_url
            method = request.get_method()
            method_and_full_url = f"{method} {full_url}"
            request_headers = {
                key: decode_header_value(value) for key, value in request.header_items()
            }

            api_request: ApiInfo = {
                "request": {
                    "method": method,
                    "url": full_url,
                    "method_and_full_url": method_and_full_url,
                    "body": decode_body(request.data),
                    "headers": request_headers,
                    "timestamp": get_timestamp(),
                }
            }

            self.data["api_requests_made"].append(api_request)
        elif event == "return":  # pragma: no branch
            response = frame.f_locals["r"]
            self.data["api_requests_made"][-1]["response"] = {
                "timestamp": get_timestamp(),
                "status_code": response.status,
                "headers": dict(response.headers),
            }
