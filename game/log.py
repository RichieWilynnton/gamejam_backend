from dataclasses import dataclass, field

from game.action import Action

@dataclass
class ActionLog:
    action : Action
    executor : int