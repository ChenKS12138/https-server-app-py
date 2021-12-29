from enum import Enum

# 定义状态机异常类


class FiniteStateMachineException(Exception):
    pass

# 定义状态机父类


class FiniteStateMachine:
    state: Enum
    transition = None  # current, input, next, output

    def __init__(self, init: Enum, transition) -> None:
        self.state = init
        self.transition = transition

    # 定义consume函数，通过传入的input参数进行状态跳转，并返回output
    def consume(self, input: Enum) -> Enum:
        for (current, condition, next, output) in self.transition:
            if current == self.state and input == condition:
                self.state = next
                return output
        raise FiniteStateMachineException()
