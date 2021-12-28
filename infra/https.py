from enum import Enum, auto
import socket
import threading
from typing import Callable
from OpenSSL import SSL

from infra.http.message import Parser, Request, Response

# https服务器的状态类
class HttpsServerStatus(Enum):
    Stop = auto()
    Start = auto()

# 解析请求报文，发送响应报文
# 参数：conn：socket实例 、on_request：可调用的方法（app/middleware.py 下的static_middleware函数返回的handle函数）
def handle_request(conn: socket.socket, on_request: Callable[[Request], Response]):
    parser = Parser(conn)
    request = parser.parse()
    response = on_request(request)
    conn.sendall(response.to_bytes())
    conn.close()

# 服务器类
class HttpsServer:
    bind_addr = None
    cert = None
    key = None
    status = HttpsServerStatus.Stop

    # 通过设置服务器状态关闭服务器    
    def shutdown(self):
        self.status = HttpsServerStatus.Stop

    # 在socket对象上wrap一层ssl，实现服务器端的https
    # 参数：on_request：可调用的方法（app/middleware.py 下的static_middleware函数返回的handle函数）
    def launch(self, on_request: Callable[[Request], Response]):
        self.status = HttpsServerStatus.Start

        # 调用openssl里的ssl模块，装载服务器证书和私钥
        ctx = SSL.Context(SSL.TLSv1_2_METHOD)
        ctx.use_privatekey_file(self.key)
        ctx.use_certificate_file(self.cert)

        # 调用openssl里的ssl模块，生成wrap了ssl的socket实例
        s = SSL.Connection(ctx, socket.socket())
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # socket绑定地址，并监听端口，等待连接
        s.bind(self.bind_addr)
        s.listen(5)

        # 生成线程，并开始运行，此处调用了_launch函数，并传入s、on_request作为参数
        t = threading.Thread(target=self.__launch, args=(s, on_request))
        t.start()
   
    # 被动接受客户端连接,建立连接，并调用handle_request函数处理请求
    # 参数：server_socket:socket实例、 on_request：可调用的方法（app/middleware.py 下的static_middleware函数返回的handle函数）
    def __launch(self, server_socket: socket.socket, on_request: Callable[[Request], Response]):
        while True:
            conn, _ = server_socket.accept()
            if self.status == HttpsServerStatus.Stop:
                return
            handle_request(conn, on_request)
