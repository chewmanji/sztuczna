from datetime import datetime, timedelta
from typing import Optional
import heapq
from stop import Stop
from connection import Connection
from utils import SearchResult, calculate_transfers, TRANSFER_TIME, measure_time


@measure_time
def dijkstra(
    start_stop: Stop, end_stop: Stop, arrival_time: datetime
) -> Optional[SearchResult]:
    # Priority queue to store stops to visit
    # Each item is (total_duration, arrival_time, stop, path_so_far, list_connections)
    pq: list[tuple[timedelta, datetime, Stop, list[Stop], list[Connection]]] = [
        (timedelta(), arrival_time, start_stop, [start_stop], [])
    ]

    # Track visited stops to prevent cycles
    visited: set[str] = set()

    while pq:
        (
            current_duration,
            current_time,
            current_stop,
            current_path,
            current_connections,
        ) = heapq.heappop(pq)

        # Skip if we've already found a better path to this stop
        if current_stop.name in visited:
            continue

        # Mark as visited
        visited.add(current_stop.name)

        # If we've reached the destination, return the result
        if current_stop == end_stop:
            return SearchResult(
                shortest_path=current_path,
                arrival_time=current_time,
                total_duration=current_duration,
                path_connections=current_connections,
                transfers=calculate_transfers(current_connections),
            )

        # Explore outbound connections
        for connection in current_stop.outbounds:
            # Skip if destination stop is already visited
            if connection.end_stop.name in visited:
                continue

            is_transfer = False
            if len(current_connections) != 0:
                is_transfer = current_connections[-1].line != connection.line

            new_current_time = current_time

            if is_transfer:
                new_current_time = new_current_time + timedelta(minutes=TRANSFER_TIME)
                if connection.start_time < new_current_time:
                    continue

            if connection.start_time < current_time:
                continue

            # Calculate total duration including this connection
            waiting_time = connection.start_time - current_time

            new_duration = current_duration + connection.duration + waiting_time

            # Calculate arrival time at the next stop
            new_arrival_time = connection.end_time

            # Prepare new path and check if we should explore this route
            new_path = current_path + [connection.end_stop]
            new_connections = current_connections + [connection]

            # Add to priority queue
            # solution from https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Using_a_priority_queue
            heapq.heappush(
                pq,
                (
                    new_duration,
                    new_arrival_time,
                    connection.end_stop,
                    new_path,
                    new_connections,
                ),
            )

    return None
