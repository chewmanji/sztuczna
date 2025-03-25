import pandas as pd
from stop import Stop
from connection import Connection
import re
from datetime import datetime, timedelta
import pickle

regexp = re.compile(r"(\d{2}):(\d{2}):(\d{2})")


# ['id', 'company', 'line', 'departure_time', 'arrival_time', 'start_stop',
#      'end_stop', 'start_stop_lat', 'start_stop_lon', 'end_stop_lat',
#      'end_stop_lon']
def create_stops(data: pd.DataFrame):
    stops: dict[str, Stop] = {}
    for start, start_lat, start_lon, end, end_lat, end_lon in zip(
        data.start_stop,
        data.start_stop_lat,
        data.start_stop_lon,
        data.end_stop,
        data.end_stop_lat,
        data.end_stop_lon,
    ):
        start_stop = Stop(start, start_lat, start_lon)
        end_stop = Stop(end, end_lat, end_lon)
        for stop in [start_stop, end_stop]:
            if stop.name not in stops.keys():
                stops[stop.name] = stop

    print(f"Number of stops generated: {len(stops)}")
    return stops


# ['id', 'company', 'line', 'departure_time', 'arrival_time', 'start_stop',
#      'end_stop', 'start_stop_lat', 'start_stop_lon', 'end_stop_lat',
#      'end_stop_lon']
def create_connections(data: pd.DataFrame, stops: dict[str, Stop]):
    connections: list[Connection] = []

    for line, start, end, departure_time, arrival_time in zip(
        data.line,
        data.start_stop,
        data.end_stop,
        data.departure_time,
        data.arrival_time,
    ):
        start_stop = stops[start]
        end_stop = stops[end]
        connection = Connection(
            line,
            start_stop,
            end_stop,
            getTime(departure_time),
            getTime(arrival_time),
        )
        connections.append(connection)
        start_stop.add_outbound_connection(connection)
        end_stop.add_inbound_connection(connection)

    print(f"Number of connections generated: {len(connections)}")
    return connections


def getTime(connection_time: str):
    match = re.search(regexp, connection_time)
    if match is None:
        raise Exception("Shouldn't happen")
    h, m, s = map(int, match.groups())
    if h >= 24:
        h -= 24
        dt = datetime.strptime(f"{h}:{m}:{s}", "%H:%M:%S")
        dt += timedelta(1)
        return dt
    else:
        dt = datetime.strptime(f"{h}:{m}:{s}", "%H:%M:%S")
        return dt


def create_structures():
    data = pd.read_csv(
        "data_with_normalized_locations.csv",
        dtype={"line": str},
    )
    stops = create_stops(data)
    connections = create_connections(data, stops)
    return stops, connections


if __name__ == "__main__":
    from arg_parser import parser

    args = parser.parse_args()

    criterion = args.criterion
    start_stop = args.start_stop
    end_stop = args.end_stop
    start_time = args.start_time

    stops, connections = create_structures()
