# Instance comms

Most game packets must have their `type` field set to `game_action`. This lets the main engine easily forward these packets to the instance server in question. The `subtype` field is used to determine the type of the action the user wishes to conduct in game.

## Player actions

### Pass

Pass is a simple packet. Passing when a stack exists, will pass priority. Passing without a stack will pass the turn.

```json
{
    "type": "game_action",
    "subtype": "pass"
}
```

### Use

Use is the opposite of pass. Instead of doing nothing, use signals that the player wishes to interact with something.
Targets are chosen on resolution, so this packet doesn't require any other than the thing being used.

```json
{
    "type": "game_action",
    "subtype": "use",
    "instance": "**string uuid that describes the card the user wants to play or the activity they want to activate**"
}
```

### Prompt

Sometimes after using something, addition information such as targets must be provided.

#### From server

```json
{
    "type": "game_action",
    "subtype": "prompt",
    "instance": "**List of lists of options. Each sub-list is a list of options**"
}
```

#### To server

After server sends a prompt message to a client, they are expected to respond with their selected options.

For each sub-list in the server package, the client must select one and respond with a list containing each selection.

```json
{
    "type": "game_action",
    "subtype": "prompt",
    "instance": "**List of selections**"
}
```

### Query

When a game is going on, a client may query any information that they have already been provided.

```json
{
    "type": "query",
    "info": "**string that describes what the client wants to know.**"
}
```

Info is one of the following, to which the server responds with:

#### Game

when `"info": "game"`, server responds with:
```json
{
    "type": "query",
    "players": {
        "**string uuid**": {
            "health": "**int of health**",
            "deck": "**int amount of cards in deck**",
            "grave": "**list of (uuid)-(cardID)-(modifier dictionary) trios**",
            "hand": "**list of (uuid)-(cardID)-(modifier dictionary) trios**",                // If this doesn't represent the player querying, hand attribute is an int amount of cards instead of pairlist.
            "ready_resources": "**list of (uuid)-(cardID)-(modifier dictionary) trios**",
            "exhausted_resources": "**list of (uuid)-(cardID)-(modifier dictionary) trios**",
            "ready_defense": "**list of (uuid)-(cardID)-(modifier dictionary) trios**",
            "exhausted_defense": "**list of (uuid)-(cardID)-(modifier dictionary) trios**",
            "ready_offense": "**list of (uuid)-(cardID)-(modifier dictionary) trios**",
            "exhausted_offense": "**list of (uuid)-(cardID)-(modifier dictionary) trios**"
        }, // For each player
    },
}
```

#### Object

when `"info": "**string uuid**"` and uuid corresponds to a card:

```json
{
    "type": "query",
    "cardID": "**cardID of the card**",
    "modifiers": "**modifier dictionary**"
}
```

When uuid corresponds to an ability, server responds with:

```json
{
    "type": "query",
    "cardID": "**cardID of the parent card**",
    "activated": "**boolean if true, this ability is an activated ability, if false, it's a triggered ability**",
    "index": "**int, index of this ability on parent card.**",
    "uses": "**int, times used this turn**",
    "max_uses": "**int, max times can be used in a turn. Null if not limited.**",
    "enabled": "**boolean. True if owner can use it, false if not.**"
}
```

When uuid corresponds to a player, server responds with one player object. See previous point (Game) for information on the structure.

## Events

Like incoming packets with the type `game_action`, all of the game relevant packets the server sends out have the type `game_update` and their subtype is what determines more accurately what happened.

### Start

This is sent when the game starts. This packet tells the players who are they playing against and the uuids that the server will reference later.

```json
{
    "type": "game_update",
    "subtype": "start",
    "players": [
        // a list of player objects serialized as the following:
        [
            "**string uuid of player**",
            "**string name of player**",
            "**int number of cards in this player's deck**"
        ]
    ]
}
```


### Stack add action

Some action was just added to the stack.

```json
{
    "type": "game_update",
    "subtype": "stack_add_action",
    "uuid": "**string uuid of the action that was placed on stack.**"
}
```

### Trigger

Some trigger was just added to the stack. Happens for example when something was healed. In this case `trigger_type` would be `HEAL` and trigger_params an uuid of the thing healed.

```json
{
    "type": "game_update",
    "subtype": "stack_add_trigger",
    "uuid": "**string uuid of trigger (for targeting)**",
    "trigger_type": "**string type of trigger. For example 'HEAL' when something was healed.**",
    "trigger_params": "**parameters for that specific kind of trigger. Type dependent on trigger_type**"
}
```

Trigger types and the corresponding `trigger_params`:

* HEAL - string uuid of healed gameobject
\# TODO

### Turn start

Player's turn has started. This is broadcasted to everyone, so checking the `player` field is mandatory.

```json
{
    "type": "game_update",
    "subtype": "turn_start",
    "player": "**string uuid of the player whose turn is about to start**"
}
```

### Priority_shift

This is a packet telling each client who has priority.

```json
{
    "type": "game_update",
    "subtype": "priority_shift",
    "player": "**uuid of the player who is up**"
}
```

## Meta information

Revealing something and redundant information sharing

### Reveal

It's assumed that each player knows the uuid of everything always, but doesn't know what everything is. Think of this as revealing that the card with a certain uuid is a certain type of card.

```json
{
    "type": "game_update",
    "subtype": "reveal",
    "cards": "**list of pairs. Each pair is linked. **"
}
```

## Game ending

### Defeat

A player has died.

```json
{
    "type": "game_update",
    "subtype": "defeat",
    "player": "**uuid of the player who lost**"
}
```

### Tie

All players have died.

```json
{
    "type": "game_update",
    "subtype": "tie"
}
```

### Victory

All players except for one have died. This one player is declared the winner.

```json
{
    "type": "game_update",
    "subtype": "victory",
    "player": "**uuid of the player who won**"
}
```