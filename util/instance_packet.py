from engine.zone import to_string

def game_start_packet(players):
    # Players: [<uuid>, <name>, <int number of cards in this player's deck>]
    return {
        "type": "game_update",
        "subtype": "start",
        "players": players
    }

def card_reveal_packet(cards):
    cards = [[i.uuid, i.card_id, [j.uuid for j in i.triggered], [j.uuid for j in i.activated]] for i in cards]

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
        "from": to_string(original),
        "to": to_string(target)
    }

def prompt_params(uuid, params):
    return {
        "type": "game_update",
        "subtype": "param_prompt",
        "object": uuid,
        "params": params
    }

def fizzle_packet(uuid, params):
    return {
        "type": "game_update",
        "subtype": "fizzle",
        "object": uuid,
        "params": params
    }

def fight_packet(attacker, defender):
    return {
        "type": "game_update",
        "subtype": "fight",
        "attacker": attacker,
        "defender": defender
    }

def resource_gain_packet(player, resources):
    # TODO serialize resource types somehow.
    return {
        "type": "game_update",
        "subtype": "resource_gain",
        "player": player,
        "resources": resources
    }