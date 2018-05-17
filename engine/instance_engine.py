"""
Will eventually contain the class used for an interface to manage a singular game.

"""

from .card_lookup import lookup
from .stack import Stack
from .zone import Zone

from gameobjects.ability import Ability
from gameobjects.permanent import Permanent
from gameobjects.player import Player
from gameobjects.spell import Spell
from gameobjects.trigger import Trigger
from gameobjects.triggered_ability import Triggered_ability
from util.errors import NOT_FAST_ENOUGH_ERROR, NOT_ENOUGH_RESOURCES_ERROR, INVALID_ZONE_ERROR, ACTIVATIONS_USED_ERROR
from util.instance_packet import *
from util.packet import packet_encode

from copy import deepcopy
from itertools import cycle
from random import shuffle
from uuid import UUID

def order():
    i = 0
    while True:
        yield i
        i += 1

class Instance_engine(object):
    def __init__(self, users):
        self.players = [Player(user) for user in users]
        self.player_iterator = cycle(self.players)
        # cycle is an iterator, that has a next operator. Basically, it loops endlessly and seamlessly
        # an iterator cannot tell it's current value, so storing it is probably smart.
        # player_iterator is EXCLUSIVELY used to keep track of TURN order. priority order is solved with
        # self.next_from(self.active_player)
        self.active_player = next(self.player_iterator)     # Who has priority
        self.turn_owner = self.active_player                # Whose turn is it when the stack settles
        # With an empty stack, active_player == turn_owner

        self.over = False
        self.winner = None

        self.stack = Stack()

        # Initialize gameobjects
        self.gameobjects = {}
        for player in self.players:
            self.add_gameobject(player)
            player.deck = [lookup(i, j) for i, j in player.user.deck]
            for card in player.deck:
                card.order = order()
                self.add_gameobject(card)
                for triggered in card.trigger:
                    triggered.order = order()
                    self.add_gameobject(triggered)
                for activated in card.activated:
                    activated.order = order()
                    self.add_gameobject(activated)

        # Announce who is going first and what is the order of play
        self.broadcast(game_start_packet(
            [
                [
                    player.uuid, player.name,
                    [
                        card.uuid
                        for card in player.deck
                    ]
                ]
                for player in self.players
            ]
        ))

        for player in self.players:
            # Tell each player what does their deck contain.
            self.active_player.send(card_reveal_packet(
                [
                    [card.uuid, card.id]
                    for card in player.deck
                ], True
            ))
            shuffle(player.deck)
        # At this point, each player knows the uuid for everything and the cards within their deck but not the order.

    def add_gameobject(self, obj):
        ID = UUID()
        self.gameobjects[ID] = obj
        self.gameobjects[ID].uuid = ID
        return ID

    def tick(self, packet):
        # rough structure:
        # 1. handle the input
        self.handle_action(packet)

        # 2. check for win-states (check if a player is dead)
        self.death_check()

    def resolve(self):
        # 1. Pop the top of the stack.
        target = self.stack.pop()

        # 2. Deal with that
        if isinstance(target, Permanent):
            self.change_zone(target, Zone.BATTLEFIELD)
        else:
            # Either an ability or a spell
            # Resolve the effect
            triggers = target(self)

            # Move used spell to graveyard
            if isinstance(target, Spell):
                self.change_zone(target, Zone.GRAVEYARD)

            # Add triggers to stack
            for trigger in triggers:
                self.react(trigger)

    def handle_action(self, packet):
        if packet["subtype"] == "pass":
            if self.stack.empty():
                # If stack is empty, pass the turn
                self.turn_owner = next(self.player_iterator)

                # Skip dead players
                while self.turn_owner.dead:
                    self.turn_owner = next(self.player_iterator)

                self.active_player = self.turn_owner
                self.broadcast(turn_start_packet(self.turn_owner))

                # DISCUSS, should ability activations have a certain amount per turn or per own turn.
                # Should the ability.activations reset each turn swap or only when the controllers turn starts
                for ability in [i for i in self.gameobjects if isinstance(i, Ability)]:
                    ability.activations = 0
            else:
                # If stack is not full, pass priority
                if self.stack.peek_next().owner == self.active_player:
                    # Priority lap has passed, resolve top card.
                    self.resolve()
                self.rotate_priority()
                # Top card was by the active player, meaning it was played when the active player had priority
                # Meaning the next player from the active player should be the one to pick up after it's resolved.

        elif packet["subtype"] == "use":
            # User attempts to use an ability or play a card.
            target = self.gameobjects[packet["instance"]]
            if target.speed < self.stack.peek_next().speed:
                self.active_player.send(NOT_FAST_ENOUGH_ERROR)
                return

            if self.active_player.can_afford(target.cost):
                self.active_player.send(NOT_ENOUGH_RESOURCES_ERROR)
                return

            if isinstance(target, Ability):
                if target.parent.zone not in target.usable_zones:
                    self.active_player.send(INVALID_ZONE_ERROR)
                    return

                if target.max_activations <= target.activations:
                    self.active_player.send(ACTIVATIONS_USED_ERROR)
                    return

                trigger_type = "USE"
                if target.max_activations:
                    target.activations += 1
            else:
                trigger_type = "USE"

            # Add the card/ability to stack.
            self.stack.push(target)
            self.broadcast(stack_add_action_packet(packet["instance"]))

            # Add the trigger to stack
            self.react(Trigger(trigger_type, target))

            self.rotate_priority()

    def rotate_priority(self):
        self.active_player = self.next_from(self.active_player)
        self.broadcast(priority_shift_packet(self.active_player))

    def next_from(self, target):
        tmp_iter = cycle([player for player in self.players if not player.dead])
        player = next(tmp_iter)
        while player is not target:
            player = next(tmp_iter)
        return next(tmp_iter)

    def broadcast(self, packet, blacklist = []):
        # Send a message to everyone in this instance
        for player in [i for i in self.players if i not in blacklist]:
            player.send(packet)

    def death_check(self):
        for player in self.players:
            if player.health <= 0:
                player.dead = True
                self.broadcast(lose_packet(player.uuid))


        if all(player.dead for player in self.players):
            self.over = True
            self.broadcast(tie_packet())

        players_alive = [player for player in self.players if not player.dead]
        if len(players_alive) == 1:
            self.over = True
            self.winner = players_alive[0]
            self.broadcast(win_packet(self.winner.uuid))

    def react(self, trigger):
        trigger_type, trigger_params = trigger.trigger_type, trigger.trigger_params
        reacters =  [i for i in self.triggered_abilities() if i.trigger_type == trigger_type and i.constraint(trigger_params, i)]
        reacters = sorted(reacters, lambda x: x.order)
        reacters = sorted(reacters, lambda x: x.speed)
        for reacter in reacters:
            self.stack.push(reacter)

    def triggered_abilities(self):
        return [j for i, j in self.gameobjects if isinstance(j, Triggered_ability)]

    def change_zone(self, mover, destination):
        self.react(Trigger("EXIT", [mover, mover.zone]))
        mover.order = order()
        mover.zone = destination
        self.react(Trigger("ENTER", [mover, mover.zone]))
