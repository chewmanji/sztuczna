from stop import Stop
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional
from connection import Connection
import time

VEHICLE_VELOCITY = 50  # km/h
TRANSFER_TIME = 1  # minutes
TRANSFER_PENALTY = 5  # minutes - possible delays resulting from making a line change (random accidents may occur)


@dataclass
class SearchResult:
    shortest_path: List[Stop]
    arrival_time: Optional[datetime] = None
    total_duration: Optional[timedelta] = None
    path_connections: List[Connection] = field(default_factory=list)
    transfers: Optional[int] = None


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKCYAN = "\033[96m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def my_strptime(time: str):
    try:
        return datetime.strptime(time, "%H:%M")
    except Exception:
        print(f"{bcolors.FAIL}Format of time must be HH:MM.{bcolors.ENDC}")
        exit(1)


def measure_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(
            f"{bcolors.FAIL}Execution time: {end_time - start_time} seconds{bcolors.ENDC}"
        )
        return result

    return wrapper


def print_result(result: Optional[SearchResult], start_time: datetime):
    if result is None:
        print("Nie znaleziono połączenia.")
        return

    print(f"{result.shortest_path[0].name} -> {result.shortest_path[-1].name}")
    print(f"Czas pojawienia się na przystanku: {start_time}")
    print(f"Czas dotarcia do celu: {bcolors.OKCYAN}{result.arrival_time}{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}Czas podróży: {result.total_duration}{bcolors.ENDC}")
    if result.transfers:
        print(f"{bcolors.WARNING}Liczba przesiadek: {result.transfers}{bcolors.ENDC}")

    print("\nLinie:")
    current_connection = result.path_connections[0]
    print(
        f"Wsiadamy w {current_connection.line} [{current_connection.start_time}] na [{current_connection.start_stop.name}]"
    )
    for i in range(1, len(result.path_connections)):
        next_connection = result.path_connections[i]
        if current_connection.line != next_connection.line:
            print(
                f"Wysiadamy z {current_connection.line} [{current_connection.end_time}] na [{current_connection.end_stop.name}]"
            )
            print(
                f"Wsiadamy w {next_connection.line} [{next_connection.start_time}] na [{next_connection.start_stop.name}]"
            )
        current_connection = next_connection
    print(
        f"Wysiadamy z {current_connection.line} [{current_connection.end_time}] na [{current_connection.end_stop.name}]"
    )

    # print("\nPrzystanki:")
    # for connection in result.path_connections:
    #     print(
    #         f"Linia {connection.line}: "
    #         f"{connection.start_stop.name} -> {connection.end_stop.name} "
    #         f"(Odjazd: {connection.start_time}, Przyjazd: {connection.end_time})"
    #     )


def calculate_transfers(connections: list[Connection]):
    transfers = 0
    for i in range(1, len(connections)):
        if connections[i - 1].line != connections[i].line:
            transfers += 1
    return transfers
