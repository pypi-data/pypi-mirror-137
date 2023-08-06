class FSMError(Exception):
    pass


class InitialStateNotProvidedError(FSMError):
    pass


class MultipleInitialStatesProvidedError(FSMError):
    pass


class EndStateNotProvidedError(FSMError):
    pass


class NoNextStateError(FSMError):
    pass
