"""
Will eventually contain the class used for an interface to manage games.

"""

class Master_engine(object):
    def __init__(self, network_handle, args):
        self.running = True
        self.network_handle = network_handle
        self.args = args

    def loop(self):
        if self.running:
            pass
            # Insert game here