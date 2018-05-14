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


"""

class GameObject(object):
    """
    Fields:
    name: string name of this gameobject
    owner: Player that owns this gameobject
    uuid: UUID this instance has this gameobject stored in.
    """

    def __init__(self):
        self.name = None
        self.owner = None
        self.uuid = None
