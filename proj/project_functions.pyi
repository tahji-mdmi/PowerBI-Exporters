from datetime import datetime, tzinfo
from typing import Literal, overload

@overload
def parse_datetime_string(
    datetime_string: str,
    _timezone: tzinfo | None = ...,
    ignore_errors: Literal[False] = ...,
) -> datetime: ...
@overload
def parse_datetime_string(
    datetime_string: str,
    _timezone: tzinfo | None = ...,
    ignore_errors: Literal[True] = ...,
) -> datetime | None: ...
