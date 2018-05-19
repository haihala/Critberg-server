"""
Module for handling packets. Mostly used to create commonly used packets.

"""
from .errors import INVALID_PACKET

from json import dumps, loads
from json.decoder import JSONDecodeError

# Incoming
def new_user_packet(sock, addr):
    return {
        "type": "new_user",
        "socket": sock,
        "address": addr
    }

def identify_response(name, sock, addr):
    return {
        "type": "identify",
        "name": name,
        "socket": sock,
        "address": addr
    }
# Outgoing
def identify_prompt():
    return {
        "type": "prompt",
        "value": "identify"
    }

def connect_packet(name):
    return {
        "type": "connect",
        "name": name                # It's crucial to not give sockets or addressess to the clients
                                    # See "skype ddos" for context
    }

def disconnect_packet(name):
    return {
        "type": "disconnect",
        "name": name
    }

def message_packet(sender, content):
    return {
        "type": "message",
        "sender": sender,
        "content": content
    }


def packet_encode(packet):
    return dumps(packet).encode("UTF-8") + b'\n'

def packet_decode(data):
    # This should validate the packet. Check that it does contain everything required for a packet of it's type
    packet = None
    try:  # Given faulty bytes, loads can fail.
        packet = loads(data.decode("UTF-8"))
    except JSONDecodeError:
        return None

    if authenticate(packet):
        return packet
    else:
        return INVALID_PACKET

def authenticate(packet):
    if "type" not in packet:
        return False
    elif packet["type"] == "identify":
        if "name" not in packet:
            return False
        if not isinstance(packet["name"], str):
            return False
        return True
    elif packet["type"] == "message":
        if "target" not in packet:
            return False
        if not isinstance(packet["target"], str):
            return False
        if "content" not in packet:
            return False
        if not isinstance(packet["content"], str):
            return False
        return True
    elif packet["type"] == "queue":
        if "deck" not in packet:
            return False
        if not isinstance(packet["deck"], list):
            return False
        if not all(len(i) == 2 for i in packet["deck"]):
            return False
        return True
    elif packet["type"] == "disconnect":
        return True
    elif packet["type"] == "game_action":
        if "subtype" not in packet:
            return False
        if packet["subtype"] == "pass":
            return True
        if packet["subtype"] == "use":
            if "instance" not in packet:
                return False
            if not isinstance(packet["instance"], str):
                return False
            return True

    return False        # Packet has invalid type