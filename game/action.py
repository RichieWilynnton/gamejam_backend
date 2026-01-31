from dataclasses import dataclass

@dataclass
class Action:
    action_type : str

@dataclass
class Move(Action):
    fromX : int
    fromY : int
    toX : int
    toY : int

@dataclass
class Reveal(Action):
    atX : int
    atY : int

@dataclass
class Spawn(Action):
    atX : int
    atY : int
    troopType : str

@dataclass
class Swap(Action):
    fromX : int
    fromY : int
    toX : int
    toY : int

@dataclass
class Shoot(Action):
    fromX : int
    fromY : int
    toX : int
    toY : int
