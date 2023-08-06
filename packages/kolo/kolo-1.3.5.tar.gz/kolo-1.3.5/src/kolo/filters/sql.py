import time
import types
from typing import Any, Dict, List, TYPE_CHECKING

from ..serialize import get_callsite_data, serialize_potential_json


if TYPE_CHECKING:
    # TypedDict only exists on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import TypedDict
    from ..serialize import UserCodeCallSite

    class QueryInfo(TypedDict, total=False):
        query: str
        query_template: str
        user_code_call_site: UserCodeCallSite
        call_timestamp: float
        return_timestamp: float


class SQLQueryFilter:
    use_frames_of_interest = False

    def __init__(self) -> None:
        self.queries_with_call_site: List[QueryInfo] = []
        self.data = {"queries_with_call_site": self.queries_with_call_site}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        co_name = frame.f_code.co_name
        return (
            co_name in ("_execute", "debug_sql", "execute")
            and "/django/db/backends/utils.py" in frame.f_code.co_filename
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        import django

        co_name = frame.f_code.co_name
        if event == "call" and co_name == "_execute":
            query_data: QueryInfo = {
                "user_code_call_site": get_callsite_data(frame, call_frame_ids[-1]),
                "call_timestamp": time.time(),
                "query_template": frame.f_locals["sql"],
            }
            self.queries_with_call_site.append(query_data)
        elif event == "return":
            query_data = self.queries_with_call_site[-1]

            assert frame.f_back is not None
            calling_co_name = frame.f_back.f_code.co_name
            if co_name == "_execute":
                query_data["return_timestamp"] = time.time()
            elif (
                co_name == "debug_sql" and calling_co_name == "__exit__"
            ) or django.VERSION < (3, 0, 0):
                query_data["query"] = frame.f_locals["sql"]
