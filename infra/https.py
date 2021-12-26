from enum import Enum, auto
import socket
import threading
from typing import Callable
from OpenSSL import SSL

from infra.http.message import Parser, Request, Response


class HttpsServerStatus(Enum):
    Stop = auto()
    Start = auto()


def handle_request(conn: socket.socket, on_request: Callable[[Request], Response]):
    parser = Parser(conn)
    request = parser.parse()
    response = on_request(request)
    conn.sendall(response.to_bytes())
    conn.close()


class HttpsServer:
    bind_addr = None
    cert = None
    key = None
    status = HttpsServerStatus.Stop

    def shutdown(self):
        self.status = HttpsServerStatus.Stop

    def launch(self, on_request: Callable[[Request], Response]):
        self.status = HttpsServerStatus.Start
        ctx = SSL.Context(SSL.TLSv1_2_METHOD)
        ctx.use_privatekey_file(self.key)
        ctx.use_certificate_file(self.cert)

        s = SSL.Connection(ctx, socket.socket())
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(self.bind_addr)
        s.listen(5)

        t = threading.Thread(target=self.__launch, args=(s, on_request))
        t.start()

    def __launch(self, server_socket: socket.socket, on_request: Callable[[Request], Response]):
        while True:
            conn, _ = server_socket.accept()
            if self.status == HttpsServerStatus.Stop:
                return
            # with ThreadPoolExecutor() as pool:
            # pool.map(handle_request, [conn, on_request])
            # self.__handle_request(conn, on_request)
            handle_request(conn, on_request)
