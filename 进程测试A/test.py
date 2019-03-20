from multiprocessing import Process
import os


from testA import runA

print("test",os.getpid())

runmain = Process(target= runA)
runmain.start()

