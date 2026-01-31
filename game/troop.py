from dataclasses import dataclass

@dataclass
class Troop:
    troopType : str = "empty"
    revealed : bool = False
    owner : int = -1
    health : int = 0

@dataclass 
class Empty(Troop):
    pass

@dataclass 
class Banker(Troop):
    pass

# @dataclass 
# class Empty(Troop):
#     pass
#
# @dataclass 
# class Empty(Troop):
#     pass
#
