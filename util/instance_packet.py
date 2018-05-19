
def game_start_packet(players):
    # Players: [<uuid>, <name>, <list of uuids of the cards representing the deck>]
    # CardID for unknown cards is 0. Every other player will not know what you have in your deck.
    # ID's are still shared, to maybe keep track of certain elements
    return {  # Players and the server must have the same id's for everything
        "type": "game_update",
        "subtype": "start",
        "players": players
    }

def card_reveal_packet(cards, multiple=False):
    # Cards is a list of [<uuid>, <cardID>] pairs
    # Single pair supported as well
    # Parse on client, all information is in.
    return {
        "type": "game_update",
        "subtype": "reveal",
        "multiple": multiple,               # I'm fully aware this parameter isn't needed, but it makes client building slightly easier.
        "cards": cards
    }

def stack_add_action_packet(uuid):
    return {
        "type": "game_update",
        "subtype": "stack_add_action",
        "uuid": uuid
    }

def turn_start_packet(player):
    return {
        "type": "game_update",
        "subtype": "turn_start",
        "player": player.uuid
    }

def priority_shift_packet(player):
    return {
        "type": "game_update",
        "subtype": "priority_shift",
        "player": player.uuid
    }

def lose_packet(loser):
    return {
        "type": "game_update",
        "subtype": "defeat",
        "player": loser
    }

def tie_packet():
    return {
        "type": "game_update",
        "subtype": "tie"
    }

def win_packet(winner):
    return {
        "type": "game_update",
        "subtype": "victory",
        "player": winner
    }

def move_packet(mover, original, target):
    return {
        "type": "game_update",
        "subtype": "move",
        "mover": mover,
        "from": original,
        "to": target
    }

def prompt_params(uuid, params):
    return {
        "type": "game_update",
        "subtype": "param_prompt",
        "object": uuid,
        "params": params
    }