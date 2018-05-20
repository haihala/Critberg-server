"""
Something that stays on the field after being played.

"""

from .card import Card

class Permanent(Card):
    def __init__(   self,
                    name,
                    cost,
                    fuel,
                    speed = 0,
                    triggered_abilities = [],
                    activated_abilities = []
                    ):
        Card.__init__(self)

        self.name = name
        self.cost = cost
        self.fuel = fuel
        self.speed = speed
        self.triggered = triggered_abilities
        self.activated = activated_abilities
        self.exhausted = False
