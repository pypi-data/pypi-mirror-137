import sys

from .common import execute


def main():
    argv = sys.argv[1:]
    if argv:
        sys.exit("ArgvError: bingonacci takes no argument")
    
    sys.exit()


if __name__ == '__main__':
    main()
