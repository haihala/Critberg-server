"""
Gameobject is a generic class for an object in the game. Something that can be interacted with.
Mostly used to define targetings and whatnot. Gameobjects have a hiararchy that is something among the lines of:

* Gameobject
    * Player
    * Ability
        * Activated ability
        * Triggered ability
    * Card
        * Permanent
            * Creature
        * Spell

Types for fields:
name: string
owner: Gameobject

"""

class GameObject(object):
    def __init__(self):
        self.name = None
        self.owner = None
