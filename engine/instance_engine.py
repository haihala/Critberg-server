"""
Will eventually contain the class used for an interface to manage a singular game.

"""

from .card_lookup import lookup

class Master_engine(object):
    def __init__(self, players):
        self.players = players

