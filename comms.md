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