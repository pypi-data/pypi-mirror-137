# Dumbtils

Dumb Utilities.

## Installation

With makefile:

1. Install python3 (3.6+) and pip3 in your OS.
2. Copy the `Makefile` in the repo.
3. Run `make` on the folder with the `Makefile` or pass the `Makefile` explicitely.

With pip:

1. Install python3 (3.6+) and pip3 in your OS.
2. Run `pip3 install dumbtils -U`.

Note: If new commands are not found after installing, try reloading shell or virtual environment.

## Commands

* `procmax`: Return max process per user.
* `timeprog <prog> [arg1, arg2, ...]`: Measure execution time in seconds of a command or program.
* `ucp <bufsize> <src_path> <dst_path>`: Copy a file with a custom buffer size.
* `tictoc`: Simulates a comunication between two subprocesses of C1 and C2.
* `bingonacci [-t]`: Sum a millions fibonacci numbers of the range [0, 19], `-t` flag to use threading mode.
