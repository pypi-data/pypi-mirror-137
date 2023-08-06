from typing import Any, Dict, List, Tuple, TYPE_CHECKING

from kolo.serialize import serialize_celery_args, serialize_celery_kwargs


if TYPE_CHECKING:
    # TypedDict only exists on python 3.8+
    # We run mypy using a high enough version, so this is ok!
    from typing import TypedDict

    class HueyJob(TypedDict):
        name: str
        args: Tuple[Any, ...]
        kwargs: Dict[str, Any]


class HueyFilter:
    use_frames_of_interest = False

    def __init__(self) -> None:
        self.data: Dict[str, List[HueyJob]] = {"jobs_enqueued": []}

    def __call__(self, frame, event, arg):
        filepath = frame.f_code.co_filename
        co_name = frame.f_code.co_name
        if event == "call" and "/huey/api.py" in filepath and co_name == "__init__":
            from huey.api import Task

            return isinstance(frame.f_locals["self"], Task)
        return False

    def process(self, frame, event, arg, call_frame_ids):
        frame_locals = frame.f_locals
        task_object = frame_locals["self"]
        task_args = serialize_celery_args(frame_locals["args"])
        task_kwargs = serialize_celery_kwargs(frame_locals["kwargs"])

        job: HueyJob = {
            "name": f"{task_object.__module__}.{task_object.name}",
            "args": task_args,
            "kwargs": task_kwargs,
        }
        self.data["jobs_enqueued"].append(job)
