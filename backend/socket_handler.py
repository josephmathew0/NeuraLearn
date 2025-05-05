# File: backend/socket_handler.py

from flask_socketio import SocketIO, emit
from flask import request

# Initialize SocketIO
socketio = SocketIO()

# Player state
players = {}  # sid -> { username, character, role, x, y }
correct_answers = {}  # sid -> int
winner_sid = None
game_over = False

@socketio.on("connect")
def handle_connect():
    sid = request.sid
    print(f"🔌 Connected: {sid}")

@socketio.on("player_join")
def handle_player_join(data):
    sid = request.sid
    username = data.get("username")
    character = data.get("character")

    # ✅ Assign role based on character image
    if character in ["char4.png", "char5.png"]:
        role = "murderer"
    else:
        role = "player"

    if not sid or not username:
        return

    players[sid] = {
        "sid": sid,
        "username": username,
        "character": character,
        "role": role,
        "x": 300,
        "y": 300,
    }

    print(f"🎭 Player Joined → {username} ({character}) Role: {role}")
    emit("start_game", {"role": role}, room=sid)
    emit("player_data", players[sid])
    emit("player_list", list(players.values()), broadcast=True)

# @socketio.on("player_move")
# def handle_player_move(pos):
#     sid = request.sid
#     if sid in players:
#         players[sid]["x"] = pos.get("x", 300)
#         players[sid]["y"] = pos.get("y", 300)

#         # Prevent overwriting role from frontend in case of desync
#         incoming_role = pos.get("role")
#         if incoming_role and players[sid]["role"] != incoming_role:
#             print(f"⚠️ Role mismatch for {players[sid]['username']} — ignoring update to preserve assigned role.")

#         emit("player_positions", list(players.values()), broadcast=True)


@socketio.on("player_move")
def handle_player_move(pos):
    sid = request.sid
    if sid in players:
        players[sid]["x"] = pos.get("x", 300)
        players[sid]["y"] = pos.get("y", 300)

        # Character image tracking
        incoming_character = pos.get("character")
        if incoming_character:
            players[sid]["character"] = incoming_character  # track character image

        # Role protection (optional, if roles still matter later)
        incoming_role = pos.get("role")
        if incoming_role and players[sid]["role"] != incoming_role:
            print(f"⚠️ Role mismatch for {players[sid]['username']} — ignoring update to preserve assigned role.")

        emit("player_positions", list(players.values()), broadcast=True)


@socketio.on("question_correct")
def handle_question_correct():
    global game_over, winner_sid

    sid = request.sid
    if game_over:
        return

    correct_answers[sid] = correct_answers.get(sid, 0) + 1
    print(f"✅ {players[sid]['username']} now has {correct_answers[sid]} correct answers")

    if correct_answers[sid] >= 10:
        winner_sid = sid
        game_over = True
        winner = players[sid]["username"]
        murderers = [p["username"] for p in players.values() if p["role"] == "murderer"]

        print(f"🏆 Game Over! Winner: {winner}")
        emit("game_over", {"winner": winner, "murderers": murderers}, broadcast=True)

@socketio.on("disconnect")
def handle_disconnect():
    sid = request.sid
    if sid in players:
        print(f"❌ {players[sid]['username']} disconnected")
        del players[sid]
    if sid in correct_answers:
        del correct_answers[sid]

    emit("player_list", list(players.values()), broadcast=True)
    emit("player_positions", list(players.values()), broadcast=True)


# Add to socket_handler.py
@socketio.on("game_over")
def handle_game_over(data):
    print("🏁 Game Over Triggered:", data)
    winner = data.get("winner")
    murderers = data.get("murderers", [])

    emit("game_over", {
        "winner": winner,
        "murderers": murderers
    }, broadcast=True)


# Optional helper
def get_all_players():
    return list(players.values())
