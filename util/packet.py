"""
Module for handling packets. Mostly used to create commonly used packets.

"""
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
    return packet_encode({
        "type": "prompt",
        "value": "identify"
    })

def disconnect_packet(name, addr):
    return packet_encode({
        "type": "disconnect",
        "name": name,
        "address": addr
    })

def message_packet(sender, content):
    return packet_encode({
        "type": "message",
        "sender": sender,
        "content": content
    })


def packet_encode(packet):
    return dumps(packet).encode("UTF-8")

def packet_decode(data):
    # TODO
    # This should validate the packet. Check that it does contain everything required for a packet of it's type
    try:  # Given faulty bytes, loads can fail.
        return loads(data.decode("UTF-8"))
    except JSONDecodeError:
        return None
