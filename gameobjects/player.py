"""
Represents the players of the game.

"""

from .gameobject import GameObject
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
    def __init__(self, user):
        GameObject.__init__(self)

        self.resource = {i: 0 for i in RESOURCES}
        self.health = STARTING_HEALTH
        self.dead = False
        self.hand = []
        self.deck = []
        self.library = []
        self.attack = []
        self.defense = []
        self.graveyard = []
        self.exile = []

        self.user = user

    def can_afford(self, card):
        # TODO
        return True

    def send(self, packet):
        self.user[0].socket.send(packet_encode(packet))
