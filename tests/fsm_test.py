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

from nose.tools import assert_equal, raises
from unittest import TestCase
from simplefsm import State, Transition, SimpleFSM
from simplefsm.exceptions import (
    FSMStartStatesError, FSMNoStartStateError, FSMFinalStateError,
    FSMRejectedInput, FSMDuplicatedState, FSMDuplicatedTransition,
    FSMEndOfInput
)


class DummyFSM(SimpleFSM):
    def __init__(self):
        super(DummyFSM, self).__init__()
        self._symbols = None
        self._pointer = 0

    def reset(self):
        self._symbols = None
        self._pointer = 0

    def set_symbols(self, symbols):
        self._symbols = symbols

    def read_symbol(self, *args, **kwargs):
        try:
            s = self._symbols[self._pointer]
            self._pointer += 1
        except IndexError:
            raise FSMEndOfInput

        return s


class TestDummyFSM(TestCase):
    def setUp(self):
        self._fsm = self._build_fsm()

    def _build_fsm(self):
        # States.
        state_a = State('a')
        state_a.start_state = True
        state_a.final_state = False

        state_b = State('b')
        state_b.final_state = True

        # Transitions.
        transition_a_self = Transition(state_a, state_a, lambda s: s == 'a')
        transition_b_self = Transition(state_b, state_b, lambda s: s == 'b')
        transition_a_b = Transition(state_a, state_b, lambda s: s == 'b')
        transition_b_a = Transition(state_b, state_a, lambda s: s == 'a')

        # FSM.
        fsm = DummyFSM()
        fsm.add_state(state_a)
        fsm.add_state(state_b)
        fsm.add_transition(transition_a_self)
        fsm.add_transition(transition_b_self)
        fsm.add_transition(transition_a_b)
        fsm.add_transition(transition_b_a)

        return fsm

    def test_input_is_accepted(self):
        fsm_test_input = ['a', 'a', 'b', 'b', 'a', 'b', 'a', 'b']
        self._fsm.reset()
        self._fsm.set_symbols(fsm_test_input)
        assert_equal(self._fsm.run(), fsm_test_input)
        
    @raises(FSMRejectedInput)
    def test_input_is_rejected(self):
        fsm_test_input = ['a', 'a', 'b', 'b', 'a', 'c', 'a']
        self._fsm.reset()
        self._fsm.set_symbols(fsm_test_input)
        self._fsm.run()

    @raises(FSMRejectedInput)
    def test_input_is_rejected_because_not_in_final_state(self):
        fsm_test_input = ['a', 'a', 'b', 'b', 'a']
        self._fsm.reset()
        self._fsm.set_symbols(fsm_test_input)
        self._fsm.run()

    @raises(FSMNoStartStateError)
    def test_missing_start_state(self):
        fsm = DummyFSM()
        fsm.run()

    @raises(FSMFinalStateError)
    def test_missing_final_states(self):
        fsm = DummyFSM()
        state_a = State('a')
        state_a.start_state = True
        fsm.add_state(state_a)
        fsm.run()

    @raises(FSMStartStatesError)
    def test_no_unique_start_state(self):
        fsm = DummyFSM()
        state_a = State('a')
        state_a.start_state = True
        state_b = State('b')
        state_b.start_state = True
        fsm.add_state(state_a)
        fsm.add_state(state_b)
        fsm.run()

    @raises(FSMDuplicatedState)
    def test_duplicated_states(self):
        fsm = DummyFSM()
        fsm.add_state(State('a'))
        fsm.add_state(State('a'))

    @raises(FSMDuplicatedTransition)
    def test_duplicated_transitions(self):
        fsm = DummyFSM()
        transition = Transition(State('a'), State('b'), lambda c: True)
        fsm.add_transition(transition)
        fsm.add_transition(transition)
