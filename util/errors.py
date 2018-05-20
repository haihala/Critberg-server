# Errors are stored as bytes, so they can be sent directly.

NAME_IN_USE_ERROR = {
    "type": "error",
    "short": "name",
    "value": "Name in use"
    }


NOT_ACTIVE_PLAYER_ERROR = {
    "type": "error",
    "short": "priority",
    "value": "This player is not active"
    }

NOT_FAST_ENOUGH_ERROR = {
    "type": "error",
    "short": "speed",
    "value": "That isn't fast enough to be played here."
    }

NOT_ENOUGH_RESOURCES_ERROR = {
    "type": "error",
    "short": "cost",
    "value": "You can't afford that."
    }

INVALID_ZONE_ERROR = {
    "type": "error",
    "short": "zone",
    "value": "You can't use that from there."
    }


ACTIVATIONS_USED_ERROR = {
    "type": "error",
    "short": "activations",
    "value": "You have exhausted the maximum amount of usages this ability permits."
    }

INVALID_PACKET = {
    "type": "error",
    "short": "packet",
    "value": "The packet you have sent is invalid."
    }

INVALID_UUID_ERROR = {
    "type": "error",
    "short": "uuid",
    "value": "A gameobject with that uuid doesn't exist"
}

INVALID_TYPE_ERROR = {
    "type": "error",
    "short": "type",
    "value": "That gameobject is of the wrong type"
}

EXHAUSTED_ERROR = {
    "type": "error",
    "short": "exhaust",
    "value": "That creature is exhausted."
}