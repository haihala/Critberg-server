"""
Permanent gameobject that can attack.

"""

from .permanent import Permanent

class Creature(Permanent):
    def __init__(self):
        super(self)
        self.health = 0
        self. attack = 0
        self.defense = 0
