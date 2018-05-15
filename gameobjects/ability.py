"""
Ability is an abstract class. Cards may have abilities (triggered or activated).

"""

from .gameobject import GameObject
from .executable import Executable

class Ability(GameObject, Executable):
    """
    Fields:
    speed: int. Casting speed
    max_activations: int of times it can be used per turn
    activations: int of times this has been used this turn
    parent: Gameobject his is attached to
    usable_zones: list of elements from the util.zone enum
    constraint: Function.
        For example, "whenever a creature is played: ..." would have the first trigger parameter constricted to creatures.
        constraint is a function that should return true or false when passed the possible target. True if legal, False if illegal.
    """
    def __init__(self):
        GameObject.__init__(self)
        Executable.__init__(self)
        self.speed = None
        self.max_activations = None
        self.parent = None
        self.usable_zones = []
        self.constraint = callable()

        self.activations = 0                # This can default to 0 because it isn't a constant property
