"""
Ability is an abstract class. Cards may have abilities (triggered or activated).

Types for fields:
ability: string (code)
max_activations: int
"""

from .gameobject import GameObject


class Ability(GameObject):
    def __init__(self):
        super(Ability, self).__init__()
        self.ability = None
        self.speed = None
        self.max_activations = None     # Per turn
        self.activations = 0
        self.parent = None              # Permanent this is attatched to
        self.usable_zones = []          # Zones this can be used in