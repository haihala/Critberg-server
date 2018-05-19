"""
Represents the players of the game.

"""

from .gameobject import GameObject

from engine.zone import Zone
from engine.card_lookup import lookup

from util.config import RESOURCES, STARTING_HEALTH
from util.packet import packet_encode

class Player(GameObject):
    """
    Fields:
    resource: amount of resources this player has available.
    health: health this player has
    dead: bool telling the server has the player died. dead players are valid targets, but cannot act themselves.
    hand: list of Cards this player has in their hand.
    deck: list of Cards this player has in their deck.
    library: list of Cards this player has in their library.
    attack: list of Cards this player has in their attack field.
    defense: list of Cards this player has in their defense field.
    graveyard: list of Cards this player has in their graveyard.
    exile: list of Cards this player has exiled.
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
        return all([self.resources[resource] >= amount for resource, amount in cost])

    def drain(self, cost):
        if not self.can_afford(cost):
            return False
        for resource, amount in cost:
            self.resources[resource] -= amount
        return True

    def send(self, packet):
        self.user.socket.send(packet_encode(packet))

    def move(self, card, zone):
        self.zones[card.zone].remove(card)
        self.zones[zone].append(card)
