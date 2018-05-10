"""
Abstraction of the networking. Used to parse packages to usable format, etcetera.

"""

from .packet import packet_decode, packet_encode, new_user_packet
from .user import User

from select import select
import socket

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

        self.unverified = {}
        # List of users connected, but never verified.
        # key is socket, value is address-deletable tuple.

        # Todo: Handle errors in binding ports
        self.listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.listen_socket.bind(('localhost', kwargs["networking"]["port"]))
        self.listen_socket.listen(10)  # enough to prevent weird errors, small enough to prevent ddos.

        self.inputs = [self.listen_socket]

    def loop(self):
        while self.running:

            readable, [], exceptional = select(self.inputs, [], self.inputs, 10)

            for s in readable:
                if s is server:
                    connection, client_address = s.accept()
                    connection.setblocking(0)
                    inputs.append(connection)

                    self.unverified.append([connection, client_address, False])
                    self._generic_inbox.append(new_user_packet(connection, client_address))

                else:
                    packet = get_packet(s)
                    if not packet:
                        continue

                    if s in self.unverified:
                        if packet["type"] == "identify":
                            if packet["name"] not in [i.name for i in self._inbox]:
                                # User with that name doesn't exist.
                                self.add_user((sock, addr), packet["name"])
                                deletable = True
                                # Might not work, because of references, but hope it does
                            else:
                                sock.send(NAME_IN_USE_ERROR)

                    self.unverified = {i: self.unverified[i] for i in self.unverified if not self.unverified[i][1]}

                    for user in self._inbox:
                        if user.socket == s:
                            self._inbox[user].append(packet)
                            break

            for s in exceptional:
                # Other end of connection was closed suddenly
                self.disconnect([i for i in self._inbox if i.socket == s][0])

        self.listen_socket.close()

    def get_packet(self, sock):
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
        self._generic_inbox.append(identification_response(name, *network_handle))
        self._inbox[new_user] = []

    def get_unreads(self, user):
        unread = self._inbox[user][:]
        self._inbox[user] = []
        return unread

    def get_generics(self):
        unread = self._generic_inbox[:]
        self._generic_inbox = []
        return unread

    def send(self, user, packet):
        user.socket.send(packet_encode(packet))

    def reply(self, original, reply):
        original["socket"].send(packet_encode(reply))

    def broadcast(self, packet):
        for user in self._inbox:
            self.send(user, packet)

    def disconnect(self, user):
        user.socket.close()
        del self._inbox[user]
        self.inputs.remove(user.socket)
