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

    def can_afford(self, cost):
        return all([self.resources[resource] >= amount for resource, amount in cost.items()])

    def drain(self, cost):
        if not self.can_afford(cost):
            return False
        for resource, amount in cost.items():
            self.resources[resource] -= amount
        return True

    def gain(self, resources):
        for fuel, amount in resources.items():
            if fuel in self.resources:
                self.resources[fuel] += amount
            else:
                self.resources[fuel] = amount

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