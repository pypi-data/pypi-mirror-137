import time
import types
from typing import Dict, List, Optional, TYPE_CHECKING

from ..serialize import get_callsite_data


if TYPE_CHECKING:
    # TypedDict only exists on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import TypedDict
    from ..serialize import UserCodeCallSite

    class QueryInfo(TypedDict, total=False):
        query: str
        query_template: str
        user_code_call_site: Optional[UserCodeCallSite]
        call_timestamp: float
        return_timestamp: float


class SQLQueryFilter:
    use_frames_of_interest = False

    def __init__(self) -> None:
        self.queries_with_call_site: List[QueryInfo] = []
        self.data = {"queries_with_call_site": self.queries_with_call_site}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        co_name = frame.f_code.co_name
        filename = frame.f_code.co_filename
        return (
            co_name == "_execute" and "/django/db/backends/utils.py" in filename
        ) or co_name == "last_executed_query"

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        co_name = frame.f_code.co_name
        if event == "call" and co_name == "_execute":
            if call_frame_ids:
                user_code_call_site = get_callsite_data(frame, call_frame_ids[-1])
            else:
                user_code_call_site = None
            query_data: QueryInfo = {
                "user_code_call_site": user_code_call_site,
                "call_timestamp": time.time(),
                "query_template": frame.f_locals["sql"],
            }
            self.queries_with_call_site.append(query_data)
        elif event == "return":
            query_data = self.queries_with_call_site[-1]
            if co_name == "_execute":
                query_data["return_timestamp"] = time.time()
            elif co_name == "last_executed_query":  # pragma: no branch
                from django.db.backends.base.operations import BaseDatabaseOperations

                if isinstance(  # pragma: no branch
                    frame.f_locals.get("self"), BaseDatabaseOperations
                ):
                    assert isinstance(arg, str)
                    query_data["query"] = arg
