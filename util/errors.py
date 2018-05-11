from .packet import packet_encode

# Errors are stored as bytes, so they can be sent directly.

NAME_IN_USE_ERROR = packet_encode(
        {
        "type": "error",
        "short": "name",
        "value": "Name in use"
        }
    )

NOT_ACTIVE_PLAYER_ERROR = packet_encode(
        {
        "type": "error",
        "short": "priority",
        "value": "Yhis player is not active"
        }
    )

NOT_FAST_ENOUGH_ERROR = packet_encode(
        {
        "type": "error",
        "short": "speed",
        "value": "Yhat isn't fast enough to be played here."
        }
    )

NOT_ENOUGH_RESOURCES_ERROR = packet_encode(
        {
        "type": "error",
        "short": "cost",
        "value": "You can't afford that."
        }
    )

INVALID_ZONE_ERROR = packet_encode(
        {
        "type": "error",
        "short": "zone",
        "value": "You can't use that from there."
        }
    )

ACTIVATIONS_USED_ERROR = packet_encode(
        {
        "type": "error",
        "short": "activations",
        "value": "You have exhausted the maximum amount of usages this ability permits."
        }
    )
