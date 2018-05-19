"""
Will be used to lookup cards from IDs.

"""

from gameobjects.creature import Creature
from util.config import RESOURCES

def lookup(cardID, artID=0):
    tmp = Creature(
        "loli squire",
        {'Apple': 2},
        {'Apple': 1},
        1,
        1,
    )

    tmp.card_id = 0

    return tmp