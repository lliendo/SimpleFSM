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

class FSMError(Exception):
    pass


class FSMStartStatesError(FSMError):
    def __str__(self):
        return 'Error - Only one start state is allowed for this FSM.'


class FSMNoStartStateError(FSMError):
    def __str__(self):
        return 'Error - No start state defined for this FSM.'


class FSMFinalStateError(FSMError):
    def __str__(self):
        return 'Error - No final state/s defined for this FSM.'


class FSMNotImplementedInput(FSMError):
    def __str__(self):
        return 'Error - The read_symbol() method must be implemented.'


class FSMRejectedInput(FSMError):
    def __init__(self, rejected_input, type='symbol'):
        self._rejected_input = rejected_input
        self._type = type

    @property
    def rejected_input(self):
        return self._rejected_input

    def __str__(self):
        rejected_input_formatted = ' '.join('{0}'.format(s) for s in self._rejected_input)
        return 'Error - \'{0}\' is not a recognized {1} by this FSM.'.format(
            rejected_input_formatted, self._type
        )


class FSMEndOfInput(FSMError):
    def __str__(self):
        return 'No more symbols available. FSM reached input end.'


class FSMDuplicatedState(FSMError):
    def __init__(self, state):
        self._state = state

    def __str__(self):
        return 'Error - The state : \'{0}\' is already defined.'.format(self._state.id)


class FSMDuplicatedTransition(FSMError):
    def __init__(self, transition):
        self._transition = transition

    def __str__(self):
        return 'Error - There\'s already a transition from \'{0}\' to \'{1}\' with the same function.'.format(
            self._transition.from_state.id, self._transition.to_state.id
        )
