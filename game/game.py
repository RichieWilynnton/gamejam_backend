from dataclasses import dataclass, field

from game.troop import *
from game.action import *
from game.log import *
from game.player import *


@dataclass
class Game:
    board: list[list[Troop]]
    playerOneInfo: Player = field(default_factory=Player)
    playerTwoInfo: Player = field(default_factory=Player)
    curTurn: int = 0
    actionLog: list[ActionLog] = field(default_factory=list)

    def handleAction(self, moveJson):
        curPlayer = moveJson["playerNum"]
        boardData = moveJson["board"]
        recentActionData = moveJson["action"]
        playerInfoData = moveJson["playerInfo"]
        self.handleBoard(boardData)
        self.handleRecentAction(recentActionData, curPlayer)
        self.handlePlayerInfo(curPlayer, playerInfoData)

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
                elif troopType == "king":
                    curTroop = King(**troopData)
                elif troopType == "guard":
                    curTroop = Guard(**troopData)
                elif troopType == "assassin":
                    curTroop = Assassin(**troopData)
                elif troopType == "spy":
                    curTroop = Spy(**troopData)
                elif troopType == "archer":
                    curTroop = Archer(**troopData)

                if curTroop is None:
                    print("Unknown troop type:", troopType)
                    continue

                self.board[i][j] = curTroop

    def handleRecentAction(self, recentActionData, curPlayer):
        actionType = recentActionData.get("actionType")

        newAction = None

        if actionType == "move":
            newAction = Move(**recentActionData)
        elif actionType == "reveal":
            newAction = Reveal(**recentActionData)
        elif actionType == "spawn":
            newAction = Spawn(**recentActionData)
        elif actionType == "swap":
            newAction = Swap(**recentActionData)
        elif actionType == "shoot":
            newAction = Shoot(**recentActionData)
        elif actionType == "endTurn":
            newAction = EndTurn(**recentActionData)
            self.curTurn += 1

        if newAction is None:
            print("Unknown action type:", actionType)
            return

        self.actionLog.append(ActionLog(action=newAction, executor=curPlayer))

    def handlePlayerInfo(self, curPlayer, playerInfoData):
        if curPlayer == 1:
            self.playerOneInfo = Player(**playerInfoData)
        else:
            self.playerTwoInfo = Player(**playerInfoData)
