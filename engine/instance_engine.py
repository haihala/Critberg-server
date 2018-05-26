"""
Will eventually contain the class used for an interface to manage a singular game.

"""

from .card_lookup import lookup
from .stack import Stack
from .zone import Zone, to_zone

from gameobjects.ability import Ability
from gameobjects.executable import Executable
from gameobjects.card import Card
from gameobjects.creature import Creature
from gameobjects.permanent import Permanent
from gameobjects.player import Player
from gameobjects.spell import Spell
from gameobjects.trigger import Trigger
from gameobjects.triggered_ability import Triggered_ability
from util.errors import NOT_FAST_ENOUGH_ERROR, NOT_ENOUGH_RESOURCES_ERROR, INVALID_ZONE_ERROR, ACTIVATIONS_USED_ERROR, INVALID_UUID_ERROR, INVALID_TYPE_ERROR, EXHAUSTED_ERROR
from util.instance_packet import *
from util.packet import packet_encode

from copy import deepcopy
from itertools import cycle
from random import shuffle
from uuid import uuid4

def order():
    i = 0
    while True:
        yield i
        i += 1

class Instance_engine(object):
    def __init__(self, users):
        self.players = [Player(user, deck) for user, deck in users]
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
        self.casting = None

        self.stack = Stack()

        # Initialize gameobjects
        self.gameobjects = {}
        for player in self.players:
            self.add_gameobject(player)
            for card in player.zones[Zone.LIBRARY]:
                card.order = order()
                card.owner = player
                self.add_gameobject(card)
                for triggered in card.triggered:
                    triggered.order = order()
                    self.add_gameobject(triggered)
                for activated in card.activated:
                    activated.order = order()
                    self.add_gameobject(activated)

        # Announce who is playing.
        self.broadcast(game_start_packet(
            [
                [
                    player.uuid, player.name, len(player.zones[Zone.LIBRARY])
                ]
                for player in self.players
            ]
        ))

        # Announce who is going first.
        self.broadcast(turn_start_packet(self.turn_owner))

        # Draw a starting hand.
        for player in self.players:
            shuffle(player.zones[Zone.LIBRARY])
            player.draw(order, 5)

    def add_gameobject(self, obj):
        ID = str(uuid4())
        self.gameobjects[ID] = obj
        self.gameobjects[ID].uuid = ID
        return ID

    def tick(self, packet):
        # handle input
        self.handle_action(packet)

        # check for win-states (check if a player is dead)
        self.death_check()

    def resolve(self):
        # 1. Pop the top of the stack.
        target = self.stack.pop()

        # 2. Deal with that
        if isinstance(target, Ability):
            if self.executable_pre_resolve(target):
                self.executable_resolve(target)

        elif target.zone == Zone.HAND:
            if self.card_pre_resolve(target):
                if isinstance(target, Spell):
                    self.executable_resolve(target)
                    self.change_zone(target, Zone.GRAVEYARD)
                else:
                    self.change_zone(target, to_zone(target.parameters[0]))
            else:
                # Fizzles
                self.change_zone(target, Zone.GRAVEYARD)
                self.broadcast(fizzle_packet(target.uuid, target.parameters))


        elif target.exhausted:
            target.owner.send(EXHAUSTED_ERROR)
        else:
            if target.zone == Zone.DEFENSE:
                self.change_zone(target, Zone.OFFENSE)
            elif target.zone == Zone.OFFENSE:
                if target.parameters[0] in self.gameobjects:
                    # Attacking
                    opponent = self.gameobjects[target.parameters[0]]
                    self.broadcast(fight_packet(target.uuid, opponent.uuid))

                    self.react(Trigger("ATTACK", [target, opponent]))
                    self.react(Trigger("DEFEND", [opponent, target]))
                    target.fight(self.gameobjects[target.parameters[0]])

                    for trigger in [Trigger("HURT", [target, opponent.attack]), Trigger("HURT", [opponent, target.attack])]:
                        self.react(trigger)
                elif target.parameters[0] == "DEFENSE":
                    # Moving back
                    self.change_zone(target, Zone.DEFENSE)
            elif target.zone == Zone.RESOURCE:
                target.owner.gain(target.fuel)
                self.broadcast(resource_gain_packet(target.owner.uuid, target.owner.resources))
            target.exhausted = True

    def handle_action(self, packet):
        if packet["subtype"] == "pass":
            self.casting = None
            if self.stack.empty():
                # If stack is empty, pass the turn
                self.turn_owner = next(self.player_iterator)

                # Skip dead players
                while self.turn_owner.dead:
                    self.turn_owner = next(self.player_iterator)

                self.active_player = self.turn_owner
                self.broadcast(turn_start_packet(self.turn_owner))
                self.turn_owner.draw(order)
                self.turn_owner.refresh()

                # DISCUSS, should ability activations have a certain amount per turn or per own turn.
                # Should the ability.activations reset each turn swap or only when the controllers turn starts
                for ability in [i for i in self.gameobjects if isinstance(i, Ability)]:
                    ability.activations = 0
            else:
                # If stack is not full, pass priority
                while self.stack.peek_next().owner == self.active_player:
                    # Priority lap has passed, resolve top card.
                    self.resolve()

                if not self.stack.empty():
                    self.rotate_priority()
                # Top card was by the active player, meaning it was played when the active player had priority
                # Meaning the next player from the active player should be the one to pick up after it's resolved.

        elif packet["subtype"] == "use":
            # User attempts to use an ability or play a card.
            self.casting = None
            if packet["instance"] not in self.gameobjects:
                self.active_player.send(INVALID_UUID_ERROR)
                return

            target = self.gameobjects[packet["instance"]]
            if self.check_errors(target):
                ask_for_params = True
                if not target.owner.can_afford(target):                         # If card can't be afforded
                    if isinstance(target, Card):
                        target.parameters = ["RESOURCE"]
                        ask_for_params = False
                    else:
                        self.active_player.send(NOT_ENOUGH_RESOURCES_ERROR)

                elif isinstance(target, Executable) and not target.requirements:
                    ask_for_params = False
                elif target.zone in [Zone.RESOURCE, Zone.DEFENSE]:
                    ask_for_params = False

                if ask_for_params:
                    self.prompt_params(target)
                    self.casting = target
                else:
                    self.play(target)

        elif packet["subtype"] == "prompt" and self.casting:
            self.casting.parameters = packet["params"]
            self.play(self.casting)
            self.casting = None

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
        trigger_type, trigger_params = trigger.type, trigger.type_params
        reacters =  [i for i in self.triggered_abilities() if i.trigger_type == trigger_type and i.constraint(trigger_params, i)]
        order_cap = float(order())
        reacters = sorted(reacters, key=lambda x: float(x.speed) + (x.order/order_cap))
        # Note, this only works as long as speed is an int.
        self.broadcast(trigger_packet(trigger_type, trigger_params))
        for reacter in reacters:
            self.stack.push(reacter)

    def triggered_abilities(self):
        return [j for i, j in self.gameobjects.items() if isinstance(j, Triggered_ability)]

    def change_zone(self, mover, destination):
        # DISCUSS
        # This is done in this way, because it's easier handling cards so that they always have an intutive zone.
        # This is why we react to the card exiting it's zone when the card is still in that zone
        # This makes it so, we don't need to pass zone arguments to the trigger.
        self.react(Trigger("EXIT", [mover]))
        self.broadcast(move_packet(mover.uuid, mover.zone, destination))
        mover.order = order()
        mover.owner.move(mover, destination, order)
        self.react(Trigger("ENTER", [mover]))

    def card_pre_resolve(self, target):
        if target.parameters[0] == "RESOURCE":
            return True

        if isinstance(target, Spell):
            return self.executable_pre_resolve(target)
        else:
            return target.owner.drain(target.cost)

    def executable_pre_resolve(self, target):
        # Drain resources, verify parameters
        if not target.owner.drain(target.cost):
            return False

        for i in range(len(target.requirements)):
            tester = target.parameters[i + int(isinstance(target, Spell))]
            # Spells can be played as mana, so the params need to be offset by one.
            if tester in self.gameobjects:
                test_object = self.gameobjects[tester]
                if not target.requirements[i](test_object):
                    # If a single parameter is invalid, fizzle
                    return False

    def prompt_params(self, card):
        params = None
        if card.zone == Zone.HAND:
            if isinstance(card, Spell):
                params = [["PLAY", "RESOURCE"] + [uuid for uuid, target in self.gameobjects.items() if req(target) for req in card.requirements]]
            else:
                params = [["OFFENSE", "DEFENSE", "RESOURCE"]]

        elif card.zone == Zone.OFFENSE:
            params = [["DEFENSE"]]
            for player in self.players:
                if player == card.owner:
                    continue
                for blocker in player.zones[Zone.DEFENSE]:
                    params[0].append(blocker.uuid)
                if not player.zones[Zone.DEFENSE]:
                    params[0].append(player.uuid)

        self.active_player.send(prompt_params(card.uuid, params))

    def play(self, target):
        # Add the card/ability/zone swap/attack to stack.
        # Only reveal abilities when their source is not yet revealed.
        trigger_type = None
        if isinstance(target, Ability):
            trigger_type = "USE"
            if target.parent.zone in [Zone.HAND, Zone.LIBRARY]:
                self.broadcast(card_reveal_packet([target.parent]))
        elif target.zone == Zone.HAND:
            # Reveal a card played from hand.
            trigger_type = "PLAY"
            self.broadcast(card_reveal_packet([target]))

        self.stack.push(target)
        self.broadcast(stack_add_action_packet(target.uuid))

        # Add the trigger to stack
        if trigger_type:
            self.react(Trigger(trigger_type, target))

        self.rotate_priority()

    def check_errors(self, target):
        # Generic
        if not (isinstance(target, Ability) or isinstance(target, Card)):
            self.active_player.send(INVALID_TYPE_ERROR)
            return False

        # Executable
        if isinstance(target, Executable):
            if target.speed < self.stack.peek_next().speed:
                self.active_player.send(NOT_FAST_ENOUGH_ERROR)
                return False

        if isinstance(target, Ability):
            if target.parent.zone not in target.usable_zones:
                self.active_player.send(INVALID_ZONE_ERROR)
                return False

            if target.max_activations:
                if target.max_activations <= target.activations:
                    self.active_player.send(ACTIVATIONS_USED_ERROR)
                    return False

                target.activations += 1

        if isinstance(target, Creature):
            if target.exhausted:
                self.active_player.send(EXHAUSTED_ERROR)
                return False
        elif isinstance(target, Permanent):
            self.active_player.send(INVALID_TYPE_ERROR)

        return True

    def executable_resolve(self, target):
        triggers = target(self)
        for trigger in triggers:
            self.react(trigger)