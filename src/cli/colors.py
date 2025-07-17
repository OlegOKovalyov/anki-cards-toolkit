# src/cli/colors.py

class Color:
    PURPLE = "\033[95m"
    CYAN = "\033[36m"
    DARKCYAN = "\033[36m"
    BLUE = "\033[94m"
    GREEN = "\033[92m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"
    END = "\033[0m"


def purple(text: str) -> str:
    return f"{Color.PURPLE}{text}{Color.END}"

def yellow(text: str) -> str:
    return f"{Color.YELLOW}{text}{Color.END}"

def green(text: str) -> str:
    return f"{Color.GREEN}{text}{Color.END}"

def cyan(text: str) -> str:
    return f"{Color.CYAN}{text}{Color.END}"

def red(text: str) -> str:
    return f"{Color.RED}{text}{Color.END}"
