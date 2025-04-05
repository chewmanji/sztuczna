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
    inbound_lines: set[str] = field(default_factory=set)
    outbound_lines: set[str] = field(default_factory=set)

    def add_inbound_connection(self, connection: "Connection"):
        self.inbounds.append(connection)
        self.inbound_lines.add(connection.line)

    def add_outbound_connection(self, connection: "Connection"):
        self.outbounds.append(connection)
        self.outbound_lines.add(connection.line)

    def __eq__(self, other):
        if isinstance(other, Stop):
            return self.name == other.name
        return False

    def __lt__(self, other):
        return self.name < other.name

    def __repr__(self) -> str:
        return f"Stop(name={self.name})"
