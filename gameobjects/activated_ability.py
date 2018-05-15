"""
Cards may have abilities (triggered or activated).
Activated abilities are put on the stack manually when a set of criteria is met and the owner decides to use said ability (and maybe pay it's cost if any).
"""

from .ability import Ability


class Activated_ability(Ability):
    """
    Fields:
    cost: dictionary of resource costs
    """

    def __init__(self):
        Ability.__init__(self)
        self.cost = None