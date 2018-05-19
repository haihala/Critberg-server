from enum import Enum, auto


class Zone(Enum):
    DEFENSE = auto()
    OFFENSE = auto()
    HAND = auto()
    GRAVEYARD = auto()
    LIBRARY = auto()
    SIDEBOARD = auto()