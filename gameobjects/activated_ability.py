"""
Cards may have abilities (triggered or activated). 
Activated abilities are put on the stack manually when a set of criteria is met and the owner decides to use said ability (and maybe pay it's cost if any).

Types for fields:
cost: dictionary of resource costs

"""

from .gameobject import GameObject


class Activated_ability(GameObject):
    def __init__(self):
        super(Activated_ability, self).__init__()
        self.cost = None