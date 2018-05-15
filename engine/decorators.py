"""
This is a module for the decorators used in card text. This transforms python to an ability
"""

from gameobjects.activated_ability import Activated_ability
from gameobjects.triggered_ability import Triggered_ability

from util.zone import Zone

def ability(
            target,
            speed = 0,
            max_activations = None,
            usable_zones = [Zone.BATTLEFIELD],
            constraint = lambda *x: True,
            func = lambda *x: None
        ):
    target.speed = speed
    target.max_activations = max_activations
    target.usable_zones = usable_zones
    target.constraint = constraint
    target.ability = func
    return target

def triggered_ability(trigger_type, **kwargs):
    def triggered_ability_decorator(func):
        tmp = Triggered_ability()
        tmp = ability(tmp, **kwargs, func=func)
        tmp.trigger_type = trigger_type
        if tmp.parent:
            tmp.parent.triggered.append(tmp)
        return tmp
    return triggered_ability_decorator

def activated_ability(cost, **kwargs):
    def activated_ability_decorator(func):
        tmp = Activated_ability()
        tmp = ability(tmp, **kwargs, func=func)
        tmp.cost = cost
        if tmp.parent:
            tmp.parent.activated.append(tmp)
        return tmp
    return activated_ability_decorator
