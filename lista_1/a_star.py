# https://en.wikipedia.org/wiki/Vincenty%27s_formulae
from vincenty import vincenty
from stop import Stop
from datetime import datetime, timedelta
from typing import Optional
import heapq
from connection import Connection
from utils import (
    SearchResult,
    calculate_transfers,
    VEHICLE_VELOCITY,
    measure_time,
)
from sys import maxsize


def heuristic_time(
    stop: Stop,
    end_stop: Stop,
):
    distance = vincenty(
        (stop.lat, stop.lon),
        (end_stop.lat, end_stop.lon),
        miles=False,
    )

    if distance is None:
        raise Exception("Shouldn't happen")

    estimated_cost = distance / VEHICLE_VELOCITY

    return estimated_cost


@measure_time
def a_star_min_time(
    start_stop: Stop, end_stop: Stop, arrival_time: datetime, stops: list[Stop]
) -> Optional[SearchResult]:
    print(f"Średnia prędkość pojazdu: {VEHICLE_VELOCITY} km/h")
    # Priority queue to store stops to visit
    open_set: list[tuple[timedelta, datetime, Stop, list[Connection]]] = []

    # Keep track of the best known path to each stop
    g_score: dict[str, timedelta] = {s.name: timedelta.max for s in stops}
    g_score[start_stop.name] = timedelta(0)

    # Estimated total cost from start to end through this stop
    f_score: dict[str, timedelta] = {s.name: timedelta.max for s in stops}
    f_score[start_stop.name] = timedelta(hours=heuristic_time(start_stop, end_stop))

    # Initial queue entry: (f_score, arrival_time, stop)
    heapq.heappush(open_set, (f_score[start_stop.name], arrival_time, start_stop, []))

    while open_set:
        _, current_time, current_stop, current_connections = heapq.heappop(open_set)

        if current_stop.name == end_stop.name:
            return SearchResult(
                arrival_time=current_time,
                cost=current_time - arrival_time,
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

            # Check if this is a better path
            if total_travel_time < g_score[neighbour.name]:
                # Heuristic estimate to the end stop
                heuristic_estimate = timedelta(
                    hours=heuristic_time(neighbour, end_stop)
                )
                estimated_total_cost = total_travel_time + heuristic_estimate
                g_score[neighbour.name] = total_travel_time
                f_score[neighbour.name] = estimated_total_cost

                new_connections = current_connections + [connection]

                # Push to open set with new arrival time
                heapq.heappush(
                    open_set,
                    (
                        estimated_total_cost,
                        connection.end_time,
                        neighbour,
                        new_connections,
                    ),
                )

    return None


def heuristic_transfers(current_stop: Stop, end_stop: Stop) -> int:
    # Get all lines that depart from the current stop
    current_lines = current_stop.outbound_lines

    # Get all lines that arrive at the end stop
    end_lines = end_stop.inbound_lines

    # If there's a common line, we can reach the destination without transfers
    if current_lines.intersection(end_lines):
        return 0

    # Otherwise, we need at least 1 transfer
    # This is an admissible (never overestimates)
    return 1


@measure_time
def a_star_min_transfers(
    start_stop: Stop, end_stop: Stop, arrival_time: datetime, stops: list[Stop]
) -> Optional[SearchResult]:
    print(f"Średnia prędkość pojazdu: {VEHICLE_VELOCITY} km/h")
    # Priority queue to store stops to visit
    open_set: list[tuple[int, timedelta, datetime, Stop, list[Connection]]] = []

    # Keep track of the best known path to each stop
    g_score: dict[str, int] = {s.name: maxsize for s in stops}
    g_score[start_stop.name] = 0

    # Estimated total cost from start to end through this stop
    f_score: dict[str, int] = {s.name: maxsize for s in stops}
    f_score[start_stop.name] = heuristic_transfers(start_stop, end_stop)
    print(f"F score of initial stop = {f_score[start_stop.name]}")

    # Initial queue entry: (f_score, arrival_time, stop)
    heapq.heappush(
        open_set,
        (
            f_score[start_stop.name],
            timedelta(0),
            arrival_time,
            start_stop,
            [],
        ),
    )

    while open_set:
        (
            current_transfers,
            total_duration,
            current_time,
            current_stop,
            current_connections,
        ) = heapq.heappop(open_set)

        if current_stop.name == end_stop.name:
            return SearchResult(
                arrival_time=current_time,
                cost=current_transfers,
                path_connections=current_connections,
                transfers=calculate_transfers(current_connections),
            )

        # Explore outbound connections
        for connection in current_stop.outbounds:
            # Skip connections that start before current time
            if connection.start_time < current_time:
                continue

            is_transfer = False
            if len(current_connections) != 0:
                is_transfer = current_connections[-1].line != connection.line

            # new_current_time = current_time
            new_number_of_transfers = calculate_transfers(current_connections)

            if is_transfer:
                new_number_of_transfers += 1

            neighbour = connection.end_stop

            # Calculate waiting time and total travel time
            waiting_time = connection.start_time - current_time
            new_total_duration_time = (
                total_duration + waiting_time + connection.duration
            )

            # Check if this is a better path
            if new_number_of_transfers < g_score[neighbour.name]:
                heuristic_estimate = heuristic_transfers(neighbour, end_stop)
                estimated_total_cost = new_number_of_transfers + heuristic_estimate

                g_score[neighbour.name] = new_number_of_transfers
                f_score[neighbour.name] = estimated_total_cost

                new_connections = current_connections + [connection]

                # Push to open set with new arrival time
                heapq.heappush(
                    open_set,
                    (
                        estimated_total_cost,
                        new_total_duration_time,
                        connection.end_time,
                        neighbour,
                        new_connections,
                    ),
                )

    return None
