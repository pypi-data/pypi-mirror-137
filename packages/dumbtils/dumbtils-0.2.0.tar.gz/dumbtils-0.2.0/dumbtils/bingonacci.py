import os
import sys
import math
import random
import multiprocessing


def fib(n):
    if n in {0, 1}:
        return n
    return fib(n - 1) + fib(n - 2)


def bingonacci(fib_range: tuple, addends_size: int):
    fibs = {}
    fib_range = range(fib_range)
    for i in fib_range:
        fibs[i] = fib(i)
    addends_size = addends_size
    sum_total = 0
    for _ in range(addends_size):
        sum_total += fibs[random.choice(fib_range)]
    return sum_total


def main():
    argv = sys.argv[1:]
    if len(argv) > 1:
        sys.exit("ArgvError: bingonacci [-t]")
    if argv and argv[0] != "-t":
        sys.exit("ArgvError: bingonacci only accepts -t flag as single argument")
    fib_range = 20
    addends_size = 1000000
    if not argv:
        print(bingonacci(fib_range, addends_size))
    else:
        # Python threading does not take more than 1 CPU, use multiprocessing instead.
        proc_num = max((os.cpu_count() or 0) - 1, 1)
        split_size = math.ceil(addends_size / proc_num)
        pool = multiprocessing.Pool(proc_num)
        print(sum(pool.starmap(bingonacci, [(fib_range, split_size) for _ in range(proc_num)])))
        pool.close()
    sys.exit()


if __name__ == '__main__':
    main()
