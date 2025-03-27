from stop import Stop
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional
from connection import Connection


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


def print_result(result: Optional[SearchResult], start_time: datetime):
    if result is None:
        print("Nie znaleziono połączenia.")
        return

    # print("Ścieżka:")
    # for stop in result.shortest_path:
    #     print(f"- {stop.name}")

    print(f"\nCzas pojawienia się na przystanku: {start_time}")
    print(f"Czas dotarcia do celu: {bcolors.OKCYAN}{result.arrival_time}{bcolors.ENDC}")
    print(f"{bcolors.OKGREEN}Czas podróży: {result.total_duration}{bcolors.ENDC}")
    if result.transfers:
        print(f"Liczba przesiadek: {result.transfers}")

    print("\nPrzystanki:")
    for connection in result.path_connections:
        print(
            f"Linia {connection.line}: "
            f"{connection.start_stop.name} -> {connection.end_stop.name} "
            f"(Odjazd: {connection.start_time}, Przyjazd: {connection.end_time})"
        )


def calculate_transfers(connections: list[Connection]):
    transfers = 0
    for i in range(1, len(connections)):
        if connections[i - 1].line != connections[i].line:
            transfers += 1
    return transfers
