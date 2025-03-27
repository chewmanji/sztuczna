from datetime import datetime
from typing import TYPE_CHECKING
from dataclasses import dataclass


if TYPE_CHECKING:
    from stop import Stop


@dataclass
class Connection:
    def __init__(
        self,
        line: str,
        start_stop: "Stop",
        end_stop: "Stop",
        start_time: datetime,
        end_time: datetime,
    ) -> None:
        self.line = line
        self.start_stop = start_stop
        self.end_stop = end_stop
        self.start_time = start_time
        self.end_time = end_time
        self.duration = end_time - start_time

    def __lt__(self, other):
        return self.duration < other.duration
