"""
Represents the players of the game.

"""

from .gameobject import GameObject
from util.config import RESOURCES, STARTING_HEALTH

class Player(GameObject):
    """
    Adding basic player attributes regarding health, hand and manapool
    """
    def __init__(self, user):
        super(Player, self).__init__()

        self.resource = {i: 0 for i in RESOURCES}
        self.health = STARTING_HEALTH
        self.dead = False
        self.hand = []
        self.deck = []
        self.library = []
        self.attack = []
        self.defense = []
        self.graveyard = []
        self.exile = []

        self.user = user