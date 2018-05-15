"""
A card that after doing it's effect is moved to the graveyard.
"""
from .card import Card
from .executable import Executable

class Spell(Card, Executable):
    def __init__(self):
        Card.__init__(self)
        Executable.__init__(self)