import socketio

from game import Game
from player import Player
from bet import Bet

sio = socketio.Server(async_mode='eventlet', cors_allowed_origins="*")
app = socketio.WSGIApp(sio, static_files={
    '/': './public/'
})
# Command to start server: gunicorn -b 0.0.0.0:80 -k eventlet -w 1 --reload app:app
# Or gunicorn --reload --threads 50 app:app

GAME_ID = 0
GAME = Game(GAME_ID)
PLAYER_MAP = {}  # name: player
BET_MAP = {}  # sid: bet

# FIX: 斷線處理

def create_game():
    global GAME_ID, GAME
    GAME_ID += 1
    GAME = Game(GAME_ID)

@sio.event
def create_player(sid, name):
    payload = {
        "name": "",
        "points": 0,
        "success": False
    }
    if name not in PLAYER_MAP:
        player = Player(name)
        PLAYER_MAP[name] = player
        payload["name"] = name
        payload["points"] = player.points
        payload["success"] = True
    sio.emit("create_player_result", payload, to=sid)

@sio.event
def get_player(sid, name):
    payload = {
        "name": "",
        "points": 0,
        "success": False
    }
    if name in PLAYER_MAP:
        player = PLAYER_MAP[name]
        payload["name"] = name
        payload["points"] = player.points
        payload["success"] = True
        sio.save_session(sid, {"name": name})
    sio.emit("get_player_result", payload, to=sid)

@sio.event
def logout(sid):
    sio.save_session(sid, {})
    sio.emit("logout_result", to=sid)

@sio.event
def join_game(sid):
    if GAME.is_full():
        create_game()
    name = sio.get_session(sid)["name"]
    player = PLAYER_MAP[name]
    bet = Bet(GAME, player)
    player.current_game = GAME
    player.current_bet = bet
    BET_MAP[sid] = bet
    GAME.add_bet(bet)
    sio.enter_room(sid, GAME_ID)
    sio.emit("join_game_result", to=sid)

    payload = GAME.get_waiting_room_details()
    sio.emit("get_waiting_room_details", payload, room=GAME_ID)

@sio.event
def get_waiting_room_details(sid):
    bet = BET_MAP[sid]
    game = bet.game
    payload = game.get_waiting_room_details()
    sio.emit("get_waiting_room_details", payload, to=sid)

@sio.event
def be_dealer(sid):
    bet = BET_MAP[sid]
    game = bet.game
    res = bet.be_dealer()
    sio.emit("be_dealer_result", res, to=sid)

    if res:
        payload = game.get_waiting_room_details()
        sio.emit("get_waiting_room_details", payload, room=game.id)

@sio.event
def start_game(sid):
    game = BET_MAP[sid].game
    res = game.start()
    sio.emit("start_game_result", res, to=sid)

    if res:
        sio.emit("wait_game_start", room=game.id)

@sio.event
def get_game_detail(sid):
    game = BET_MAP[sid].game
    payload = game.get_game_detail()
    sio.emit("get_game_detail", payload, to=sid)

@sio.event
def hit(sid):
    bet = BET_MAP[sid]
    game = bet.game
    bet.hit()
    if bet.cards.is_bust():
        if game.is_last_bet():
            game.close()
            sio.emit("game_end", room=game.id)
            return
        else:
            game.next_bet()
    payload = game.get_game_detail()
    sio.emit("get_game_detail", payload, room=game.id)

@sio.event
def stand(sid):
    bet = BET_MAP[sid]
    game = bet.game
    if game.is_last_bet():
        game.close()
        sio.emit("game_end", room=game.id)
        return
    game.next_bet()
    payload = game.get_game_detail()
    sio.emit("get_game_detail", payload, room=game.id)
    
@sio.event
def get_result(sid):
    game = BET_MAP[sid].game
    payload = game.get_result()
    sio.emit("get_result", payload, to=sid)
