from enum import Enum, auto


class HttpMethodException(Exception):
    pass


class Method(Enum):
    Get = auto()
    Post = auto()
    Put = auto()
    Delete = auto()
    Options = auto()
    Head = auto()
    Trace = auto()
    Connect = auto()
    Patch = auto()


def get_method(method: Method) -> str:
    return {
        Method.Get: "GET",
        Method.Post: "POST",
        Method.Put: "PUT",
        Method.Delete: "DELETE",
        Method.Options: "OPTIONS",
        Method.Head: "HEAD",
        Method.Trace: "TRACE",
        Method.Connect: "CONNECT",
        Method.Patch: "PATCH"
    }[method]
