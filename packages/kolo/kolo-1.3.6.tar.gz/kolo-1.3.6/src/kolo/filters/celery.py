import types
from typing import Any, Dict, List, Tuple, TYPE_CHECKING

from kolo.serialize import serialize_celery_args, serialize_celery_kwargs


if TYPE_CHECKING:
    # TypedDict only exists on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import TypedDict

    class CeleryJob(TypedDict):
        name: str
        args: Tuple[Any, ...]
        kwargs: Dict[str, Any]


class CeleryFilter:
    use_frames_of_interest = True

    def __init__(self) -> None:
        self.data: Dict[str, List[CeleryJob]] = {"jobs_enqueued": []}

    def __call__(self, frame: types.FrameType, event: str, arg: object) -> bool:
        filepath = frame.f_code.co_filename
        return (
            "celery" in filepath
            and "sentry_sdk" not in filepath
            and "apply_async" in frame.f_code.co_name
        )

    def process(
        self,
        frame: types.FrameType,
        event: str,
        arg: object,
        call_frame_ids: List[Dict[str, str]],
    ):
        if event == "return":
            return

        frame_locals = frame.f_locals
        task_name = frame_locals["self"].name
        task_args = serialize_celery_args(frame_locals["args"])
        task_kwargs = serialize_celery_kwargs(frame_locals["kwargs"])

        job: CeleryJob = {"name": task_name, "args": task_args, "kwargs": task_kwargs}

        self.data["jobs_enqueued"].append(job)
