"""
Each card everywhere is represented by a gameobject that inherits from Card.
Card itself is an abstract class.

"""

from .gameobject import GameObject

from util.config import RESOURCES

class Card(GameObject):
    """
    Fields:
    cost: dictionary of resource costs
    fuel: dictionary of resources provided each turn when in resource mode.
    speed: int. Casting speed
    zone:  engine.zone where this card currently resides in
    art: path where the art this card uses is found.
    # DISCUSS ^
    triggered: list of triggered abilities this card has.
    activated: list of activated abilities this card has.
    """

    def __init__(self):
        GameObject.__init__(self)
        self.cost = {i: 0 for i in RESOURCES}   # Example Type Costs
        self.fuel = {i: 0 for i in RESOURCES}   # Example Type Generated when used as mana
#        self.color = 0                         # DISCUSS? Indicated Color (Type? Tribe? whatever)
                                                # This doesn't make sense to me
#        self.rarity = None                     # [Common, Rare, Epic, Legendary] ? More unique names like Mythical?
                                                # Too early to think about this IMO easy to implement later anyways
        self.speed = None
        self.order = None
        self.zone = None

        self.art = None

        self.triggered = []
        self.activated = []

