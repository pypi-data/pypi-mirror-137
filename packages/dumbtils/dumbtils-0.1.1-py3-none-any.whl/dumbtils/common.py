import subprocess


def execute(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True, shell=True)
    for stdout_line in iter(popen.stdout.readline, ""):
        print(stdout_line, end="") 
    popen.stdout.close()
    return popen.wait()
