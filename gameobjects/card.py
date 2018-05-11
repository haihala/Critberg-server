"""
Each card everywhere is represented by a gameobject that inherits from Card.
Card itself is an abstract class.

"""

from .gameobject import GameObject

from util.config import RESOURCES

from enum import Enum, auto

class Zone(Enum):
    # DISCUSS IMO cards should handle both offense and defense zones as battlefield
    BATTLEFIELD = auto()
    HAND = auto()
    GRAVEYARD = auto()
    LIBRARY = auto()


class Card(GameObject):
    def __init__(self):
        super(self)
        self.cost = {i: 0 for i in RESOURCES}   # Example Type Costs
        self.fuel = {i: 0 for i in RESOURCES}   # Example Type Generated when used as mana
        self.color = 0                          # DISCUSS? Indicated Color (Type? Tribe? whatever)
        self.rarity = 0                         # [Common, Rare, Epic, Legendary] ? More unique names like Mythical?
        self.speed = 0
        self.zone = None

        self.image = None

        self.triggered = []
        self.activated = []

