import sys
import time

from .common import execute


def main():
    argv = sys.argv[1:]
    begin = time.monotonic()
    execute(argv)
    end = time.monotonic()
    print(f"Exited in {end - begin}s")
    sys.exit()


if __name__ == '__main__':
    main()
