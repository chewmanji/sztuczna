from datetime import datetime


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
