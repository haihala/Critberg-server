"""
Will eventually contain the class used for an interface to manage a singular game.

"""

from .card_lookup import lookup
from .stack import Stack

from gameobjects.ability import Ability
from gameobjects.player import Player
from gameobjects.trigger import Trigger
from util.errors import NOT_FAST_ENOUGH_ERROR, NOT_ENOUGH_RESOURCES_ERROR, INVALID_ZONE_ERROR, ACTIVATIONS_USED_ERROR
from util.packet import packet_encode

from copy import deepcopy
from itertools import cycle
from random import choice
from uuid import UUID

class Instance_engine(object):
    def __init__(self, users):
        self.players = [Player(user) for user in users]
        self.player_iterator = cycle(self.players)
        # cycle is an iterator, that has a next operator. Basically, it loops endlessly and seamlessly
        # an iterator cannot tell it's current value, so storing it is probably smart.
        self.active_player = next(self.player_iterator)     # Who has priority
        self.turn_owner = self.active_player                # Whose turn is it when the stack settles
        # With an empty stack, active_player == turn_owner

        # Announce who is going first and what is the order of play
        
        self.over = False
        self.winner = None

        self.stack = Stack()

        # Initialize gameobjects
        self.gameobjects = {}
        for player in self.players:
            self.add_gameobject(player)
            for card in [lookup(i, j) for i, j in player.user.deck]:
                self.add_gameobject(card)
                for triggered in card.trigger:
                    self.add_gameobject(triggered)
                for activated in card.activated:
                    self.add_gameobject(activated)
                

    def add_gameobject(self, obj):
        # Init could just use this line, but adding gameobjects later (tokens etc)
        # is easier with a separate method
        ID = UUID()
        self.gameobjects[ID] = deepcopy(obj)        # DISCUSS: Maybe don't deepcopy
        return ID

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
        # This is the most of the work
        # Todo
        # Sketch:
        # 1. Pop the top of the stack.
        # 2. Deal with that
        # 3. If the resolvee was a trigger, delete from gameobjects
        pass

    def handle_action(self, packet):
        # Returns triggers caused by this action
        if packet["subtype"] == "pass":
            if self.stack.empty():
                # If stack is empty, pass the turn
                self.turn_owner = next(self.player_iterator)
                self.active_player = self.turn_owner
            else:
                # If stack is not full, pass priority
                if self.stack.peek_next()[1].owner == self.active_player:
                    # Priority lap has passed, resolve top card.    
                    self.resolve()

        elif packet["subtype"] == "use":
            # User attempts to use an ability or play a card.
            target = self.gameobjects[packet["instance"]]
            if target.speed < self.stack.peek_next()[1].speed:
                self.send(self.active_player, NOT_FAST_ENOUGH_ERROR)
                return

            if self.active_player.can_afford(target.cost):
                self.send(self.active_player, NOT_ENOUGH_RESOURCES_ERROR)
                return

            # All clear.
            # Add the card played trigger or the ability used trigger to the stack after the card.
            self.stack.push(packet["instance"], target)
            if isinstance(target, Ability):
                if target.parent.zone not in target.usable_zones:
                    self.send(self.active_player, INVALID_ZONE_ERROR)
                    return

                if target.max_activations <= target.activations:
                    self.send(self.active_player, ACTIVATIONS_USED_ERROR)
                    return

                ID = self.add_gameobject(Trigger("USE", target))
            else:
                ID = self.add_gameobject(Trigger("PLAY", target))


            self.stack.push(ID, self.gameobjects[ID])

    def send(self, player, packet):
        player.user.socket.send(packet_encode(packet))

    def broadcast(self, packet, blacklist = []):
        # Send a message to everyone in this instance
        for player in [i for i in self.players if i not in blacklist]:
            self.send(player, packet)