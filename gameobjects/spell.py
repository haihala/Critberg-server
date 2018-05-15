"""
A card that after doing it's effect is moved to the graveyard.
"""
from .card import Card
from .executable import Executable

class Spell(Card, Executable):
    def __init__(   self,
                    name,
                    cost,
                    fuel,
                    ability,
                    speed = 0,
                    constraint = lambda *x: True,
                    triggered_abilities = [],
                    activated_abilities = []
                    ):
        Card.__init__(self)
        Executable.__init__(self)

        self.name = name
        self.cost = cost
        self.fuel = fuel
        self.speed = speed
        self.ability = ability
        self.constraint = constraint
        self.triggered = triggered_abilities
        self.activated = activated_abilities
