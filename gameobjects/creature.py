"""
Permanent gameobject that can attack.

"""

from .permanent import Permanent

class Creature(Permanent):
    """
    Field:
    health: int. Number of damage this can take before dying.
    attack: int. Number of damage this does per attack.
    """

    def __init__(self):
        super(self)
        self.health = 0
        self.attack = 0
