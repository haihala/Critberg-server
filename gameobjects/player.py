"""
Represents the players of the game.

"""

from .gameobject import GameObject

class Player(object):
    """
    Adding basic player attributes regarding health, hand and manapool
    """
    def __init__(self):
        super(self)
        self.health = 0
        self.resource = {}
        self.hand = []
        self.deck = []
        self.AZone = []
        self.DZone = []
        self.graveyard = []
        self.exile = []
