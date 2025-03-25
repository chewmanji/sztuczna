import argparse
from utils import my_strptime


parser = argparse.ArgumentParser(
    prog="JakDojadeBiedaWersja",
    description="Finding optimal connections between 2 stops using Dijkstra and A* algorithms",
)


parser.add_argument("start_stop", type=str)
parser.add_argument("end_stop", type=str)
parser.add_argument(
    "start_time",
    type=my_strptime,
    help="Format of time is HH:MM.",
)
parser.add_argument(
    "-c",
    "--criterion",
    choices=["time", "changes"],
    default="time",
    help="The criterion on the basis of which the algorithm optimizes the function (default = time).",
)
