from flask_socketio import SocketIO, emit
from flask import request

# Initialize SocketIO with full CORS and eventlet support
socketio = SocketIO(cors_allowed_origins=[
    "http://localhost:5173",
    "http://10.0.0.165:5173",
    "https://neuralearn-one.vercel.app"
], async_mode="eventlet")

# Player state
lobby_players = []  # [{ sid, username, character }]
player_positions = {}  # sid -> { username, character, x, y }

def register_socket_events(app):
    # Note: init_app is done in app.py, so keep this commented unless using standalone
    # socketio.init_app(app)

    @socketio.on("connect")
    def handle_connect():
        print(f"✅ Client connected: {request.sid}")
        sid = request.sid

        # Ensure player gets a default position (restored on refresh)
        if sid not in player_positions:
            player_positions[sid] = {
                "username": "Anonymous",
                "character": "char0.png",
                "x": 300,
                "y": 300
            }

    @socketio.on("disconnect")
    def handle_disconnect():
        global lobby_players, player_positions
        sid = request.sid
        print(f"❌ Client disconnected: {sid}")

        # Remove from lobby and positions
        lobby_players = [p for p in lobby_players if p.get("sid") != sid]
        if sid in player_positions:
            del player_positions[sid]

        # Broadcast updated state
        emit("lobby_update", {"players": lobby_players}, broadcast=True)
        emit("player_positions", list(player_positions.values()), broadcast=True)

    @socketio.on("player_join")
    def handle_player_join(data):
        global lobby_players, player_positions
        sid = request.sid
        username = data.get("username", "Anonymous")
        character = data.get("character", "char0.png")

        print(f"📨 Player joined: {username}, {character}")

        # Add to lobby
        lobby_players.append({
            "sid": sid,
            "username": username,
            "character": character
        })

        # Set initial position
        player_positions[sid] = {
            "username": username,
            "character": character,
            "x": 300,
            "y": 300
        }

        emit("lobby_update", {"players": lobby_players}, broadcast=True)
        emit("player_positions", list(player_positions.values()), broadcast=True)

    @socketio.on("player_move")
    def handle_player_move(data):
        sid = request.sid
        x = data.get("x")
        y = data.get("y")

        if sid in player_positions:
            player_positions[sid]["x"] = x
            player_positions[sid]["y"] = y

        emit("player_positions", list(player_positions.values()), broadcast=True)

# Used by REST API route
def get_lobby_players():
    return lobby_players
