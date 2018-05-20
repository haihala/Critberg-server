"""
Permanent gameobject that can attack.

"""

from .permanent import Permanent

class Creature(Permanent):
    """
    Fields:
    health: int. Number of damage this can take before dying.
    attack: int. Number of damage this does per attack.
    """

    def __init__(   self,
                    name,
                    cost,
                    fuel,
                    health,
                    attack,
                    speed = 0,
                    triggered_abilities = [],
                    activated_abilities = []
                    ):
        Permanent.__init__( self,
                            name,
                            cost,
                            fuel,
                            speed,
                            triggered_abilities,
                            activated_abilities
                            )
        self.health = health
        self.attack = attack

    def fight(self, target):
        target.health -= self.attack
        if isinstance(target, Creature):
            self.health -= target.attack
