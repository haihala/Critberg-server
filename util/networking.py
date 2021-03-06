"""
Abstraction of the networking. Used to parse packages to usable format, etcetera.

"""

from .errors import NAME_IN_USE_ERROR, INVALID_PACKET
from .packet import packet_decode, packet_encode, new_user_packet, identify_response, message_packet
from .user import User

from select import select
from socket import socket, AF_INET, SOCK_STREAM

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
        self.listen_socket = socket(AF_INET, SOCK_STREAM)

        self.listen_socket.bind(('', kwargs["networking"]["port"]))
        self.listen_socket.listen(10)  # enough to prevent weird errors, small enough to prevent ddos.

        self.inputs = [self.listen_socket]

    def loop(self):
        while self.running:

            readable, [], exceptional = select(self.inputs, [], self.inputs, 0.1)

            for sock in readable:
                if sock is self.listen_socket:
                    client_socket, client_address = sock.accept()
                    client_socket.setblocking(0)
                    self.inputs.append(client_socket)

                    # self.unverified.append([connection, client_address, False])
                    self.unverified[client_socket] = (client_address, False)
                    self._generic_inbox.append(new_user_packet(client_socket, client_address))

                else:
                    packet = self.get_packet(sock)
                    if not packet:
                        continue
                    if packet == INVALID_PACKET:
                        sock.send(packet_encode(INVALID_PACKET))

                    if sock in self.unverified:
                        if packet["type"] == "identify":
                            if packet["name"] not in [i.name for i in self._inbox]:
                                # User with that name doesn't exist.
                                self._generic_inbox.append(identify_response(packet["name"], *(sock, self.unverified[sock][0])))
                                self.unverified[sock] = (self.unverified[sock][0],True)
                            else:
                                sock.send(packet_encode(NAME_IN_USE_ERROR))

                    self.unverified = {i: self.unverified[i] for i in self.unverified if not self.unverified[i][1]}

                    for user in self._inbox:
                        if user.socket == sock:
                            self._inbox[user].append(packet)
                            break

            for sock in exceptional:
                # Other end of connection was closed suddenly
                self.disconnect([i for i in self._inbox if i.socket == sock][0])

        self.listen_socket.close()

    def get_packet(self, sock):
        data = b''
        while len(data) == 0 or data[-1] != b'\n':
            # newline can only be present if the transmission has ended. This is to assure the entire thing comes through as one.
            # recv timeout would be really cool here.
            tmp = sock.recv(1024)
            data += tmp
            if len(tmp) < 1024:
                break

        ret = packet_decode(data)

        if ret:
            print("In: ", end="")
            print(ret)
            return ret
        # Packet field existance is checked in packet_parse

    def add_user(self, user):
        # Called from main engine. Before this, a generic is raised to ask for a name.
        self._inbox[user] = []

    def get_unreads(self, user):
        unread = self._inbox[user][:]
        self._inbox[user] = []
        return unread

    def get_generics(self):
        unread = self._generic_inbox[:]
        self._generic_inbox = []
        return unread

    def send(self, user, packet):
        print("Out: ", end="")
        print(packet)
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
