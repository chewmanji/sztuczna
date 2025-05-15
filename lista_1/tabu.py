from typing import List, Optional
from datetime import datetime
from stop import Stop
from connection import Connection
from dijkstra import dijkstra
from utils import SearchResult, measure_time, calculate_tabu_list_size, print_result


class TabuSearchRoutePlanner:
    def __init__(self, stops: dict[str, Stop], connections: List[Connection]):
        self.stops = stops
        self.connections = connections
        self.tabu_list_max_size = 100

    @measure_time
    def find_optimal_route(
        self,
        start_stop: Stop,
        stops_to_visit: List[str],
        start_time: datetime,
        max_iterations: int = 300000,
    ) -> Optional[List[Connection]]:
        # Initial solution generation
        current_solution = self._generate_initial_solution(
            start_stop, stops_to_visit, start_time
        )

        if current_solution is None:
            return None

        best_solution = current_solution

        tabu_list = []

        for _ in range(max_iterations):
            # Generate neighborhood solutions
            neighborhood = self._generate_neighborhood(current_solution)

            # Select best neighbor not in tabu list
            best_neighbor = None
            for neighbor in neighborhood:
                if neighbor not in tabu_list:
                    if best_neighbor is None or self._evaluate_solution(
                        neighbor
                    ) < self._evaluate_solution(best_neighbor):
                        best_neighbor = neighbor

            if best_neighbor is None:
                print("breaking mainloop")
                break

            # Update solutions
            current_solution = best_neighbor

            if self._evaluate_solution(current_solution) < self._evaluate_solution(
                best_solution
            ):
                best_solution = current_solution

            # Update tabu list
            tabu_list.append(current_solution)

        return best_solution

    @measure_time
    def find_optimal_route_constrained(
        self,
        start_stop: Stop,
        stops_to_visit: List[str],
        start_time: datetime,
        max_iterations: int = 300000,
    ) -> Optional[List[Connection]]:
        # Initial solution generation
        current_solution = self._generate_initial_solution(
            start_stop, stops_to_visit, start_time
        )

        if current_solution is None:
            return None

        best_solution = current_solution

        tabu_list = []

        for _ in range(max_iterations):
            # Generate neighborhood solutions
            neighborhood = self._generate_neighborhood(current_solution)

            # Select best neighbor not in tabu list
            best_neighbor = None
            for neighbor in neighborhood:
                if neighbor not in tabu_list:
                    if best_neighbor is None or self._evaluate_solution(
                        neighbor
                    ) < self._evaluate_solution(best_neighbor):
                        best_neighbor = neighbor

            if best_neighbor is None:
                print("breaking mainloop")
                break

            # Update solutions
            current_solution = best_neighbor

            if self._evaluate_solution(current_solution) < self._evaluate_solution(
                best_solution
            ):
                best_solution = current_solution

            # Update tabu list
            tabu_list.append(current_solution)
            # Constraint
            if len(tabu_list) > self.tabu_list_max_size:
                tabu_list.pop(0)

        return best_solution

    def _generate_initial_solution(
        self, start_stop: Stop, stops_to_visit: List[str], start_time: datetime
    ) -> Optional[List[Connection]]:
        current_stop = start_stop
        current_time = start_time
        route = []

        while stops_to_visit:
            # Find the nearest stop to visit
            next_stop_name = stops_to_visit[0]
            next_stop = self.stops[next_stop_name]

            # Find a route to the next stop
            multi_hop_route = dijkstra(current_stop, next_stop, current_time)

            if multi_hop_route is None:
                return None

            # Update route, current stop, and time
            route.extend(multi_hop_route.path_connections)
            current_stop = next_stop
            current_time = route[-1].end_time
            stops_to_visit.remove(current_stop.name)
            for stop in multi_hop_route.get_stops():
                if stop.name in stops_to_visit:
                    stops_to_visit.remove(stop.name)

        # Find route back to start stop
        return_route = dijkstra(current_stop, start_stop, current_time)

        if return_route is None:
            return None

        route.extend(return_route.path_connections)
        print_result(create_result(start_time, route), start_time)
        return route

    def _generate_neighborhood(
        self, solution: List[Connection]
    ) -> List[List[Connection]]:
        neighborhood = []

        # Swap adjacent connections
        for i in range(len(solution) - 1):
            neighbor = solution.copy()
            neighbor[i], neighbor[i + 1] = neighbor[i + 1], neighbor[i]
            neighborhood.append(neighbor)

        # Replace a connection with an alternative route
        for i in range(len(solution)):
            start_stop = solution[i].start_stop
            end_stop = solution[i].end_stop
            current_time = solution[i].start_time

            alternative_connections = [
                conn
                for conn in self.connections
                if (
                    conn.start_stop == start_stop
                    and conn.end_stop == end_stop
                    and conn.start_time >= current_time
                    and conn != solution[i]
                )
            ]

            for alt_conn in alternative_connections:
                neighbor = solution.copy()
                neighbor[i] = alt_conn
                neighborhood.append(neighbor)

        return neighborhood

    def _evaluate_solution(self, solution: List[Connection]) -> float:
        if not solution:
            return float("inf")

        # Check time constraints and route correctness
        current_time = solution[0].start_time
        current_stop = solution[0].start_stop

        for conn in solution:
            # Ensure connection starts after current time
            if conn.start_time < current_time:
                return float("inf")

            # Ensure connection starts from the previous stop
            if conn.start_stop != current_stop:
                return float("inf")

            current_stop = conn.end_stop
            current_time = conn.end_time

        # Total route duration
        return sum(conn.duration.total_seconds() for conn in solution)


def solve_route_planning_problem(
    stops: dict[str, Stop],
    connections: List[Connection],
    start_stop: Stop,
    stops_to_visit: List[str],
    start_time: datetime,
    is_constrained: bool = False,
) -> Optional[SearchResult]:
    planner = TabuSearchRoutePlanner(stops, connections)
    planner.tabu_list_max_size = calculate_tabu_list_size(stops_to_visit)

    connections_solution = None
    if is_constrained:
        connections_solution = planner.find_optimal_route_constrained(
            start_stop, stops_to_visit, start_time
        )
    else:
        connections_solution = planner.find_optimal_route(
            start_stop, stops_to_visit, start_time
        )

    if connections_solution is None:
        return None

    return create_result(start_time, connections_solution)


def create_result(
    start_time: datetime,
    connections_solution: List[Connection],
):
    shortest_path: dict[str, Stop] = {}
    for connection in connections_solution:
        start, end = connection.start_stop, connection.end_stop
        for stop in [start, end]:
            if stop.name not in shortest_path.keys():
                shortest_path[stop.name] = stop

    total_duration = connections_solution[-1].end_time - start_time

    return SearchResult(start_time, total_duration, connections_solution)
