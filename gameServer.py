'''
    游戏准备功能
    游戏服务器, 狼人杀游戏功能
'''
import socket
import threading
import time
import os
import os.path
import json
import random
from time import sleep
from multiprocessing import Process


def GameRun(conn=None):

    def distributeRole():
        role = ['狼人', '狼人', '平民', '平民', '平民', '女巫', '上帝']
        user = ['1号玩家', '2号玩家', '3号玩家', '4号玩家', '5号玩家', '6号玩家', '7号玩家']
        user = user[::-1]
        # 角色分配列表
        users = []

        # 将角色序列随机重置
        def randomrole():
            random.shuffle(role)
            # 给users 分配角色
            for i in user:
                # 弹出role列表中元素
                i += '-'+role.pop()
                users.append(i)
            return users

        # 得到随机分配的角色列表roles
        roles = randomrole()

        return roles

    def gameServer():

        IP = ''
        PORT = 50010   # 此端口开启浪人杀游戏
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((IP, PORT))
        s.listen(5)

        # 获取角色列表
        Roles = distributeRole()
        gamerole = []
        # 处理游戏客户端连接消息

        def sendrole(conn, addr, currole):

            print("新连接", addr)
            # 游戏规则
            youxiguize = [
                '游戏开始',
                '天黑请闭眼',
                '狼人玩家睁眼,请选择击杀',
                '女巫请睁眼,是否救人',
                '预言家请睁眼,你要查验的人是',
                '天亮了,请发言',
                '开始投票',
            ]

            conn.send(("\n系统为你分配的角色为:%s\n" % currole).encode())
            print("%s角色为%s" % (addr, currole))
            print(gamerole)
            while 1:
                
                if len(gamerole) == 2:
                    for m in youxiguize:
                        conn.send(("%s\n" % m).encode())
                        sleep(2)
                    conn.send("游戏结束".encode())
                    conn.close()
                    return

        # 处理游戏逻辑
        def handle(conn, addr):
            while 1:
                data = conn.recv(1024).decode()
                print("游戏服务器接受到的消息,处理文字请求", data)


        print('游戏服务器启动成功,端口号:50010!')
        while True:
            conn, addr = s.accept()
            data = conn.recv(1024).decode()

            print("接受到的消息为:", data)
            if data == "ready":
                # 保存当连接的客户端用户的角色到角色列表
                currole = Roles.pop()
                # 将角色保存到角色列表中
                gamerole.append((conn,currole))
                # 发角色
                t = threading.Thread(target=sendrole, args=(conn, addr,currole))
                t.start()
            else:
                print("开启新进程处理消息函数,并做系统处理")
                receive = Process(target=handle, args=(conn, addr))
                receive.start()

        s.close()

    # 开启游戏
    gameServer()
