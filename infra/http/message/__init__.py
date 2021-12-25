from typing import Callable
import fsm
import socket

from infra.http.status import ReasonMap

HTTP_VERSION = "1.1"


class Message:
    headers: map[str, str] = map()
    version: str = HTTP_VERSION

    def __init__(self, headers) -> None:
        self.headers = headers


class Request(Message):
    method: str = ''
    path: str = ''
    body: bytes = bytes()

    def __init__(self, headers, method, path, body) -> None:
        super().__init__(headers)
        self.method = method
        self.path = path
        self.body = body


class Response(Message):
    code: int = 200
    body: bytes = bytes()

    def __init__(self, headers, code, body) -> None:
        super().__init__(headers)
        self.code = code
        self.body = body

    def to_bytes(self) -> bytes:
        msg = "HTTP/{} {} {}\r\n".format(self.version,
                                         self.code, ReasonMap[self.code])
        for (key, value) in self.headers:
            msg += "{}: {}\r\n".format(key, value)
        msg += "\r\n"
        return msg.encode() + self.body


class Parser():
    machine = fsm.RequestMessage
    conn: socket.socket

    def __init__(self, conn: socket.socket) -> None:
        self.conn = conn

    def parse(self) -> Request:
        b = self.conn.recv(1)[0]
        rest_body_size = 0
        body = bytes()
        headers = map()
        header_field, header_value, method, path, version = str(), str(), str(), str(), str()

        while True:
            input = None
            if rest_body_size == 0 and (self.machine.state == fsm.State.Lf2 or self.machine.state == fsm.State.Body):
                input = fsm.Input.End
            elif b == b' ':
                input = fsm.Input.Blank
            elif b == b':':
                input = fsm.Input.Colon
            elif b == b'\r':
                input = fsm.Input.Cr
            elif b == b'\n':
                input = fsm.Input.Lf
            else:
                input = fsm.Input.Alpha

            effect = self.machine.consume(input)
            if effect == fsm.Output.EffectAppendHeader:
                headers[header_field] = header_value
                header_field, header_value = str(), str()
            elif effect == fsm.Output.EffectAppendHeaderField:
                header_field += b
            elif effect == fsm.Output.EffectAppendHeaderValue:
                header_value += b
            elif effect == fsm.Output.EffectAppendMethod:
                method += b
            elif effect == fsm.Output.EffectAppendPath:
                path += b
            elif effect == fsm.Output.EffectAppendVersion:
                version += b
            else:
                if effect == fsm.Output.EffectCheckEnd:
                    rest_body_size = int(headers["Content-Length"])
                elif effect == fsm.Output.EffectAppendBody:
                    body += b
                    rest_body_size -= 1
                if rest_body_size == 0:
                    request = Request(headers, method, path, body)
                    self.machine.consume(fsm.Input.End)
                    return request


def consume(conn: socket.socket, on_data: Callable[[Request], Response]):
    parser = Parser(conn)
    request = parser.parse()
    response = on_data(request)
    conn.send(response.to_readable_buffer())
