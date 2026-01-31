from flask import Flask, request, jsonify
from game.game import Game
from game.troop import *

app = Flask(__name__)

@dataclass
class GameRoom:
    game : Game

@dataclass
class LobbyRoom:
    isPlayerOneReady : bool = False
    isPlayerTwoReady : bool = False
    playerCount : int = 0

lobbyRooms : dict[str, LobbyRoom] = {}
gameRooms : dict[str, GameRoom] = {}

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
    if roomId not in gameRooms:
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
    data = request.json or {}
    roomId = data.get("roomId", "default")
    
    if roomId in gameRooms or roomId in lobbyRooms:
        return jsonify({"error": "Room already exists"}), 400
    
    lobbyRooms[roomId] = LobbyRoom(playerCount=1)

    # Player 0 is the creator
    return jsonify({"message": f"Room {roomId} created!", "playerNum": 0}), 201

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

    # Player 1 is the joiner
    return jsonify({"message": f"Joined room {roomId}!", "playerNum": 1}), 200

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
        newGame = Game(board=initialBoard)
        gameRooms[roomId] = GameRoom(game=newGame)
    
    return jsonify({
        "message": f"Player {playerNum} is ready!",
    }), 200

@app.route("/delete_room/<roomId>", methods=["POST"])
def deleteRoom(roomId):
    if roomId in gameRooms:
        del gameRooms[roomId]
        return jsonify({"message": f"Room {roomId} deleted!"}), 200
    elif roomId in lobbyRooms:
        del lobbyRooms[roomId]
        return jsonify({"message": f"Room {roomId} deleted!"}), 200
    else:
        return jsonify({"error": "Room not found"}), 404


"""
input:
{
    "board" : [TroopInfo(...) for _ in range(boardRows) for _ in range(boardCols)],
    "move" : [Action()]
    "playerNum" : int
    "playerInfo" : {...}
}
"""
@app.route("/move/<roomId>", methods=["POST"])
def handleMove(roomId):
    if roomId not in gameRooms:
        return jsonify({"error": "Room not found"}), 404
        
    receivedData = request.json
    gameRoom = gameRooms[roomId]

    error = gameRoom.game.handleMove(receivedData)
    if error:
        return jsonify(error), 400
    
    print(f"Received move for room {roomId}: {receivedData}")

    return (
        jsonify({"message": "Move processed!", "yourData": receivedData}),
        201,
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)
