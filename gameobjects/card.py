"""
Each card everywhere is represented by a gameobject that inherits from Card.
Card itself is an abstract class.

"""

from .gameobject import GameObject
from utils.config import Resources

class Card(GameObject):
    def __init__(self):
        super(self)
        self.cost = {i: 0 for i in Resources} # Example Type Costs
        self.fuel = {i: 0 for i in Resources} # Example Type Generated when used as mana
        self.color = 0 # Indicated Color (Type? Tribe? whatever)
        self.rarity = 0 # [Common, Rare, Epic, Legendary] ? More unique names like Mythical?
        self.speed = 0
