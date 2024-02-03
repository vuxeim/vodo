import sys
import time


def bprint(*text: str, sleep: float = 0.03, sep: str = ' ', end: str = '\n') -> None:
    for char in sep.join(text):
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(sleep)
    sys.stdout.write(end)
    sys.stdout.flush()


def fprint(text: str) -> None:
    """ Fast print. Empty sep and end """
    bprint(text, sleep=0, sep='', end='')


def pprint(x: int, y: int, text: str) -> None:
    """ Print at position (x, y) """
    sys.stdout.write(f"\x1b7\x1b[{y};{x}f{text}\x1b8")
    sys.stdout.flush()


def eprint(text: str) -> None:
    sys.stderr.write(text)
    sys.stderr.flush()


def nice_time(time) -> str:
    """ Strip milliseconds from time string """
    return str(time).split(".", maxsplit=1)[0]


def clear_screen() -> None:
    sys.stdout.write("\x1b[2J")
    sys.stdout.flush()
