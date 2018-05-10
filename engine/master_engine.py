"""
Will eventually contain the class used for an interface to manage games.

"""

from util.packet import *
# Should not be * but fix later

class Master_engine(object):
    def __init__(self, network_handle, args):
        self.running = True
        self.network_handle = network_handle
        self.args = args
        self.users = []

    def loop(self):
        while self.running:
            for generic in self.network_handle.get_generics():
                if generic["type"] == "new_user":
                    self.network_handle.reply(generic, identify_prompt())
            
            for user in self.users:
                for message in self.network_handle.get_unreads(user)
                    if message["type"] == "message":
                        self.network_handle.send(message["target"])
                    elif message["type"] == "disconnect":
                        self.network_handle.broadcast(disconnect_packet(user.name, user.address))
                        self.network_handle.disconnect(user)
                        self.users