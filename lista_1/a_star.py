# https://en.wikipedia.org/wiki/Vincenty%27s_formulae
from vincenty import vincenty
from stop import Stop
from datetime import datetime, timedelta
from typing import Optional
import heapq
from connection import Connection
from utils import SearchResult, calculate_transfers

VEHICLE_VELOCITY = 70  # km/h


def heuristic(
    stop: Stop,
    end_stop: Stop,
    is_transfer: bool = False,
):
    distance = vincenty(
        (stop.lat, stop.lon),
        (end_stop.lat, end_stop.lon),
        miles=False,
    )

    if distance is None:
        raise Exception("Shouldn't happen")

    transfer_penalty = 0  # hours

    if is_transfer:
        transfer_penalty = 0.5

    estimated_cost = distance / VEHICLE_VELOCITY + transfer_penalty

    return estimated_cost


def a_star_min_time(
    start_stop: Stop, end_stop: Stop, arrival_time: datetime, stops: list[Stop]
) -> Optional[SearchResult]:
    print(f"Średnia prędkość pojazdu: {VEHICLE_VELOCITY} km/h")
    # Priority queue to store stops to visit
    open_set: list[tuple[timedelta, datetime, Stop, list[Stop], list[Connection]]] = []

    # Keep track of the best known path to each stop
    g_score: dict[str, timedelta] = {s.name: timedelta.max for s in stops}
    g_score[start_stop.name] = timedelta(0)

    # Estimated total cost from start to end through this stop
    f_score: dict[str, timedelta] = {s.name: timedelta.max for s in stops}
    f_score[start_stop.name] = timedelta(hours=heuristic(start_stop, end_stop))

    # Track the best path and connections
    came_from: dict[str, Connection] = {}

    # Initial queue entry: (f_score, arrival_time, stop)
    heapq.heappush(
        open_set, (f_score[start_stop.name], arrival_time, start_stop, [start_stop], [])
    )

    while open_set:
        _, current_time, current_stop, current_path, current_connections = (
            heapq.heappop(open_set)
        )

        if current_stop.name == end_stop.name:
            return SearchResult(
                shortest_path=current_path,
                arrival_time=current_time,
                total_duration=current_time - arrival_time,
                path_connections=current_connections,
                transfers=calculate_transfers(current_connections),
            )

        # Explore outbound connections
        for connection in current_stop.outbounds:
            # Skip connections that start before current time
            if connection.start_time < current_time:
                continue

            neighbour = connection.end_stop

            # Calculate waiting time and total travel time
            waiting_time = connection.start_time - current_time
            total_travel_time = (
                g_score[current_stop.name] + waiting_time + connection.duration
            )

            # Heuristic estimate to the end stop
            heuristic_estimate = timedelta(hours=heuristic(neighbour, end_stop))
            estimated_total_cost = total_travel_time + heuristic_estimate

            # Check if this is a better path
            if total_travel_time < g_score[neighbour.name]:
                # Update best known path
                came_from[neighbour.name] = connection
                g_score[neighbour.name] = total_travel_time
                f_score[neighbour.name] = estimated_total_cost

                new_path = current_path + [neighbour]
                new_connections = current_connections + [connection]

                # Push to open set with new arrival time
                heapq.heappush(
                    open_set,
                    (
                        estimated_total_cost,
                        connection.end_time,
                        neighbour,
                        new_path,
                        new_connections,
                    ),
                )

    # No path found
    return None


def a_star_min_transfers(
    start_stop: Stop, end_stop: Stop, arrival_time: datetime, stops: list[Stop]
) -> Optional[SearchResult]:
    print(f"Średnia prędkość pojazdu: {VEHICLE_VELOCITY} km/h")
    # Priority queue to store stops to visit
    open_set: list[tuple[timedelta, datetime, Stop, list[Stop], list[Connection]]] = []

    # Keep track of the best known path to each stop
    g_score: dict[str, timedelta] = {s.name: timedelta.max for s in stops}
    g_score[start_stop.name] = timedelta(0)

    # Estimated total cost from start to end through this stop
    f_score: dict[str, timedelta] = {s.name: timedelta.max for s in stops}
    f_score[start_stop.name] = timedelta(hours=heuristic(start_stop, end_stop))

    # Track the best path and connections
    came_from: dict[str, Connection] = {}

    # Initial queue entry: (f_score, arrival_time, stop)
    heapq.heappush(
        open_set, (f_score[start_stop.name], arrival_time, start_stop, [start_stop], [])
    )

    while open_set:
        _, current_time, current_stop, current_path, current_connections = (
            heapq.heappop(open_set)
        )

        if current_stop.name == end_stop.name:
            return SearchResult(
                shortest_path=current_path,
                arrival_time=current_time,
                total_duration=current_time - arrival_time,
                path_connections=current_connections,
                transfers=calculate_transfers(current_connections),
            )

        # Explore outbound connections
        for connection in current_stop.outbounds:
            # Skip connections that start before current time
            if connection.start_time < current_time:
                continue

            neighbour = connection.end_stop

            # Calculate waiting time and total travel time
            waiting_time = connection.start_time - current_time
            total_travel_time = (
                g_score[current_stop.name] + waiting_time + connection.duration
            )

            # Heuristic estimate to the end stop
            is_transfer = False
            if len(current_connections) != 0:
                is_transfer = current_connections[-1].line != connection.line

            heuristic_estimate = timedelta(
                hours=heuristic(neighbour, end_stop, is_transfer)
            )
            estimated_total_cost = total_travel_time + heuristic_estimate

            # Check if this is a better path
            if total_travel_time < g_score[neighbour.name]:
                # Update best known path
                came_from[neighbour.name] = connection
                g_score[neighbour.name] = total_travel_time
                f_score[neighbour.name] = estimated_total_cost

                new_path = current_path + [neighbour]
                new_connections = current_connections + [connection]

                # Push to open set with new arrival time
                heapq.heappush(
                    open_set,
                    (
                        estimated_total_cost,
                        connection.end_time,
                        neighbour,
                        new_path,
                        new_connections,
                    ),
                )

    # No path found
    return None
