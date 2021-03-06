"""
Will eventually contain the class used for an interface to manage games.

"""

from .instance_engine import Instance_engine

from util.user import User
from util.errors import NOT_ACTIVE_PLAYER_ERROR
from util.packet import identify_prompt, message_packet, connect_packet, disconnect_packet, queue_enter


class Master_engine(object):
    def __init__(self, network_handle, args):
        self.running = True
        self.network_handle = network_handle
        self.args = args
        self.users = []
        self.instances = {}
        self.queue = []

    def loop(self):
        while self.running:
            for generic in self.network_handle.get_generics():
                if generic["type"] == "new_user":
                    self.network_handle.reply(generic, identify_prompt())
                elif generic["type"] == "identify":
                    self.users.append(User(generic["name"], (generic["socket"], generic["address"])))
                    self.network_handle.add_user(self.users[-1])
                    self.network_handle.broadcast(connect_packet(generic["name"]))

            disconnected = []

            for user in self.users:
                for message in self.network_handle.get_unreads(user):
                    if message["type"] == "message":
                        if not self.user_called(message["target"]):
                            self.network_handle.send(user, message_packet("Server", "User Not Found. Message not sent"))
                        else:
                            self.network_handle.send(self.user_called(message["target"]), message_packet(user.name, message["content"]))
                            self.network_handle.send(user, message_packet(user.name, message["content"]))
                    elif message["type"] == "disconnect":
                        self.network_handle.broadcast(disconnect_packet(user.name))
                        self.network_handle.disconnect(user)
                        disconnected.append(user)
                    elif message["type"] == "queue":
                        self.queue.append((user, message["deck"]))
                        # TODO at this point, verify deck.
                        self.network_handle.send(user, queue_enter())
                    elif message["type"] == "game_action":
                        if user in self.instances:
                            if user is self.instances[user].active_player.user:
                                self.instances[user].tick(message)
                            else:
                                self.network_handle.send(user, NOT_ACTIVE_PLAYER_ERROR)

            if len(self.queue) >= 2:
                self.start_instance()

            for user in disconnected:
                self.users.remove(user)

            for user, game in self.instances.items():
                if game.over:
                    for player in game.players:
                        del self.instances[player]
                        # TODO record stats.
                        # For card/player/deck winrates

    def start_instance(self):
        users = [self.queue.pop() for i in range(2)]
        new_instance = Instance_engine(users)
        for user in [u[0] for u in users]:
            self.instances[user] = new_instance

    def user_called(self, name):
        try:
            return [i for i in self.users if i.name == name][0]
        except IndexError:
            return None

    def user_from(self, addr):
        try:
            return [i for i in self.users if i.address == addr][0]
        except IndexError:
            return None

    def user_at(self, sock):
        try:
            return [i for i in self.users if i.socket == sock][0]
        except IndexError:
            return None
