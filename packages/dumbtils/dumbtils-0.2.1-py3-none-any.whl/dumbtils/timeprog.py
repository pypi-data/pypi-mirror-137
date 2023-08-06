import sys
import time

from .common import execute


def main():
    argv = sys.argv[1:]
    begin = time.monotonic()
    execute(" ".join(argv))
    end = time.monotonic()
    print(end - begin)
    sys.exit()


if __name__ == '__main__':
    main()
