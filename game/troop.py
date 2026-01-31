from dataclasses import dataclass


@dataclass
class Troop:
    troopType: str = "empty"
    isRevealed: bool = False
    owner: int = -1
    health: int = 0


@dataclass
class Empty(Troop):
    pass

@dataclass
class King(Troop):
    troopType: str = "king"
    health : int = 3

@dataclass
class Banker(Troop):
    troopType : str = "banker"
    health : int = 1


@dataclass
class Guard(Troop):
    troopType: str = "guard"
    health: int = 1


@dataclass
class Assassin(Troop):
    troopType: str = "assassin"
    health: int = 1


@dataclass
class Spy(Troop):
    troopType: str = "spy"
    health: int = 1


@dataclass
class Archer(Troop):
    troopType: str = "archer"
    health: int = 1


# @dataclass
# class Empty(Troop):
#     pass
#
# @dataclass
# class Empty(Troop):
#     pass
#
