class FSMError(Exception):
    pass


class FSMStartStatesError(FSMError):
    def __str__(self):
        return "Error - Only one start state is allowed for this FSM."


class FSMNoStartStateError(FSMError):
    def __str__(self):
        return "Error - No start state defined for this FSM."


class FSMFinalStateError(FSMError):
    def __str__(self):
        return "Error - No final state/s defined for this FSM."


class FSMUnimplementedInput(FSMError):
    def __str__(self):
        return "Error - The read_symbol() method must be implemented."


class FSMRejectedInput(FSMError):
    def __init__(self, symbol):
        self._symbol = symbol

    def __str__(self):
        return "'{0}' is not a recognized symbol by this FSM.".format(self._symbol)


class FSMEndOfInput(FSMError):
    def __str__(self):
        return "No more symbols available. FSM reached input end."


class FSMDuplicatedState(FSMError):
    def __init__(self, state):
        self._state = state

    def __str__(self):
        return "Error - The state : '{0}' is already defined.".format(self._state.id)


class FSMDuplicatedTransition(FSMError):
    def __init__(self, transition):
        self._transition = transition

    def __str__(self):
        return "Error - There's already a transition from '{0}' to '{1}' with the same function.".format(self._transition.from_state.id, self._transition.to_state.id)
