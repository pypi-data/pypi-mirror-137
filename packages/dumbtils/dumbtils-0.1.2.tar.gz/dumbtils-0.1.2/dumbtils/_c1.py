import sys
import signal
import time
from functools import partial


def handler(counters, signum, *args):
    print(f"C1 received signal {signum}")
    counters["i"] += 1
    if counters["i"] == 10:
        sys.exit()


def main():
    counters = {"i": 0}
    if sys.platform.startswith("linux"):
        signal.signal(signal.SIGALRM, partial(handler, counters))
    else:
        signal.signal(signal.SIGBREAK, partial(handler, counters))
    while True:
        pass


if __name__ == '__main__':
    main()
