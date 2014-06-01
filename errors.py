class FSMError(Exception) :
    pass


class FSMStartStatesError(FSMError) :
    def __str__(self) :
        return "Error - Only one start state is allowed for this FSM."


class FSMNoStartStateError(FSMError) :
    def __str__(self) :
        return "Error - No start state defined for this FSM."


class FSMFinalStateError(FSMError) :
    def __str__(self) :
        return "Error - No final state/s defined for this FSM."


class FSMUnimplementedInput(FSMError) :
    def __str__(self) :
        return "Error - The read_symbol() method must be implemented."


class FSMRejectedInput(Exception) :
    def __init__(self, symbol) :
        self._symbol = symbol

    def __str__(self) :
        return "'%s' is not a recognized symbol by this FSM." % self._symbol


class FSMEndOfInput(Exception) :
    def __str__(self) :
        return "No more symbols available. FSM reached input end."


class FSMDuplicatedState(Exception) :
    def __init__(self, state) :
        self._state = state

    def __str__(self) :
        return "Error - The state : '%s' is already defined." % self._state.id


class FSMDuplicatedTransition(Exception) :
    def __init__(self, transition) :
        self._transition = transition

    def __str__(self) :
        return "Error - There's already a transition from '%s' to '%s' with the same function." % self._transition.from_state.id, self._transition.to_state.id
