from enum import Enum, auto

from infra.fsm import FiniteStateMachine


class Input(Enum):
    Dash = auto()
    Alpha = auto()
    Colon = auto()
    Cr = auto()
    Lf = auto()
    Blank = auto()
    BoundaryLike = auto()
    EndDash = auto()
    End = auto()


class State(Enum):
    End = auto()
    Boundary = auto()
    Cr0 = auto()
    Lf0 = auto()
    HeaderField = auto()
    Colon = auto()
    Blank = auto()
    HeaderValue = auto()
    Cr1 = auto()
    Lf1 = auto()
    Cr2 = auto()
    Lf2 = auto()
    Data = auto()
    DataToBoundary = auto()
    EndDash1 = auto()
    Cr3 = auto()
    Lf3 = auto()
    EndDash2 = auto()


class Output(Enum):
    EffectAppendBoundary = auto()
    EffectAppendHeaderField = auto()
    EffectAppendHeaderValue = auto()
    EffectAppendHeader = auto()
    EffectAppendData = auto()
    EffectAppendLikeBoundary = auto()
    EffectAppendPart = auto()
    EffectFormData = auto()


def FormDataFSM() -> FiniteStateMachine:
    return FiniteStateMachine(init=State.End, transition=[
        (State.End, Input.Dash, State.Boundary, Output.EffectAppendBoundary),
        (State.Boundary, Input.Alpha, State.Boundary, Output.EffectAppendBoundary),
        (State.Boundary, Input.Dash, State.Boundary, Output.EffectAppendBoundary),
        (State.Boundary, Input.Colon, State.Boundary, Output.EffectAppendBoundary),
        (State.Boundary, Input.Cr, State.Cr0, None),
        (State.Cr0, Input.Lf, State.Lf0, None),
        (State.Lf0, Input.Alpha, State.HeaderField, Output.EffectAppendHeaderField),
        (State.HeaderField, Input.Alpha, State.HeaderField,
         Output.EffectAppendHeaderField),
        (State.HeaderField, Input.Dash, State.HeaderField,
         Output.EffectAppendHeaderField),
        (State.HeaderField, Input.Colon, State.Colon, None),
        (State.Colon, Input.Blank, State.Blank, None),
        (State.Blank, Input.Alpha, State.HeaderValue, Output.EffectAppendHeaderValue),
        (State.Blank, Input.Dash, State.HeaderValue, Output.EffectAppendHeaderValue),
        (State.Blank, Input.Colon, State.HeaderValue, Output.EffectAppendHeaderValue),
        (State.HeaderValue, Input.Alpha, State.HeaderValue,
         Output.EffectAppendHeaderValue),
        (State.HeaderValue, Input.Dash, State.HeaderValue,
         Output.EffectAppendHeaderValue),
        (State.HeaderValue, Input.Colon, State.HeaderValue,
         Output.EffectAppendHeaderValue),
        (State.HeaderValue, Input.Blank, State.HeaderValue,
         Output.EffectAppendHeaderValue),
        (State.HeaderValue, Input.Cr, State.Cr1, Output.EffectAppendHeader),
        (State.Cr1, Input.Lf, State.Lf1, None),
        (State.Lf1, Input.Cr, State.Cr2, None),
        (State.Lf1, Input.Alpha, State.HeaderField, Output.EffectAppendHeaderField),
        (State.Cr2, Input.Lf, State.Lf2, None),
        (State.Lf2, Input.Alpha, State.Data, Output.EffectAppendData),
        (State.Lf2, Input.Dash, State.Data, Output.EffectAppendData),
        (State.Lf2, Input.Colon, State.Data, Output.EffectAppendData),
        (State.Lf2, Input.Cr, State.Data, Output.EffectAppendData),
        (State.Lf2, Input.Lf, State.Data, Output.EffectAppendData),
        (State.Lf2, Input.BoundaryLike, State.DataToBoundary,
         Output.EffectAppendLikeBoundary),
        (State.Data, Input.Alpha, State.Data, Output.EffectAppendData),
        (State.Data, Input.Dash, State.Data, Output.EffectAppendData),
        (State.Data, Input.Colon, State.Data, Output.EffectAppendData),
        (State.Data, Input.Blank, State.Data, Output.EffectAppendData),
        (State.Data, Input.Cr, State.Data, Output.EffectAppendData),
        (State.Data, Input.Lf, State.Data, Output.EffectAppendData),
        (State.Data, Input.BoundaryLike, State.DataToBoundary,
         Output.EffectAppendLikeBoundary),
        (State.DataToBoundary, Input.BoundaryLike,
         State.DataToBoundary, Output.EffectAppendLikeBoundary),
        (State.DataToBoundary, Input.Alpha, State.Data, Output.EffectAppendData),
        (State.DataToBoundary, Input.Dash, State.Data, Output.EffectAppendData),
        (State.DataToBoundary, Input.Colon, State.Data, Output.EffectAppendData),
        (State.DataToBoundary, Input.Blank, State.Data, Output.EffectAppendData),
        (State.DataToBoundary, Input.Cr, State.Data, Output.EffectAppendData),
        (State.DataToBoundary, Input.Lf, State.Data, Output.EffectAppendData),
        (State.DataToBoundary, Input.EndDash,
         State.EndDash1, Output.EffectAppendPart),
        (State.DataToBoundary, Input.Cr, State.Cr3, Output.EffectAppendPart),
        (State.Cr3, Input.Lf, State.Lf3, None),
        (State.Lf3, Input.Alpha, State.HeaderField, Output.EffectAppendHeaderField),
        (State.EndDash1, Input.EndDash, State.EndDash2, Output.EffectFormData),
        (State.EndDash2, Input.End, State.End, None)
    ])
