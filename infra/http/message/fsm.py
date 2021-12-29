from enum import Enum, auto

from infra.fsm import FiniteStateMachine


class Input(Enum):
    Blank = auto()
    Colon = auto()
    Cr = auto()
    Lf = auto()
    Alpha = auto()
    End = auto()


class State(Enum):
    End = auto()
    Method = auto()
    Blank0 = auto()
    Path = auto()
    Blank1 = auto()
    Version = auto()
    Cr0 = auto()
    Lf0 = auto()
    HeaderField = auto()
    Colon0 = auto()
    Blank2 = auto()
    HeaderValue = auto()
    Cr1 = auto()
    Lf1 = auto()
    Cr2 = auto()
    Lf2 = auto()
    Body = auto()


class Output(Enum):
    EffectAppendMethod = auto()
    EffectAppendPath = auto()
    EffectAppendVersion = auto()
    EffectAppendHeaderField = auto()
    EffectAppendHeaderValue = auto()
    EffectAppendHeader = auto()
    EffectCheckEnd = auto()
    EffectAppendBody = auto()


# 根据请求报文格式，返回一个解析请求报文的状态机
def RequestMessageFSM() -> FiniteStateMachine:
    return FiniteStateMachine(init=State.End, transition=[
        (State.End, Input.Alpha, State.Method, Output.EffectAppendMethod),
        (State.Method, Input.Alpha, State.Method,  Output.EffectAppendMethod),
        (State.Method, Input.Blank, State.Blank0, None),
        (State.Blank0, Input.Alpha, State.Path, Output.EffectAppendPath),
        (State.Path, Input.Alpha, State.Path, Output.EffectAppendPath),
        (State.Path, Input.Blank, State.Blank1, None),
        (State.Blank1, Input.Alpha, State.Version, Output.EffectAppendVersion),
        (State.Version, Input.Alpha, State.Version, Output.EffectAppendVersion),
        (State.Version, Input.Cr, State.Cr0, None),
        (State.Cr0, Input.Lf, State.Lf0, None),
        (State.Lf0, Input.Alpha, State.HeaderField, Output.EffectAppendHeaderField),
        (State.HeaderField, Input.Alpha, State.HeaderField,
         Output.EffectAppendHeaderField),
        (State.HeaderField, Input.Colon, State.Colon0, None),
        (State.Colon0, Input.Blank, State.Blank2, None),
        (State.Blank2, Input.Alpha, State.HeaderValue,
         Output.EffectAppendHeaderValue),
        (State.HeaderValue, Input.Alpha, State.HeaderValue,
         Output.EffectAppendHeaderValue),
        (State.HeaderValue, Input.Blank, State.HeaderValue,
         Output.EffectAppendHeaderValue),
        (State.HeaderValue, Input.Colon, State.HeaderValue,
         Output.EffectAppendHeaderValue),
        (State.HeaderValue, Input.Cr, State.Cr1, Output.EffectAppendHeader),
        (State.Cr1, Input.Lf, State.Lf1, None),
        (State.Lf1, Input.Alpha, State.HeaderField, Output.EffectAppendHeaderField),
        (State.Lf1, Input.Cr, State.Cr2, None),
        (State.Cr2, Input.Lf, State.Lf2, Output.EffectCheckEnd),
        (State.Lf2, Input.Alpha, State.Body, Output.EffectAppendBody),
        (State.Lf2, Input.End, State.End, None),
        (State.Body, Input.Alpha, State.Body, Output.EffectAppendBody),
        (State.Body, Input.Blank, State.Body, Output.EffectAppendBody),
        (State.Body, Input.Colon, State.Body, Output.EffectAppendBody),
        (State.Body, Input.Cr, State.Body, Output.EffectAppendBody),
        (State.Body, Input.Lf, State.Body, Output.EffectAppendBody),
        (State.Body, Input.End, State.End, None)
    ])


#    POST / HTTP/1.1
#    Host: localhost:3000
#    User-Agent: curl/7.64.1
#    Accept: */*
#    Content-Length: 667
#    Content-Type: multipart/form-data; boundary=------------------------8e38e4e574a9351c

#    --------------------------8e38e4e574a9351c
#    Content-Disposition: form-data; name="file"; filename="aria2.conf"
#    Content-Type: application/octet-stream

#    # rpc-user=chenks
#    # rpc-passwd=749923710
#    rpc-secret=token
#    enable-rpc=true
#    rpc-allow-origin-all=true
#    rpc-listen-all=true
#    max-concurrent-downloads=5
#    continue=true
#    max-connection-per-server=5
#    min-split-size=10M
#    split=10
#    max-overall-download-limit=0
#    max-download-limit=0
#    max-overall-upload-limit=0
#    max-upload-limit=0
#    dir=/Users/brucezhou/movie
#    file-allocation=prealloc
#    --------------------------8e38e4e574a9351c
#    Content-Disposition: form-data; name="name"

#    cattchen
#    --------------------------8e38e4e574a9351c--
