"""
Trigger is a description of a state of an event in the game..

"""

from .ability import Ability
from .card import Card
from .creature import Creature
from .gameobject import GameObject
from .permanent import Permanent
from .player import Player

from engine.zone import Zone


TRIGGER_TYPES = {
    # "Name of trigger": [first_param_type, [Possible, types, of, second, param]]
    "HEAL": [[Creature, Player], int],          # Something heals something
    "HURT": [[Creature, Player], int],          # Something does damage to something
    "DRAW": [Player, Card],                     # Somebody draws a card. Drawing many cards is done by repeating this.
    "ATTACK": [Creature, [Creature, Player]],   # Something attacks something
    "DEFEND": [[Creature, Player], Creature],   # Something is attacked by something
    "END_OF_TURN": [Player],                    # Somebodys turn ends
    "START_OF_TURN": [Player],                  # Somebodys turn starts
    "PLAY": [Card],                             # Someone played some card
    "USE": [Ability],                           # Some ability on some permanent was used
    "ENTER": [Card],                            # Something is entering it's zone
    "EXIT": [Card],                             # Something is leaving it's zone
    "TARGET": [GameObject, [Card, Ability]]     # Some gameobject was targeted by some card or ability
                                                # DISCUSS
                                                # I'd imagine this asks for discussion. I vision targeting happening mid-resolution.
                                                # And if something reacts to being targeted, it will be processed before the resolution is continued.
}



class Trigger():
    """
    Fields:
    used_abilities: list of abilities that have already activated on this specific trigger
    type: string key from TRIGGER_TYPES
    type_params: list of gameobjects that should match the accepted parameters in TRIGGER_TYPES
    """

    def __init__(self, trigger_type, type_params):
        self.type = trigger_type
        self.type_params = type_params
        if not isinstance(self.type_params, list):
            self.type_params = [self.type_params]

        # Check that given types make sense. Dealing damage to a trigger is stupid.
        # All type params are mandatory, if not enough are provided the software crashes.
        # This is intentional, since all Triggers are created within the server and don't directly rely on user input,
        # meaning that if this crashes, there is an error in the code and that should be fixed instead of try-caught.
        type_match = True

        for param in range(len(self.type_params)):
            if type_match:
                if isinstance(TRIGGER_TYPES[trigger_type][param], list):
                    # Multiple types accepted
                    if not any(isinstance(self.type_params[param], i) for i in TRIGGER_TYPES[trigger_type][param]):
                        type_match = False
                else:
                    # Single accepted type
                    if not isinstance(self.type_params[param], TRIGGER_TYPES[trigger_type][param]):
                        type_match = False
        if len(self.type_params) != len(TRIGGER_TYPES[trigger_type]):
            type_match = False

        assert type_match
