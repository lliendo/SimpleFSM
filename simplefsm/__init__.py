# -*- coding: utf-8 -*-

"""
This file is part of SimpleFSM.

SimpleFSM is free software: you can redistribute it and/or modify
it under the terms of the GNU Lesser General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

SimpleFSM is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
Lesser GNU General Public License for more details.

You should have received a copy of the Lesser GNU General Public License
along with SimpleFSM. If not, see <http://www.gnu.org/licenses/>.

Copyright 2014 Lucas Liendo.
"""

from abc import ABCMeta, abstractmethod
from exceptions import *


class State(object):
    """
    The State class models a defined state.

    To create a new state an id must be supplied to identify it among other
    states. Two other keyword arguments can be supplied to identify if the
    state is a start state and/or a final state.

    Note that at least a final state is needed between all states and just
    only one start state must be established among all states.
    """

    def __init__(self, id, start_state=False, final_state=False):
        self._id = id
        self._start_state = start_state
        self._final_state = final_state

    @property
    def id(self):
        """Returns the id of the state."""
        return self._id

    @property
    def start_state(self):
        """Returns True if the state is marked as a start state."""
        return self._start_state

    @start_state.setter
    def start_state(self, start_state):
        self._start_state = start_state

    @property
    def final_state(self):
        """Returns True if the state is marked as a final state."""
        return self._final_state

    @final_state.setter
    def final_state(self, final_state):
        self._final_state = final_state

    def transit(self, fsm):
        """
        This method is automatically called from SimpleFSM and performs
        the transition from one state to another provided that a transition
        match applies otherwise a FSMRejectedInput is raised.
        """
        symbol = fsm.read_symbol()

        try:
            transition = [t for t in fsm.transitions if t.from_state.id == self.id and t.accepts(symbol)].pop()
        except IndexError:
            raise FSMRejectedInput([symbol])

        fsm.current_state = transition.to_state
        return symbol

    def __eq__(self, other):
        return self.id == other.id


class Transition(object):
    """
    The Transition class models a transition between two given states.
    To create a new transition three mandatory arguments must be supplied :

    from_state : The state from which you want to transit.
    to_state : The state you want to transit to.
    transition_function : The function used to actually test if a symbol matches
    the transition. This function must take only the symbol to be tested.
    """

    def __init__(self, from_state, to_state, transition_function):
        self._from_state = from_state
        self._to_state = to_state
        self._transition_function = transition_function

    @property
    def from_state(self):
        """Returns the state from which this transition should transit."""
        return self._from_state

    @property
    def to_state(self):
        """Returns the state from which this transition should transit to."""
        return self._to_state

    @property
    def transition_function(self):
        """Returns the transition function used by a Transition object."""
        return self._transition_function

    def accepts(self, symbol):
        """
        Returns True if the read symbol is accepted by the transition function.
        """
        return self._transition_function(symbol)

    def __eq__(self, other):
        return self.from_state == other.from_state \
            and self.to_state == other.to_state \
            and self.transition_function == other.transition_function


class SimpleFSM(object):
    """
    The SimpleFSM class models a finite state machine. To use this class
    you must create a custom class that inherits from SimpleFSM and implement
    the read_symbol() method. This method is responsible for returning a symbol
    each time is called. This symbol is then tested to check if it's actually
    accepted by the FSM.

    Typically you would instantiate a set of States and Transitions. After
    this is done you instantiate your custom-implemented FSM and add all the
    states and transitions.

    After your custom-implemented FSM is built you should call the run()
    method. If the word is recognized a list with all the accepted symbols
    is returned otherwise a FSMRejectedInput is raised.
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        self._states = []
        self._transitions = []
        self._accepted_symbols = []
        self._final_states = None
        self._current_state = None
        self._remaining_input = True

    @property
    def transitions(self):
        """Returns a list containing all the defined transitions for this FSM."""
        return self._transitions

    @property
    def current_state(self):
        return self._current_state

    @current_state.setter
    def current_state(self, state):
        self._current_state = state

    def add_state(self, state):
        """
        Adds a new state to the FSM. If the supplied state already exists
        a FSMDuplicatedState exception is raised.
        """
        if state in self._states:
            raise FSMDuplicatedState(state)

        self._states.append(state)

    def add_states(self, states):
        """
        Adds a set of states to the FSM. If one of the states is already
        present a FSMDuplicatedState exception is raised.
        """
        [self.add_state(s) for s in states]

    def add_transition(self, transition):
        """
        Adds a new transition to this FSM. If the supplied transition already
        exists a FSMDuplicatedTransition exception is raised.
        """
        if transition in self._transitions:
            raise FSMDuplicatedTransition(transition)

        self._transitions.append(transition)

    def add_transitions(self, transitions):
        """
        Adds a set of transitions to the FSM. If one of the transitions is
        already present a FSMDuplicatedTransition exception is raised.
        """
        [self.add_transition(t) for t in transitions]

    def pre_transit(self):
        """
        This method is called just before a transition is performed.
        You may optionally implement this method.
        """
        pass

    @abstractmethod
    def read_symbol(self):
        """
        Abstract method that must be implemented by the user. When there
        is no more input a FSMEndOfInput exception should be raised
        to notify the FSM that no more input is available.
        """
        raise FSMNotImplementedInput()

    def post_transit(self):
        """
        This method is called after a sucessfull transition between two
        states is performed. You may optionally implement this method.
        """
        pass

    def _set_initial_state(self):
        start_state = [s for s in self._states if s.start_state]

        if len(start_state) > 1:
            raise FSMStartStatesError()

        try:
            self._current_state = start_state.pop()
        except IndexError:
            raise FSMNoStartStateError()

    def _set_final_states(self):
        self._final_states = [s for s in self._states if s.final_state]

        if not self._final_states:
            raise FSMFinalStateError()

    def _set_states(self):
        self._accepted_symbols = []
        self._remaining_input = True
        self._set_initial_state()
        self._set_final_states()

    def run(self):
        """
        Starts the FSM. Returns a list containing the accepted symbols
        otherwise a FSMRejectedInput exception is raised.
        """

        self._set_states()

        while self._remaining_input:
            try:
                self.pre_transit()
                self._accepted_symbols.append(self._current_state.transit(self))
                self.post_transit()
            except FSMEndOfInput:
                self._remaining_input = False

        if self.current_state not in self._final_states:
            raise FSMRejectedInput(self._accepted_symbols, type='string')

        return self._accepted_symbols
