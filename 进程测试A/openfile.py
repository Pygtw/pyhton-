import os

# ---1
# 切换路径
# pwd = os.getcwd()
# addr = pwd.split('/')
# newpwd = addr[:-1]
# npwd = "/".join(newpwd)
# os.chdir(npwd + '/qiehuan')

# pwd = os.getcwd()
# print("修改后的路径",pwd)

# ----2
# fileName = '/客户端图片缓存/' + '缓存图.jpg'
# try:
#     open(fileName,'wb')
#     print('打开文件成功!')
# except Exception:
#     print("打开文件失败!")

print(os.path.realpath(__file__))
print(os.path.abspath(__file__))
