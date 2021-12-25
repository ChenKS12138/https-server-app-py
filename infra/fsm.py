from typing import List, Optional

from enum import Enum


class FiniteStateMachineException(Exception):
    pass


class FiniteStateMachine:
    state: Enum
    transition: List[(Enum, Enum, Enum, Optional[Enum])
                     ] = None  # current, input, next, output

    def __init__(self, init: Enum, transition: List[(Enum, Enum, Enum, Optional[Enum])]) -> None:
        self.state = init
        self.transition = transition

    def consume(self, input: Enum) -> Enum:
        for (current, condition, next, output) in self.transition:
            if current == self.state and input == condition:
                self.state = next
                return output
        raise FiniteStateMachineException()
