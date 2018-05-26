"""
Represents the players of the game.

"""

from .card import Card
from .creature import Creature
from .gameobject import GameObject

from engine.zone import Zone
from engine.card_lookup import lookup

from util.config import RESOURCES, STARTING_HEALTH
from util.instance_packet import card_reveal_packet
from util.packet import packet_encode

class Player(GameObject):
    """
    Fields:
    resource: amount of resources this player has available.
    health: health this player has
    dead: bool telling the server has the player died. dead players are valid targets, but cannot act themselves.
    user: User that controls this player.
    """
    def __init__(self, user, deck):
        GameObject.__init__(self)

        self.resources = {i: 0 for i in RESOURCES}
        self.health = STARTING_HEALTH
        self.dead = False
        self.zones = {z: [] for z in Zone}
        self.zones[Zone.LIBRARY] = [lookup(i, j) for i, j in deck]
        self.user = user
        self.name = user.name

    def _untapped(self, resource):
        return sum([i.fuel[resource] for i in self.zones[Zone.RESOURCE] if not i.exhausted and resource in i.fuel])
    def _autotap(self, cost, tapped=[]):
        to_tap = {resource: amount - self.resources[resource] - sum([card.fuel[resource] for card in tapped if resource in card.fuel]) for resource, amount in cost.items()}

        # TODO, this is horrible, but nobody else will ever read it so I can push it to master.
        # This was written at 3:31 am, 26.5.2018. When you encounter this, poke haj in private.

        # First, see if tapping a single card is a solution
        fulfills_cost = []
        not_sufficient = []
        for card in [i for i in self.zones[Zone.RESOURCE] if not i.exhausted and i not in tapped]:
            if all(card.fuel[resource] > to_tap[resource] for resource in card.fuel if resource in to_tap):
                fulfills_cost.append((tapped + [card], sum(amount - to_tap[resource] * int(resource in to_tap) for resource, amount in card.fuel.items())))
            else:
                not_sufficient.append((tapped + [card], sum(amount - to_tap[resource] * int(resource in to_tap) for resource, amount in card.fuel.items())))

        min_waste = min(i[1] for i in fulfills_cost)

        if len(fulfills_cost) == len([i for i in self.zones[Zone.RESOURCE] if not i.exhausted]):
            # All tappables produce waste, pick the least wasteful.
            # Strip out all non-optimal solutions
            fulfills_cost = [i for i in fulfills_cost if i[1] == min_waste]

            if len(fulfills_cost) == 1:
                return fulfills_cost[0]
            else:
                # Some logic should take place here to determine what to tap when multiple options are present.
                return fulfills_cost[0]
        else:
            # There are cards that can pay for a part of the cost, maybe they lead to lossless solutions.
            recursive = []
            for insufficient in not_sufficient:
                recursive.append(self._autotap(cost, tapped=insufficient[0]))
            # If a lossless path exists.
            minimal_loss = sorted(recursive, key=lambda x: x[1])[0]
            if minimal_loss[1] < min_waste[1]:
                # The solution presented with subdividing is better in terms of waste.
                return minimal_loss

    def can_afford(self, cost):
        if all([self.resources[resource] >= amount for resource, amount in cost.items()]):
            return 1    # yes without tapping
        elif all([self.resources[resource] + self._untapped(resource) >= amount for resource, amount in cost.items()]):
            return 2    # yes, but extra tapping is required
        return 0        # no

    def drain(self, cost):
        can_afford = self.can_afford(cost)
        if not can_afford:
            return False
        if can_afford == 2:
            self._autotap(cost)
        for resource, amount in cost.items():
            self.resources[resource] -= amount
        return True

    def gain(self, resources):
        for fuel, amount in resources.items():
            self.resources[fuel] += amount

    def send(self, packet):
        self.user.socket.send(packet_encode(packet))

    def move(self, card, zone, order):
        self.zones[card.zone].remove(card)
        self.zones[zone].append(card)
        card.zone = zone
        card.order = order()

    def draw(self, order, amount=1):
        for _ in range(amount):
            if len(self.zones[Zone.LIBRARY]):
                self.move(self.zones[Zone.LIBRARY][0], Zone.HAND, order)
        self.send(card_reveal_packet(self.zones[Zone.HAND][:-amount]))

    def refresh(self):
        for creature in [i for i in self.zones[Zone.DEFENSE] + self.zones[Zone.OFFENSE] + self.zones[Zone.RESOURCE] if isinstance(i, Card)]:
            creature.exhausted = False