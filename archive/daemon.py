import os
import sys
import time
import subprocess

def main():
    while 1:
        print("Scanning for devices...")
        p = subprocess.Popen(['python', 'main.py'])
        returncode = p.wait()
        if returncode == 1:
            print("Rescan selected.")
        # elif returncode == 2:
        #     print("Connecting...")
        #     p = subprocess.Popen(['python', 'subroutine.py'])
        #     returncode = p.wait()
        else:
            break
    print("Program exited.")
    return 0

if __name__ == "__main__":
    sys.exit(main())