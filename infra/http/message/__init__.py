from infra.http.message.fsm import Input, Output, State, RequestMessageFSM
import socket

from infra.http.status import ReasonMap

HTTP_VERSION = "1.1"


class Message:
    headers: dict[str, str] = dict()
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
        for (key, value) in self.headers.items():
            msg += "{}: {}\r\n".format(key, value)
        msg += "\r\n"
        return msg.encode() + self.body


class Parser():
    machine = RequestMessageFSM()
    conn: socket.socket

    def __init__(self, conn: socket.socket) -> None:
        self.conn = conn

    def parse(self) -> Request:
        rest_body_size = 0
        body = bytes()
        headers = dict()
        header_field, header_value = bytes(), bytes()
        method, path, version = bytes(), bytes(), bytes()

        while True:
            current = self.conn.recv(1)
            input = None
            if rest_body_size == 0 and (self.machine.state == State.Lf2 or self.machine.state == State.Body):
                input = Input.End
            elif current == b' ':
                input = Input.Blank
            elif current == b':':
                input = Input.Colon
            elif current == b'\r':
                input = Input.Cr
            elif current == b'\n':
                input = Input.Lf
            else:
                input = Input.Alpha

            effect = self.machine.consume(input)

            if effect == Output.EffectAppendHeader:
                headers[header_field.decode()] = header_value.decode()
                header_field, header_value = bytes(), bytes()
            elif effect == Output.EffectAppendHeaderField:
                header_field += current
            elif effect == Output.EffectAppendHeaderValue:
                header_value += current
            elif effect == Output.EffectAppendMethod:
                method += current
            elif effect == Output.EffectAppendPath:
                path += current
            elif effect == Output.EffectAppendVersion:
                version += current
            elif effect != None:
                if effect == Output.EffectCheckEnd:
                    if "Content-Length" in headers:
                        rest_body_size = int(headers["Content-Length"])
                elif effect == Output.EffectAppendBody:
                    body += current
                    rest_body_size -= 1
                if rest_body_size == 0:
                    request = Request(
                        headers, method.decode(), path.decode(), body)
                    self.machine.consume(Input.End)
                    return request
