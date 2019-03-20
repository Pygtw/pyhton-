"""
集成主运行程序
"""
from server import ServerRun
from fileServer import FileRun
from pictureServer import PictureRun
from gameServer import GameRun
from multiprocessing import Process

# 服务器进程运行列表
l = []

p1 = Process(target=ServerRun)
p2 = Process(target=FileRun)
p3 = Process(target=PictureRun)
p4 = Process(target=GameRun)

l.append(p1)
l.append(p2)
l.append(p3)
l.append(p4)
for i in l:
    i.start()
