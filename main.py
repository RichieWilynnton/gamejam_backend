from flask import Flask, request, jsonify
from game.game import Game
from game.troop import *

app = Flask(__name__)

rooms = {}

boardRows = 8
boardCols = 8

"""
json format:
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
    if roomId not in rooms:
        return jsonify({"error": "Room not found"}), 404
    
    state = rooms[roomId]
    return jsonify(state), 200


@app.route("/create_room", methods=["POST"])
def createRoom():
    data = request.json or {}
    roomId = data.get("roomId", "default")
    
    if roomId in rooms:
        return jsonify({"error": "Room already exists"}), 400
    
    board = [[Troop() for _ in range(boardCols)] for _ in range(boardRows)]
    rooms[roomId] = Game(board)
    return jsonify({"message": f"Room {roomId} created!", "playerNum": 0}), 201


@app.route("/join_room", methods=["POST"])
def joinRoom():
    data = request.json or {}
    roomId = data.get("roomId", "default")
    
    if roomId not in rooms:
        return jsonify({"error": "Room not found"}), 404
    
    # Logic to ensure only two players join could go here
    return jsonify({"message": f"Joined room {roomId}!", "playerNum": 1}), 200

@app.route("/delete_room/<roomId>", methods=["POST"])
def deleteRoom(roomId):
    if roomId in rooms:
        del rooms[roomId]
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
    if roomId not in rooms:
        return jsonify({"error": "Room not found"}), 404
        
    receivedData = request.json
    game = rooms[roomId]

    game.handleMove(receivedData)
    
    print(f"Received move for room {roomId}: {receivedData}")

    return (
        jsonify({"message": "Move processed!", "yourData": receivedData}),
        201,
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)
