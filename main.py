from flask import Flask, request, jsonify
from game.game import Game
from game.troop import *
import uuid

app = Flask(__name__)


@dataclass
class GameRoom:
    game: Game


@dataclass
class LobbyRoom:
    isPlayerOneReady: bool = False
    isPlayerTwoReady: bool = False
    playerCount: int = 0


lobbyRooms: dict[str, LobbyRoom] = {}
gameRooms: dict[str, GameRoom] = {}

boardRows = 8
boardCols = 8

"""
output:
{
    "board" : [TroopInfo(...) for _ in range(boardRows) for _ in range(boardCols)],
    "recentMove": [Action(), Action()]
    "playerOneInfo" : {...},
    "playerTwoInfo" : {
        "money" : int
    },
    "curTurn" : int,
}
"""


@app.route("/state/<roomId>")
def getState(roomId):
    # print("Fetching state for room:", roomId)
    # print("Current game rooms:", list(gameRooms.keys()))
    if roomId not in gameRooms:
        print("Game Room not found:", roomId)
        return jsonify({"error": "Game Room not found"}), 404

    state = gameRooms[roomId].game
    return jsonify(state), 200


"""
Input: 
{
    "roomId": str     # TODO: Server-generate?
}
"""


@app.route("/create_room", methods=["POST"])
def createRoom():
    # generate unique roomId
    roomId = str(uuid.uuid4().int)[:6]
    while roomId in gameRooms or roomId in lobbyRooms:
        roomId = str(uuid.uuid4().int)[:6]

    lobbyRooms[roomId] = LobbyRoom(playerCount=1)
    print("Created lobby room:", roomId)

    # Player 1 is the creator
    return (
        jsonify(
            {"message": f"Room {roomId} created!", "playerNum": 1, "roomId": roomId}
        ),
        201,
    )


"""
Input:
{
    "roomId": str
}
"""


@app.route("/join_room", methods=["POST"])
def joinRoom():
    data = request.json or {}
    roomId = data.get("roomId", "default")

    if roomId in gameRooms:
        return jsonify({"error": "Game already started in this room"}), 400

    if roomId not in lobbyRooms:
        return jsonify({"error": "Room not found"}), 404

    lobbyRoom = lobbyRooms[roomId]
    if lobbyRoom.playerCount >= 2:
        return jsonify({"error": "Room is full"}), 400

    lobbyRoom.playerCount += 1

    # Player 2 is the joiner
    return (
        jsonify(
            {"message": f"Joined room {roomId}!", "playerNum": 2, "roomId": roomId}
        ),
        200,
    )


"""
Input:
{
    "playerNum": int
}
"""


@app.route("/ready/<roomId>", methods=["POST"])
def readyUp(roomId):
    if roomId not in lobbyRooms:
        return jsonify({"error": "Room not found"}), 404

    data = request.json or {}
    playerNum = data.get("playerNum")

    if playerNum is None:
        return jsonify({"error": "Player number required"}), 400

    lobbyRoom = lobbyRooms[roomId]
    if playerNum == 1:
        lobbyRoom.isPlayerOneReady = True
    elif playerNum == 2:
        lobbyRoom.isPlayerTwoReady = True
    else:
        return jsonify({"error": "Invalid player number"}), 400

    if lobbyRoom.isPlayerOneReady and lobbyRoom.isPlayerTwoReady:
        del lobbyRooms[roomId]
        initialBoard = [[Empty() for _ in range(boardCols)] for _ in range(boardRows)]

        ## init
        initialBoard[7][3] = King(owner=1, isRevealed=True, health=3)
        initialBoard[0][3] = King(owner=2, isRevealed=True, health=3)


        newGame = Game(board=initialBoard)
        gameRooms[roomId] = GameRoom(game=newGame)

    return (
        jsonify(
            {
                "message": f"Player {playerNum} is ready!",
            }
        ),
        200,
    )


@app.route("/delete_room/<roomId>", methods=["POST"])
def deleteRoom(roomId):
    if roomId in gameRooms:
        del gameRooms[roomId]
        print("Deleted game room:", roomId)
        return jsonify({"message": f"Room {roomId} deleted!"}), 200
    elif roomId in lobbyRooms:
        del lobbyRooms[roomId]
        print("Deleted lobby room:", roomId)
        return jsonify({"message": f"Room {roomId} deleted!"}), 200
    else:
        print("Room not found for deletion:", roomId)
        return jsonify({"error": "Room not found"}), 404


"""
input:
{
    "board" : [TroopInfo(...) for _ in range(boardRows) for _ in range(boardCols)],
    "action" : [Action()]
    "playerNum" : int
    "playerInfo" : {...}
}
"""


@app.route("/action/<roomId>", methods=["POST"])
def handleAction(roomId):
    if roomId not in gameRooms:
        print("Room not found for action:", roomId, "roomIds:", list(gameRooms.keys()))
        return jsonify({"error": "Room not found"}), 404

    receivedData = request.json
    gameRoom = gameRooms[roomId]

    error = gameRoom.game.handleAction(receivedData)
    if error:
        return jsonify(error), 400

    return (
        jsonify({"message": "Move processed!", "yourData": receivedData}),
        201,
    )


@app.route("/room_status/<roomId>")
def roomStatus(roomId):
    if roomId in gameRooms:
        return (
            jsonify(
                {
                    "status": "in_game",
                    "playerOneReady": True,
                    "playerTwoReady": True,
                    "playerCount": 2,
                }
            ),
            200,
        )
    elif roomId in lobbyRooms:
        lobbyRoom = lobbyRooms[roomId]
        return (
            jsonify(
                {
                    "status": "in_lobby",
                    "playerOneReady": lobbyRoom.isPlayerOneReady,
                    "playerTwoReady": lobbyRoom.isPlayerTwoReady,
                    "playerCount": lobbyRoom.playerCount,
                }
            ),
            200,
        )
    else:
        return (
            jsonify(
                {
                    "status": "not_found",
                    "playerOneReady": False,
                    "playerTwoReady": False,
                    "playerCount": 0,
                }
            ),
            200,
        )


if __name__ == "__main__":
    app.run(debug=True, port=5001, host="0.0.0.0")
