"""
Something that can be executed (spell or ability)
"""

class Executable():
    """
    Fields:
    ability: function that takes in the instance and returns a (list of triggers, new instance) -tuple
    """
    def __init__(self):
        self.ability = callable()