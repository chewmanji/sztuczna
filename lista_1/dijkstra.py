from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional
import heapq
from stop import Stop
from connection import Connection


@dataclass
class DijkstraResult:
    shortest_path: List[Stop]
    arrival_time: Optional[datetime] = None
    total_duration: Optional[timedelta] = None
    path_connections: List[Connection] = field(default_factory=list)


def dijkstra(
    start_stop: Stop, end_stop: Stop, arrival_time: datetime
) -> Optional[DijkstraResult]:
    # Priority queue to store stops to visit
    # Each item is (total_duration, stop, path_so_far, last_connection)
    pq: list[tuple[timedelta, datetime, Stop, list[Stop], list]] = [
        (timedelta(), arrival_time, start_stop, [start_stop], [])
    ]

    # Track visited stops to prevent cycles
    visited: set[str] = set()

    # Track the best known path to each stop
    # best_paths: Dict[Stop, DijkstraResult] = {}

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
            return DijkstraResult(
                shortest_path=current_path,
                arrival_time=current_time,
                total_duration=current_duration,
                path_connections=current_connections,
            )

        # Explore outbound connections
        for connection in current_stop.outbounds:
            # Skip if destination stop is already visited
            if connection.end_stop.name in visited:
                continue

            if connection.start_time < current_time:
                continue

            # Calculate total duration including this connection
            waiting_time = (
                connection.start_time - current_time
                if current_time < connection.start_time
                else current_time - connection.start_time
            )

            new_duration = current_duration + connection.duration + waiting_time

            # Calculate arrival time at the next stop
            new_arrival_time = connection.end_time

            # Prepare new path and check if we should explore this route
            new_path = current_path + [connection.end_stop]
            new_connections = current_connections + [connection]

            # Add to priority queue
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

    # No path found
    return None


def print_dijkstra_result(result: Optional[DijkstraResult], start_time: datetime):
    if result is None:
        print("No path found.")
        return

    print("Ścieżka:")
    for stop in result.shortest_path:
        print(f"- {stop.name}")

    print(f"\nCzas podróży: {result.total_duration}")
    print(f"Czas dotarcia do celu: {result.arrival_time}")

    print("\nPrzystanki:")
    for connection in result.path_connections:
        print(
            f"Line {connection.line}: "
            f"{connection.start_stop.name} -> {connection.end_stop.name} "
            f"(Departure: {connection.start_time}, Arrival: {connection.end_time})"
        )
