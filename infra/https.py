from enum import Enum, auto
import socket
import threading
from concurrent.futures import ThreadPoolExecutor
from typing import Callable
from OpenSSL import SSL


class HttpsServerStatus(Enum):
    Stopped = auto()
    Starting = auto()
    Started = auto
    Stopping = auto()


class HttpsServer:
    bind_addr = None
    cert = None
    key = None
    status = HttpsServerStatus.Stopped
    __thread = None

    def shutdown(self):
        pass

    def launch(self, on_request: Callable):

        ctx = SSL.Context(SSL.TLS_SERVER_METHOD)
        ctx.use_privatekey_file(self.key)
        ctx.use_certificate_file(self.cert)

        s = SSL.Connection(ctx, socket.socket())
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(self.bind_addr)
        s.listen(5)

        __thread = threading.Thread(target=self.__launch, args=(s, on_request))
        __thread.start()

    def __launch(self, server_socket: socket.socket, on_request: Callable):
        while True:
            c, _ = server_socket.accept()

            with ThreadPoolExecutor(3) as pool:
                pool.map(on_request, [c])
