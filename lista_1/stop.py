from typing import TYPE_CHECKING
from dataclasses import dataclass, field

# Use string forward reference for Connection
if TYPE_CHECKING:
    from connection import Connection


@dataclass
class Stop:
    name: str
    lat: float
    lon: float
    inbounds: "list[Connection]" = field(default_factory=list)
    outbounds: "list[Connection]" = field(default_factory=list)

    def add_inbound_connection(self, connection: "Connection"):
        self.inbounds.append(connection)

    def add_outbound_connection(self, connection: "Connection"):
        self.outbounds.append(connection)

    def __eq__(self, other):
        if isinstance(other, Stop):
            return self.name == other.name
        return False

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self) -> str:
        return f"Stop(name={self.name})"
