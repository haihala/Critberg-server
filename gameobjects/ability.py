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
    """
    def __init__(self):
        super(Ability, self).__init__()
        self.speed = None
        self.max_activations = None
        self.parent = None
        self.usable_zones = []

        self.activations = 0                # This can default to 0 because it isn't a constant property
