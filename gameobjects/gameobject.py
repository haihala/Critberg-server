"""
Gameobject is a generic class for an object in the game. Something that can be interacted with.
Mostly used to define targetings and whatnot. Gameobjects have a hiararchy that is something among the lines of:

* Gameobject
    * Player
    * Card
        * Permanent
            * Creature
            * Object
        * Spell

"""

class GameObject(object):
    def __init__(self):
        self.name = None
        self.image = None
        self.cardText = None
        self.owner = None

        self.events = []
