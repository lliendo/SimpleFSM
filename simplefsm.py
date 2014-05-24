from abc import ABCMeta, abstractmethod
from errors import *


class State(object) :
    def __init__(self, id) :
        self._id = id
        self._start_state = False
        self._final_state = False

    @property
    def id(self) :
        return self._id

    @property
    def start_state(self) :
        return self._start_state

    @start_state.setter
    def start_state(self, start_state) :
        self._start_state = start_state

    @property
    def final_state(self) :
        return self._final_state

    @final_state.setter
    def final_state(self, final_state) :
        self._final_state = final_state

    def transit(self, fsm) :
        symbol = fsm.read_symbol()

        try :
            transition = filter(lambda t: t.from_state.id == self.id \
                and t.applies(symbol), fsm.transitions).pop()
        except IndexError :
            raise FSMRejectedInput(symbol)

        fsm.state = transition.to_state
        return symbol

    def __eq__(self, other) :
        return self.id == other.id


class Transition(object) :
    def __init__(self, from_state, to_state, transition_function) :
        self._from_state = from_state
        self._to_state = to_state
        self._transition_function = transition_function

    @property
    def from_state(self) :
        return self._from_state

    @property
    def to_state(self) :
        return self._to_state

    @property
    def transition_function(self) :
        return self._transition_function

    def applies(self, symbol) :
        return self._transition_function(symbol)

    def __eq__(self, other) :
        return self.from_state == other.from_state \
            and self.to_state == other.to_state \
            and self.transition_function == other.transition_function


class SimpleFSM(object) :
    __metaclass__ = ABCMeta

    def __init__(self) :
        self._states = []
        self._transitions = []
        self._accepted_symbols = []
        self._final_states = None
        self._current_state = None
        self._remaining_input = True

    @property
    def transitions(self) :
        return self._transitions

    @property
    def state(self) :
        return self._state

    @state.setter
    def state(self, state) :
        self._state = state

    def add_state(self, state) :
        if state in self._states :
            raise FSMDuplicatedState(state)
        
        self._states.append(state)

    def add_states(self, states) :
        [self.add_state(s) for s in states]

    def add_transition(self, transition) :
        if transition in self._transitions :
            raise FSMDuplicatedTransition(transition)
        
        self._transitions.append(transition)

    def add_transitions(self, transitions) :
        [self.add_transition(t) for t in transitions]

    @abstractmethod
    def read_symbol(self, *args, **kwargs) :
        pass

    def _set_initial_state(self) :
        if len(filter(lambda s: s.start_state, self._states)) > 1 :
            raise FSMStartStatesError()

        try :
            self._current_state = filter(lambda s: s.start_state, self._states).pop()
        except IndexError :
            raise FSMNoStartStateError()

    def _set_final_states(self) :
        self._final_states = filter(lambda s: s.final_state, self._states)

        if not self._final_states :
            raise FSMFinalStateError()

    def _set_states(self) :
        self._accepted_symbols = []
        self._set_initial_state()
        self._set_final_states()

    def run(self) :
        self._set_states()

        while (self._current_state not in self._final_states) and self._remaining_input :
            try :
                self._accepted_symbols.append(self._current_state.transit(self))
            except FSMEndOfInput :
                self._remaining_input = False

        return self._accepted_symbols
