"""
Module for handling packets. Mostly used to create commonly used packets.

"""
from json import dumps, loads
from json.decoder import JSONDecodeError, 

def new_user_packet(sock, addr):
    return packet_encode({
        "type": "new_user",
        "socket": sock,
        "address": addr
    })

def packet_encode(packet):
    return dumps(packet).encode("UTF-8")

def packet_decode(data):
    try:  # Given faulty bytes, loads can fail.
        return loads(data.decode("UTF-8"))
    except json.decoder.JSONDecodeError:
        return None
