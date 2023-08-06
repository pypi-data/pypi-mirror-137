import os
import sys


def main():
    argv = sys.argv[1:]
    if len(argv) != 3:
        sys.exit("ArgvError: ucp <bufsize> <src_path> <dst_path>")
    if not argv[0].isdigit():
        sys.exit("ArgvError: bugsize must be int")
    bufsize = int(argv[0])
    if bufsize < 1:
        sys.exit("ArgvError: bugsize must be greater than 0")
    # Python buffer size of 1 means line buffering, using 2 as minimum
    bufsize = max(int(argv[0]), 2)
    src_path = argv[1]
    dst_path = argv[2]
    if dst_path.endswith(os.sep):
        dst_path += src_path.split(os.sep)[-1]
    with open(src_path, "rb", buffering=bufsize) as src:
        with open(dst_path, "wb+", buffering=bufsize) as dst:
            while True:
                chunk = src.read(bufsize)  
                if not chunk:
                    break
                dst.write(chunk)
    sys.exit()


if __name__ == '__main__':
    main()
