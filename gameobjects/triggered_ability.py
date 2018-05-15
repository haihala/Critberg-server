"""
Cards may have abilities (triggered or activated). Triggered abilities are put on the stack automatically when a set of criteria is met (trigger fulfilled).
"""

from .ability import Ability


class Triggered_ability(Ability):
    """
    Fieldsields:
    type: string key from TRIGGER_TYPES
    """

    def __init__(self):
        Ability.__init__(self)
        self.trigger_type = None
