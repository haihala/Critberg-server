"""
Abstraction of the networking. Used to parse packages to usable format, etcetera.

"""

from .user import User
from .packet import packet_decode

from socket import socket

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

        self.unverified = []
        # List of users connected, but never verified.


        # Todo: Handle errors in binding ports
        self.listen_socket = socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_socket.bind((None, kwargs["networking"]["port"]))
        self.listen_socket.listen(10)  # enough to prevent weird errors, small enough to prevent ddos.

    def loop(self):
        while self.running:
            new_conn, new_addr = self.listen_socket.accept()
            
            if new_conn and new_addr:
                self.unverified.append([new_conn, new_addr, False])
                self._generic_inbox.append(new_user_packet(new_conn, new_addr))
            
            # Loop through unverified users for identification messages.
            for sock, addr, deletable in self.unverified:
                packet = self.get_packet(sock)
                if not packet:
                    # User either did nothing this loop or did something faulty
                    continue

                if packet["type"] == "identify":
                    # If packet has type field and it equals 'identify'
                    if packet["name"] not in [i.name for i in self._inbox]:
                        # User with that name doesn't exist.
                        self.add_user((sock, addr), packet["name"])
                        deletable = True
                        # Might not work, because of references, but hope it does
                    else:
                        sock.send(NAME_IN_USE_ERROR)
            
            self.unverified = [i for i in self.unverified if not i[0]]

            for user in self._inbox:
                packet = self.get_packet(user.socket)
                if not packet:
                    # User either did nothing this loop or did something faulty
                    continue
                self._inbox[user].append(packet)`
                
        self.listen_socket.close()

    def get_packet(self, sock)
        data = b''
        while data[-1] != b'\n':
            # newline can only be present if the transmission has ended. This is to assure the entire thing comes through as one.
            # recv timeout would be really cool here.
            data += sock.recv(1024)

        return packet_decode(data)
        # Packet field existance is checked in packet_parse

    def add_user(self, network_handle, name):
        # Called from main engine. Before this, a generic is raised to ask for a name.
        new_user = User(name, network_handle)
        self._inbox[new_user] = []

    def get_unreads(self, user):
        unread = self._inbox[user][:]
        self._inbox[user] = []
        return unread

    def get_generics(self):
        unread = self._generic_inbox[:]
        self._generic_inbox = []
        return unread
