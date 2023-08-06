import os
import sys
import time
import signal
import subprocess

from . import _c1, _c2


def main():
    argv = sys.argv[1:]
    if argv:
        sys.exit("ArgvError: tictoc takes no argument")
    if sys.platform.startswith("win32"):
        python_cmd = "py"
        c1 = subprocess.Popen(f"{python_cmd} -u {_c1.__file__}", stdout=subprocess.PIPE, shell=True, creationflags=subprocess.CREATE_NEW_PROCESS_GROUP)
    else:
        python_cmd = "python3"
        c1 = subprocess.Popen([python_cmd, "-u", _c1.__file__], stdout=subprocess.PIPE, shell=False)
    c2 = subprocess.Popen(f"{python_cmd} -u {_c2.__file__}", stdin=c1.stdout, stdout=sys.stdout, shell=True)
    for _ in range(10):
        time.sleep(2)
        if sys.platform.startswith("linux"):
            os.kill(c1.pid, signal.SIGALRM)
        else:
            os.kill(c1.pid, signal.CTRL_BREAK_EVENT)
    c1.wait()
    c1.stdout.close()
    c2.wait()
    sys.exit()

if __name__ == '__main__':
    main()
