"""
A card that after doing it's effect is moved to the graveyard.
"""
from .card import Card

class Spell(Card):
    """
    Fields:
    ability: Ability that happens when this is played.
    """

    def __init__(self):
        self.ability = None
