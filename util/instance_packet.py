
def game_start_packet(players):
    # Players: [<uuid>, <name>, <int number of cards in this player's deck>]
    return {
        "type": "game_update",
        "subtype": "start",
        "players": players
    }

def card_reveal_packet(cards):
    cards = [[i.uuid, i.card_id] for i in cards]

    return {
        "type": "game_update",
        "subtype": "reveal",
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