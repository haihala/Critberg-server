"""
Something that can be executed (spell or ability)
"""

class Executable():
    """
    Fields:
    requirements: list of (string, function) -tuples, where the string is the type of parameter required and the function is there to validate said function. Example in set_file.md
    parameters: list of parameters the user has selected for the ones listed in requirements.

    """
    def __init__(self):
        self.requirements = []
        self.parameters = []