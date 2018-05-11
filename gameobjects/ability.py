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
        self.max_activations = None  # Per turn