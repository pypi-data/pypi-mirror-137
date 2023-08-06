import sys


def main():
    for (ind, line) in enumerate(iter(sys.stdin.readline, "")):
        print(f"{ind}:", line, end="")
    sys.exit()


if __name__ == '__main__':
    main()
