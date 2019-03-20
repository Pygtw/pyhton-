import os
import sys
from time import sleep
import time
import threading


def runA():
    print("runA", os.getpid())
    print("A启动成功!")
    print("runA-ppid", os.getppid())

    def runAA():
        print("runAA", os.getpid())

        print("AA线程开启成功!")
        while 1:
            sleep(3)
            print("AAA")
        print("线程结束")

    p = threading.Thread(target=runAA)
    p.start()
    p.join()
