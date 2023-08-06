from abc import abstractmethod
from enum import Enum
from typing import Type


class StateType(Enum):
    INITIAL = "Initial"
    STANDARD = "Standard"
    END = "End"


StateCollection = dict[str, Type["BaseState"]]


class BaseState:
    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    @staticmethod
    @abstractmethod
    def type() -> StateType:  # pragma: no cover
        pass

    @abstractmethod
    async def transit(
        self, states: StateCollection
    ) -> Type["BaseState"]:  # pragma: no cover
        pass
