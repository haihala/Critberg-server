I'll write a snippet that imitates aetherflux reservoir ( http://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=417765 ) from mtg

This is a card declaration. A file called set file contains only a single function. That function returns a list of these. (Done with a function so for configuration could be implemented without changing the cards.) (maybe not smart)

```python
Permanent(
    "aetherflux reservoir",     # Name
    {"mana": 4},                # Cost
    {"mana: 1},                 # Fuel
    triggered = [
        @triggered_ability("PLAY", constraint = lambda triggerer, this: triggerer.owner is this.owner)
        def storm_heal(self, instance):
            return self.parent.owner.heal(instance.storm_count)
    ]
    activated = [
        @activated_ability({"life": 50})
        def health_nuke(self, instance, target=None):
            yield prompt_target([Player, Creature])
            return instance.gameobjects[target].hurt_(50)
    ]
)
```

Permanents and creatures are pretty similar to one another. Spell example next:

```python
Spell(
    "lightning bolt",
    {"mana": 1},
    {"mana": 1},
    speed = 1,
    constraint = lambda target, this: isinstance(target, Creature) or isinstance(target, Player),
    def func(instance, target=None):
        yield prompt_target([Player, Creature])
        return instance.gameobjects[target].hurt(3)
    )
)
```

About the functions

* yield every prompt caused when they are caused.
* return all caused triggers in the end.
* use specified functions for interacting with the instance (heal and hurt) instead of directly adding or subtracting to numbers.
    * This is because these functions return triggers and yielding them makes sure every trigger is correctly handled.
    * These specified functions return triggers one can return.

prompt_target is pretty much a pre-built function that returns a signal asking for a target and putting a target trigger on the stack.