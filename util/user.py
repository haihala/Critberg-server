"""
Each player is a user always, but only has a corresponding player object when in game.

"""

class User(object):
    def __init__(self, name, network_handle):
        self.name = name
        self.network_handle = network_handle

        self.player = None