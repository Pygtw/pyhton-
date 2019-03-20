'''
    文件功能    
    发送文件的缓存服务器
'''
import socket
import threading
import queue
import json  # json.dumps(some)打包   json.loads(some)解包
import time
import os
import os.path


def FileRun():
    # 获取文件绝对路径
    path = os.path.realpath(__file__)
    pathlist = path.split("/")
    path = "/".join(pathlist[:-1])

    os.chdir(path)  # 把运行文件设为当前工作路径
    IP = ''
    PORT = 50008
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print("文件服务器启动成功,端口号:50008！")
    s.bind((IP, PORT))
    s.listen(3)

    def tcp_connect(conn, addr):
        print('Connected by: ', addr)

        while True:
            data = conn.recv(1024)
            data = data.decode()
            if data == 'quit':
                print('Disconnected from {0}'.format(addr))
                break
            order = data.split()[0]  # 获取动作
            recv_func(order, data)

        conn.close()

    # 传输当前目录列表
    def sendList():
        listdir = os.listdir(os.getcwd())
        listdir = json.dumps(listdir)
        conn.sendall(listdir.encode())

    # 发送文件函数
    def sendFile(message):
        name = message.split()[1]  # 获取第二个参数(文件名)
        fileName = '/' + name
        with open(fileName, 'rb') as f:
            while True:
                a = f.read(1024)
                if not a:
                    break
                conn.send(a)
        time.sleep(0.1)  # 延时确保文件发送完整
        conn.send('EOF'.encode())

    # 保存上传的文件到当前工作目录
    def recvFile(message):
        name = message.split()[1]  # 获取文件名
        fileName = '/' + name
        with open(fileName, 'wb') as f:
            while True:
                data = conn.recv(1024)
                if data == 'EOF'.encode():
                    break
                f.write(data)

    # 切换工作目录
    def cd(message):
        message = message.split()[1]  # 截取目录名

        # 如果是新连接或者下载上传文件后的发送则 不切换 只将当前工作目录发送过去
        if message != 'same':

            f = '/' + message
            pwd = os.getcwd()
            addr = pwd.split('/')
            newpwd = addr[:-1]
            npwd = "/".join(newpwd)
            os.chdir(npwd + f)
            # os.chdisers[i][0].send(data.encode())r(f)

        path = ''
        path = os.getcwd().split('/')  # 当前工作目录
        for i in range(len(path)):
            if path[i] == 'resources':
                break
        pat = ''
        for j in range(i, len(path)):
            pat = pat + path[j] + ' '
        pat = '/'.join(pat.split())

        # 如果切换目录超出范围则退回切换前目录
        if not 'resources' in path:
            f = '/resources'

            pwd = os.getcwd()
            addr = pwd.split('/')
            newpwd = addr[:-1]
            npwd = "/".join(newpwd)
            os.chdir(npwd + f)

            print(os.getcwd())
            pat = 'resources'
        conn.send(pat.encode())

    # 判断输入的命令并执行对应的函数
    def recv_func(order, message):
        if order == 'get':
            return sendFile(message)
        elif order == 'put':
            return recvFile(message)
        elif order == 'dir':
            return sendList()
        elif order == 'pwd':
            return pwd()
        elif order == 'cd':
            return cd(message)

    while True:
        conn, addr = s.accept()
        t = threading.Thread(target=tcp_connect, args=(conn, addr))
        t.start()
    s.close()

    serv2 = threading.Thread(target=fileServer)
    serv2.start()
    serv2.join()
