from dataclasses import dataclass, field

from game.troop import *
from game.action import *
from game.player import *

@dataclass
class Game:
    board : list[list[Troop]]
    player_one_info : Player = field(default_factory=Player)
    player_two_info : Player = field(default_factory=Player)
    cur_turn : int = 0
    recent_move : list[Action] = field(default_factory=list)

    def handle_move(self, moveJson):
        cur_player = moveJson["player_num"]
        board_data = moveJson["board"]
        recent_move_data = moveJson["recent_move"]
        player_info_data = moveJson["player_info"]
        self.handle_board(board_data)
        self.handle_recent_move(recent_move_data)
        self.handle_player_info(cur_player, player_info_data)

        self.cur_turn += 1

    def handle_board(self, board_data):
        for i in range(len(board_data)):
            for j in range(len(board_data[i])):
                troop_data = board_data[i][j]

                troop_type = troop_data["troopType"]
                cur_troop = None
                if troop_type == "empty":
                    cur_troop = Empty(**troop_data)
                elif troop_type == "banker":
                    cur_troop = Banker(**troop_data)

                if cur_troop is None:
                    print("Unknown troop type:", troop_type)
                    continue

                self.board[i][j] = cur_troop

    def handle_recent_move(self, recent_move_data):
        for recent_action in recent_move_data:
            action_type = recent_action.get("action_type")

            new_action = None 

            if action_type == "move":
                new_action = Move(**recent_action)
            elif action_type == "reveal":
                new_action = Shoot(**recent_action)
            elif action_type == "spawn":
                new_action = Spawn(**recent_action)
            elif action_type == "swap":
                new_action = Swap(**recent_action)
            elif action_type == "shoot":
                new_action = Shoot(**recent_action)

            if new_action is None:
                print("Unknown action type:", action_type)
                continue
            
            self.recent_move.append(new_action)

    def handle_player_info(self, cur_player, player_info_data):
        if cur_player == 0:
            self.player_one_info = Player(**player_info_data)
        else:
            self.player_two_info = Player(**player_info_data)



