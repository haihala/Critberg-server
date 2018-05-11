"""
Will eventually contain the class used for an interface to manage a singular game.

"""

from .card_lookup import lookup

from gameobjects.player import Player

from copy import deepcopy
from random import choice
from uuid import UUID

class Instance_engine(object):
    def __init__(self, users):
        self.players = [Player(user) for user in users]
        self.active_player = choice(self.players)
        
        self.over = False
        self.winner = None

        # Initialize gameobjects
        self.gameobjects = {}
        for player in self.players:
            self.add_gameobject(player)
            for card in [lookup(i, j) for i, j in player.user.deck]:
                self.add_gameobject(card)
                

    def add_gameobject(self, obj):
        # Init could just use this line, but adding gameobjects later (tokens etc)
        # is easier with a separate method
        self.gameobjects[UUID()] = deepcopy(obj)

    def tick(self, packet):
        # rough structure:
        # 1. handle the input
        self.handle_action(packet)

        # 2. check for win-states (check if a player is dead)
        for player in self.players:
            if player.health <= 0:
                player.dead = True
                # Inform the player of their death.

        if all(player.dead for player in self.players):
            self.over = True
            # Inform the players that it's a draw.

        players_alive = [player for player in self.players if not player.dead]
        if len(players_alive) == 1:
            self.over = True
            self.winner = players_alive[0]
            # Inform the winner that they have indeed won.

    def resolve(self):
        # Resolves the top thing in the stack.
        pass

    def handle_action(self, packet):
        # Returns triggers caused by this action
        if packet["subtype"] == "play":
            # Package is about using a card/ability.
            pass

    def broadcast(self, packet):
        pass  # Send a message to everyone in this instance