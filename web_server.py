"""
web server 程序
完成一个类，提供给使用者
使用可通过这个类可以快速搭建web 后端服务，用于展示自己的网页

IO多路复用和http训练
"""
from socket import *
from select import select
import re

class WebServer:
    def __init__(self,host="0.0.0.0",port=8000,html=None):
        self.host = host
        self.port = port
        self.html = html
        self.address = (host,port)
        #IO多路复用准备工作
        self._rlist=[]
        self._wlist=[]
        self._xlist=[]
        # 创建套接字
        self.create_socket()
        self.bind()

    # 创建套接字
    def create_socket(self):
        self.sock = socket()
        self.sock.setblocking(False)

    # 绑定地址
    def bind(self):
        self.sock.bind((self.host,self.port))

    # 启动函数，启动整个服务 --> 客户端可以发起链接
    def start(self):
        self.sock.listen(5)
        print("Listen to the port %d"%self.port)
        # IO 多路复用
        self.rlist.append(self.sock)#关注监听套接字
        while True:
            rs,ws,xs=select(self._rlist,self._wlist,self._xlist)
            for r in rs:
                if r is self.sock:
                    connfd,addr=r.accept()
                    connfd.setblocking(False)
                    self._rlist.append(connfd)
                else:
                    data=r.recv(1024)
                    if not data:
                        self._rlist.remove(r)
                        r.close()
                        continue
                    print(data.decode())
                    self._wlist.append(r)

                    pattern="[A-Z]+\s+(?P<info>/\s*)"
                    result=re.match(pattern,data)
                    if result:
                        info=result.group("info")

            for w in ws:
                w.send(b"OK")
                self._wlist.remove(w)

            for x in xs:
                pass




if __name__ == '__main__':
    # 使用者应该怎么用我这个类

    # 什么东西应该是用户确定的，通过参数传入
    # 地址  要展示什么网页

    httpd = WebServer(host="0.0.0.0",port=8000,html="./static")
    httpd.start()