# Comms

This file shall describe the in/output of the server in depth.

Everything in here may work today, but not tomorrow. This is more of a guideline.

Nothing is also guaranteed to work, so when encountering issues while writing a client, chances are that the server is broken.

Anything not surrounded with double asterisks is literal. Everything surrounded by asterisks is supposed to not be

## In

### Generic

#### Identify

Identify is a packet the server requests upon joining. Basically, it tells the server what to call this client.

```json
{
    "type": "identify",
    "name": "**string name you wish to be called**"
}
```

#### Queue

A packet that makes the server add the user to the matchmaking queue.

```json
{
    "type": "queue",
    "deck": "**the deck of the user as a list of card IDs**"
}
```

#### Message

Message packets are in client instant messages between clients.

```json
{
    "type": "message",
    "target": "**string name of recipent**",
    "content": "**string content of the message**"
}
```

#### Disconnect

User wishes to disconnect from the server.

```json
{
    "type": "disconnect",
}
```

### Game

All game packets must have their`type` field set to `game_action`. This lets the main engine easily forward these packets to the instance server in question. The `subtype` field is used to determine the type of the action the user wishes to conduct in game.

#### Pass

Pass is a simple packet. Passing when a stack exists, will pass priority. Passing without a stack will pass the turn.

```json
{
    "type": "game_action",
    "subtype": "pass"
}
```

#### Use

Use is the opposite of pass. Instead of doing nothing, use signals that the player wishes to interact with something.
Targets are chosen on resolution, so this packet doesn't require any other than the thing being used.

```json
{
    "type": "game_action",
    "subtype": "use",
    "instance": "**string uuid that describes the card the user wants to play or the activity they want to activate**"
}
```

## Out

### Generic

#### Prompt

Prompt is a packed used by the server to ask for data. For example, it's used to request users to identify themselves.

```json
{
    "type": "prompt",
    "value": "**type of prompt. For example 'identify'**"
}
```

#### Disconnect

When a user disconnects, the server let's everyone know by broadcasting a disconnect package.

```json
{
    "type": "disconnect",
    "name": "**string name of disconnected user**",
    "address": "**string address of disconnected user**"
}
```

#### Message

Message packets are in client instant messages between clients.

```json
{
    "type": "message",
    "sender": "**string name of sender**",
    "content": "**string content of the message**"
}
```

### Game

Like incoming packets with the type `game_action`, all of the game relevant packets the server sends out have the type `game_update` and their subtype is what determines more accurately what happened.

#### Start

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
            "**list string uuids of cards in this player's deck.**"
        ]
    ]
}
```

#### Reveal

It's assumed that each player knows the uuid of everything always, but doesn't know what everything is. Think of this as revealing that the card with a certain uuid is a certain type of card.

```json
{
    "type": "game_update",
    "subtype": "reveal",
    "multiple": "**boolean. If true 'cards' is a list of uuid-cardID pairs. If false. 'cards' is a single uuid-cardID pair**",
    "cards": "**either a single uuid-cardID pair, or a list of pairs. Each pair is linked. **"
}
```

#### Stack add action

Some action (either a card or an ability) was just added to the stack.

```json
{
    "type": "game_update",
    "subtype": "stack_add_action",
    "uuid": "**string uuid of the action that was placed on stack.**"
}
```

#### Stack add trigger

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

#### Turn start

Player's turn has started. This is broadcasted to everyone, so checking the `player` field is mandatory.

```json
{
    "type": "game_update",
    "subtype": "turn_start",
    "player": "**string uuid of the player whose turn is about to start**"
}
```

#### Priority_shift

This is a packet telling each client who has priority.

```json
{
    "type": "game_update",
    "subtype": "priority_shift",
    "player": "**uuid of the player who is up**"
}
```

#### Defeat

A player has died.

```json
{
    "type": "game_update",
    "subtype": "defeat",
    "player": "**uuid of the player who lost**"
}
```
#### Tie

All players have died.

```json
{
    "type": "game_update",
    "subtype": "tie"
}
```

#### Victory

All players except for one have died. This one player is declared the winner.

```json
{
    "type": "game_update",
    "subtype": "victory",
    "player": "**uuid of the player who won**"
}
```
### Errors

Each error has the type `error` and both a short one word explanation and a longer one sentence explanation of what went wrong.

#### Name

You tried to identify with a name that is already in use.

```json
{
"type": "error",
"short": "name",
"value": "Name in use"
}
```

#### Priority

You tried to use something while you don't have the priority.

```json
{
"type": "error",
"short": "priority",
"value": "Yhis player is not active"
}
```

#### Speed

You tried to add something to the stack that is slower than the card on the top of the stack.

```json
{
"type": "error",
"short": "speed",
"value": "Yhat isn't fast enough to be played here."
}
```

#### Cost

You tried to activate an ability or play a card you can't afford.

```json
{
"type": "error",
"short": "cost",
"value": "You can't afford that."
}
```

#### Zone

You tried to activate an ability from a zone that ability cannot be activated from.

```json
{
"type": "error",
"short": "zone",
"value": "You can't use that from there."
}
```

#### Activations

```json
{
"type": "error",
"short": "activations",
"value": "You have exhausted the maximum amount of usages this ability permits."
}
```