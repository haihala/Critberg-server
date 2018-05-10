"""
Abstraction of the networking. Used to parse packages to usable format, etcetera.

"""

from .user import User


class Network(object):
    def __init__(self, kwargs):
        self.running = True

        self._inbox = {}
        # Inbox is a container for unread messages.
        # Key is the user sending the messages, value is a list of unreads.
        # Supposed to be accessed through helper methods.
        self._generic_inbox = []
        # List of messages that either don't yet have a user to associate them with
        # or come from elsewhere, such as console commands.

        # Todo: Bind ports and get ready to loop

    def loop(self):
        pass

    def add_user(self, network_handle, name):
        # Called from main engine. Before this, a generic is raised to ask for a name.
        new_user = User(name, network_handle)
        self._inbox[new_user] = []

    def get_unreads(self, user):
        unread = self._inbox[user][:]
        self._inbox[user] = []
        return unread
