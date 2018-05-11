"""
Trigger is a description of a state of an event in the game..

Types for fields:
used_abilities: list of abilities that have already activated on this specific trigger
type: string key from TRIGGER_TYPES
type_params: list of gameobjects that should match the accepted parameters in TRIGGER_TYPES

"""

from .card import Card
from .creature import Creature
from .gameobject import GameObject
from .player import Player


TRIGGER_TYPES: {
    # "Name of trigger": [first_param_type, [Possible, types, of, second, param]]
    "HEAL": [[Creature, Player], int],  # Something heals something
    "HURT": [[Creature, Player], int],  # Something does damage to something
    "DRAW": [Player, Card],             # Somebody draws a card. Drawing many cards is done by repeating this.
    "ATTACK": [Creature, Creature],     # Something attacks something
    "DEFEND": [Creature, Creature],     # Something is attacked by something
    "END_OF_TURN": [Player],            # Somebodys turn ends
    "START_OF_TURN": [Player],          # Somebodys turn starts
    "ZONE_CHANGE": [GameObject, str],   # Something is moved to a different zone (dying is just moving from the battlefield to the grave.)
}




class Trigger(GameObject):
    def __init__(self, trigger_type, type_params):
        super(Trigger, self).__init__()
        self.used_abilities = []
        # List of uuids of things that have already been in the stack because of this specific trigger.
        # Note, not this kind of trigger.
        self.type = trigger_type
        self.type_params = type_params


        # Check that given types make sense. Dealing damage to a trigger is stupid.
        # All type params are mandatory, if not enough are provided the software crashes.
        # This is intentional, since all Triggers are created within the server and don't directly rely on user input,
        # meaning that if this crashes, there is an error in the code and that should be fixed instead of try-caught.
        type_match = True

        for param in range(len(type_params)):
            if type_match:
                if not isinstance(TRIGGER_TYPES[trigger_type], list):
                    # Single accepted type
                    if not isinstance(type_params[param], TRIGGER_TYPES[trigger_type]):
                        type_match = False
                else:
                    # Multiple types accepted
                    if not any(isinstance(type_params[param], i) for i in TRIGGER_TYPES[trigger_type][param]):
                        type_match = False

        assert type_match