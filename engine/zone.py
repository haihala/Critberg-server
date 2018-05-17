from enum import Enum, auto


class Zone(Enum):
    # DISCUSS IMO cards should handle both offense and defense zones as battlefield
    BATTLEFIELD = auto()
    HAND = auto()
    GRAVEYARD = auto()
    LIBRARY = auto()
    SIDEBOARD = auto()