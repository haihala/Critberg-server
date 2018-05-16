"""
Stack is a class that is basically a list with added features. It's used to manage keep tabs on priority and avoid Single Stack Infinite Loops(ssil).

Types for fields:
_stack: list the actual stack.

"""

from gameobjects.triggered_ability import Triggered_ability

from collections import OrderedDict


class Stack():
    def __init__(self):
        self._stack = OrderedDict()

    def push(self, gameobject):
        # Some user has played a card to append the stack with
        ID = gameobject.uuid
        if isinstance(gameobject, Triggered_ability):
            # Assume the previous layer is a trigger. If it isn't a trigger, there is a bug elsewhere and this crash is justified.
            # This section adds the new triggered ability to the triggers list of used abilities.
            # instance_engine will make sure to not re-trigger the same ability on the same trigger.
            tmp = self._stack.popitem()
            tmp[1].used_abilities.append(ID)
            self._stack[tmp[0]] = tmp[1]
        self._stack[ID] = gameobject

    def pop(self):
        # Instance engine is resolving the top card
        # Returns a (id, gameobject) -tuple
        return self._stack.popitem()

    def counter(self, id):
        # Remove the given item from the stack.
        # This is the reason why using OrderedDict is good.
        del self._stack[id]

    def to_list(self):
        # Useful for stack examination
        # For example, something could take into account the height of the stack.
        # Storm fixed boys?
        return self._stack.items()

    def empty(self):
        # True if empty, false if not
        return not bool(len(self._stack))

    def peek_next(self):
        pair = self.pop()
        self.push(pair[1])
        return pair