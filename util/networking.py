"""
Abstraction of the networking. Used to parse packages to usable format, etcetera.

"""
class Network(object):
    def __init__(self, kwargs):
        self.running = True

        self._inbox = {}
        # Inbox is a container for unread messages.
        # Key is the user sending the messages, value is a list of unreads.
        # Supposed to be accessed through helper methods.

        # Todo: Bind ports and get ready to loop

    def loop(self):
        pass