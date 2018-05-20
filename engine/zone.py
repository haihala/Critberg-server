from enum import Enum, auto


class Zone(Enum):
    DEFENSE = auto()
    OFFENSE = auto()
    HAND = auto()
    GRAVEYARD = auto()
    LIBRARY = auto()
    SIDEBOARD = auto()
    RESOURCE = auto()

def to_zone(name):
    # TODO rework pls
    if name == "DEFENSE":
        return Zone.DEFENSE
    elif name == "OFFENSE":
        return Zone.OFFENSE
    elif name == "HAND":
        return Zone.HAND
    elif name == "GRAVEYARD":
        return Zone.GRAVEYARD
    elif name == "LIBRARY":
        return Zone.LIBRARY
    elif name == "SIDEBOARD":
        return Zone.SIDEBOARD
    elif name == "RESOURCE":
        return Zone.RESOURCE

def to_string(zone):
    # TODO rework pls
    if zone == Zone.DEFENSE:
        return "DEFENSE"
    elif zone == Zone.OFFENSE:
        return "OFFENSE"
    elif zone == Zone.HAND:
        return "HAND"
    elif zone == Zone.GRAVEYARD:
        return "GRAVEYARD"
    elif zone == Zone.LIBRARY:
        return "LIBRARY"
    elif zone == Zone.SIDEBOARD:
        return "SIDEBOARD"
    elif zone == Zone.RESOURCE:
        return "RESOURCE"
