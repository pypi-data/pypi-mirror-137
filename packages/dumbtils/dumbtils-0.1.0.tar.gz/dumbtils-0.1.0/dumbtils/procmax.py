import sys

from .common import execute


def main():
    argv = sys.argv[1:]
    if argv:
        sys.exit("ArgvError: procmax takes no argument")
    if sys.platform.startswith("linux"):
        execute(["ulimit", "-u"])
    else:
        print("unlimited")
    sys.exit()


if __name__ == '__main__':
    main()
