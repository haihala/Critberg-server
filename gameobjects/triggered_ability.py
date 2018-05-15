"""
Cards may have abilities (triggered or activated). Triggered abilities are put on the stack automatically when a set of criteria is met (trigger fulfilled).
"""

from .gameobject import GameObject


class Triggered_ability(GameObject):
    """
    Fieldsields:
    type: string key from TRIGGER_TYPES
    constraints: List of constraints for trigger parameters.
        For example, "whenever a creature is played: ..." would have the first trigger parameter constricted to creatures.
        constraints is a function that should return true or false when passed the possible target. True if legal, False if illegal.
    """

    def __init__(self):
        super(Triggered_ability, self).__init__()
        self.trigger_type = None
        self.constraints = callable()
