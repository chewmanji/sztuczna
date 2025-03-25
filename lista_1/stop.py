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
