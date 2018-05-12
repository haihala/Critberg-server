"""
Something that stays on the field after being played.

"""

from .card import Card

class Permanent(Card):
    def __init__(self):
        super(self)