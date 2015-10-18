SimpleFSM
=========

SimpleFSM is an easy-to-use Python module to model Finite State Machines.
The module itself consists in just three classes :

- State
- Transition
- SimpleFSM

Initially you create states and transitions and after that 
you create your custom FSM by inheriting from the SimpleFSM 
class and implementing the read_symbol() method.

Two other methods may (optionally) be implemented and its purpose
is to do pre-processing and post-processing provided that you need
to run custom code before and/or after a symbol is processed.


State class
-----------

The State class models a particular state of your FSM. To create
a state you only need to issue :

.. code-block:: python

    state_a = State('A')

This will create a state using "A" as an id. Note that all the
states of a FSM must have differents ids otherwise when adding
two states with the same id to the FSM an exception is raised.

Another two keyword arguments may optionally be set to mark
a state as a start and/or final state :

.. code-block:: python

    state_a = State('A', start_state=True, final_state=True)
    state_b = State('B', final_state=True)

Note that by default a state is not marked as a start or final
state. It's also important to remark that only a state among all
others must be marked as a start state and at least a final state
must be also marked as well.


Transition class
----------------

The Transition class models a transition between two states.
To create a transition you should write :

.. code-block:: python

    state_a = State('A', start_state=True, final_state=True)
    state_b = State('B', final_state=True)
    transition_a_b = Transition(state_a, state_b, lambda x: x == 0)

The above code builds a transition between state A and state B
and the transition will take place only if the processed symbol
equals zero.


SimpleFSM class
---------------

This class is the core of the simplefsm module. Once you have
built all your states, transitions and the custom FSM you are
ready to go. The following is a full example that shows how to
create a FSM that accepts arbitrary (maximum 10 bits) binary numbers :

.. code-block:: python

    from simplefsm import State, SimpleFSM, Transition
    from simplefsm.exceptions import FSMEndOfInput
    from random import randint


    class BinaryFSM(SimpleFSM):
        def __init__(self, input):
            super(BinaryFSM, self).__init__()
            self._index = 0
            self._input = input

        def read_symbol(self):
            try:
                symbol = self._input[self._index]
                self._index += 1
            except IndexError:
                raise FSMEndOfInput

            return symbol


    def build_fsm():
        # States.
        state_a = State('A', start_state=True, final_state=True)
        state_b = State('B', final_state=True)

        is_zero = lambda i: i == 0
        is_one = lambda i: i == 1

        # Transitions.
        transition_a_self = Transition(state_a, state_a, is_zero)
        transition_b_self = Transition(state_b, state_b, is_one)
        transition_a_b = Transition(state_a, state_b, is_one)
        transition_b_a = Transition(state_b, state_a, is_zero)

        # FSM.
        input_length = randint(1, 10)
        fsm = BinaryFSM([randint(0, 1) for i in range(0, input_length)])
        fsm.add_states([state_a, state_b])
        fsm.add_transitions([transition_a_self, transition_b_self, transition_a_b, transition_b_a])

        return fsm

    def main():
        fsm = build_fsm()
        accepted_word = [str(i) for i in fsm.run()]
        print 'Accepted word : {0}'.format(''.join(accepted_word))

    if __name__ == '__main__':
        main()


In the above example all the transitions are lambdas but you can
use any defined function as well, the functions should take only
one argument (the symbol that is being evaluated) and return a bool.

Is important to note that when implementing the read_symbol()
method and no more input is available you must raise the
FSMEndOfInput exception to notify SimpleFSM that you've reached
the end of the input that you're evaluating.

As mentioned previously there are two methods available to execute
code before and/or after a transition takes place. If you need
to do this then you must implement any of these abstract methods
in your FSM class :

.. code-block:: python

    class YourFSM(SimpleFSM):

        def pre_transit(self, *args, *kwargs):
            ...

        def post_transit(self, *args, *kwargs):
            ...


Installation
------------

Clone this repository to a temporary directory using `GIT <https://git-scm.com/>`_ (or alternatively download
as `.zip <https://github.com/lliendo/SimpleFSM/archive/master.zip>`_), and run  :

.. code-block:: bash
    
    git clone https://github.com/lliendo/SimpleFSM.git
    cd SimpleFSM
    python setup.py install


License
-------

SimpleFSM is distributed under the `GNU LGPLv3 <https://www.gnu.org/licenses/lgpl.txt>`_ license.


Authors
-------

* Lucas Liendo.
