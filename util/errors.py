from .packet import packet_encode

# Errors are stored as bytes, so they can be sent directly.

NAME_IN_USE_ERROR = packet_encode(
        {
        "type": "error",
        "value": "name in use"
        }
    )

NOT_ACTIVE_PLAYER_ERROR = packet_encode(
        {
        "type": "error",
        "value": "this player is not active"
        }
    )