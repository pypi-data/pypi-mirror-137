from abc import abstractmethod
from typing import Iterable, Type, AsyncGenerator

from datek_async_fsm.errors import (
    InitialStateNotProvidedError,
    MultipleInitialStatesProvidedError,
    EndStateNotProvidedError,
    NoNextStateError,
)
from datek_async_fsm.state import BaseState, StateCollection, StateType


class BaseFSM:
    def __init__(self, state_classes: Iterable[Type[BaseState]], **kwargs):
        _validate_state_classes(state_classes)
        initial_state_classes = _get_initial_states(state_classes)
        self._current_state_class = initial_state_classes[0]

        self._state_classes: StateCollection = {
            state.__name__: state for state in state_classes
        }

        self.__dict__.update(kwargs)

    @property
    def current_state(self) -> Type[BaseState]:
        return self._current_state_class

    async def run(self):
        # noinspection PyTypeChecker
        input_generator: AsyncGenerator = self._input_generator()
        state_generator = self._state_generator()
        async for _ in state_generator:
            input_ = await input_generator.__anext__()
            await state_generator.asend(input_)

        await input_generator.aclose()

    async def _state_generator(self):
        while self._current_state_class.type() is not StateType.END:
            kwargs = (yield) or {}
            current_state = self._current_state_class(**kwargs)

            if not (
                next_state_class := await current_state.transit(self._state_classes)
            ):
                raise NoNextStateError

            self._current_state_class = next_state_class
            yield

    @abstractmethod
    async def _input_generator(self) -> AsyncGenerator[dict, None]:  # pragma: no cover
        pass


def _validate_state_classes(states: Iterable[Type[BaseState]]):
    initial_state_classes = _get_initial_states(states)

    if not initial_state_classes:
        raise InitialStateNotProvidedError

    if len(initial_state_classes) > 1:
        raise MultipleInitialStatesProvidedError

    end_state_classes = list(
        filter(lambda state: state.type() is StateType.END, states)
    )

    if not end_state_classes:
        raise EndStateNotProvidedError


def _get_initial_states(states) -> list[Type[BaseState]]:
    return list(filter(lambda state: state.type() is StateType.INITIAL, states))
