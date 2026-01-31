from flask import Flask, request, jsonify
from game.game import Game
from game.troop import *

app = Flask(__name__)

rooms = {}

board_rows = 8
board_cols = 8

"""
json format:
{
    "board" : [TroopInfo(...) for _ in range(boardRows) for _ in range(boardCols)],
    "recent_move": [Action(), Action()]
    "player_one_info" : {...},
    "player_two_info" : {
        "money" : int
    },
    "cur_turn" : int,
}
"""
@app.route("/state/<room_id>")
def get_state(room_id):
    if room_id not in rooms:
        return jsonify({"error": "Room not found"}), 404
    
    state = rooms[room_id]
    return jsonify(state), 200


@app.route("/create_room", methods=["POST"])
def create_room():
    data = request.json or {}
    room_id = data.get("room_id", "default")
    
    if room_id in rooms:
        return jsonify({"error": "Room already exists"}), 400
    
    board = [[Troop() for _ in range(board_cols)] for _ in range(board_rows)]
    rooms[room_id] = Game(board)
    return jsonify({"message": f"Room {room_id} created!", "player_num": 0}), 201


@app.route("/join_room", methods=["POST"])
def join_room():
    data = request.json or {}
    room_id = data.get("room_id", "default")
    
    if room_id not in rooms:
        return jsonify({"error": "Room not found"}), 404
    
    # Logic to ensure only two players join could go here
    return jsonify({"message": f"Joined room {room_id}!", "player_num": 1}), 200

@app.route("/delete_room/<room_id>", methods=["POST"])
def delete_room(room_id):
    if room_id in rooms:
        del rooms[room_id]
        return jsonify({"message": f"Room {room_id} deleted!"}), 200
    else:
        return jsonify({"error": "Room not found"}), 404


"""
input:
{
    "board" : [TroopInfo(...) for _ in range(boardRows) for _ in range(boardCols)],
    "move" : [Action()]
    "player_num" : int
    "player_info" : {...}
}
"""
@app.route("/move/<room_id>", methods=["POST"])
def handle_move(room_id):
    if room_id not in rooms:
        return jsonify({"error": "Room not found"}), 404
        
    received_data = request.json
    game = rooms[room_id]

    game.handle_move(received_data)
    
    print(f"Received move for room {room_id}: {received_data}")

    return (
        jsonify({"message": "Move processed!", "your_data": received_data}),
        201,
    )

if __name__ == "__main__":
    app.run(debug=True, port=5001)
