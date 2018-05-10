"""
Will eventually contain the class used for an interface to manage a singular game.

"""

from .card_lookup import lookup

from copy import deepcopy
from random import choice
from uuid import UUID

class Master_engine(object):
    def __init__(self, players):
        self.players = players
        self.gameobjects = {}
        self.active_player = choice(self.players)

        for player in self.players:
            self.add_gameobject(player)
            for card in player.deck:
                self.add_gameobject(card)

    def add_gameobject(self, obj):
        # Init could just use this line, but adding gameobjects later (tokens etc)
        # is easier with a separate method
        self.gameobjects[UUID()] = deepcopy(obj)

    def tick(self, packet):
        pass
        # Master server calls this once the active player has done something.
        # Packet can be an action such as using an ability.
        # Or a meta ability such as not doing anything.
