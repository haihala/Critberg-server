"""
Cards may have abilities (triggered or activated). Triggered abilities are put on the stack automatically when a set of criteria is met (trigger fulfilled).

Types for fields:
trigger: Trigger object.

"""

from .gameobject import GameObject


class Triggered_ability(GameObject):
    def __init__(self):
        super(Triggered_ability, self).__init__()
        self.trigger = None