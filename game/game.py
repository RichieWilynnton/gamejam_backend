from dataclasses import dataclass, field

from game.troop import *
from game.action import *
from game.player import *

@dataclass
class Game:
    board : list[list[Troop]]
    playerOneInfo : Player = field(default_factory=Player)
    playerTwoInfo : Player = field(default_factory=Player)
    curTurn : int = 0
    recentMove : list[Action] = field(default_factory=list)

    def handleMove(self, moveJson):
        curPlayer = moveJson["playerNum"]
        boardData = moveJson["board"]
        recentMoveData = moveJson["recentMove"]
        playerInfoData = moveJson["playerInfo"]
        self.handleBoard(boardData)
        self.handleRecentMove(recentMoveData)
        self.handlePlayerInfo(curPlayer, playerInfoData)

        self.curTurn += 1
        return None

    def handleBoard(self, boardData):
        for i in range(len(boardData)):
            for j in range(len(boardData[i])):
                troopData = boardData[i][j]

                troopType = troopData["troopType"]
                curTroop = None
                if troopType == "empty":
                    curTroop = Empty(**troopData)
                elif troopType == "banker":
                    curTroop = Banker(**troopData)

                if curTroop is None:
                    print("Unknown troop type:", troopType)
                    continue

                self.board[i][j] = curTroop

    def handleRecentMove(self, recentMoveData):
        for recentAction in recentMoveData:
            actionType = recentAction.get("actionType")

            newAction = None 

            if actionType == "move":
                newAction = Move(**recentAction)
            elif actionType == "reveal":
                newAction = Shoot(**recentAction)
            elif actionType == "spawn":
                newAction = Spawn(**recentAction)
            elif actionType == "swap":
                newAction = Swap(**recentAction)
            elif actionType == "shoot":
                newAction = Shoot(**recentAction)

            if newAction is None:
                print("Unknown action type:", actionType)
                continue
            
            self.recentMove.append(newAction)

    def handlePlayerInfo(self, curPlayer, playerInfoData):
        if curPlayer == 1:
            self.playerOneInfo = Player(**playerInfoData)
        else:
            self.playerTwoInfo = Player(**playerInfoData)



