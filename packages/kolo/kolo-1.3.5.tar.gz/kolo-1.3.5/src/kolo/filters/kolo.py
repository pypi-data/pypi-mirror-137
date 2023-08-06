import types


def kolo_filter(frame: types.FrameType, event: str, arg: object) -> bool:
    """Don't profile kolo code"""
    filename = frame.f_code.co_filename
    return (
        "/kolo/middleware" in filename
        or "/kolo/profiler" in filename
        or "/kolo/serialize" in filename
    )
