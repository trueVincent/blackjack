import socketio

from shared import db  # init first
from game import Game
from player import Player
from bet import Bet

sio = socketio.Server(async_mode='eventlet', cors_allowed_origins="*")
app = socketio.WSGIApp(sio, static_files={
    '/': './public/'
})
# Command to start server: gunicorn -b 0.0.0.0:80 -k eventlet -w 1 --reload app:app

GAME = Game()
GAME.add()
BET_MAP = {}  # sid: bet

# FIX: 斷線處理

def create_game():
    global GAME
    GAME = Game()
    GAME.add()

@sio.event
def create_player(sid, name):
    payload = {
        "name": "",
        "points": 0,
        "success": False
    }
    stmt = db.select(Player).where(Player.name == name)
    if not db.get(stmt):
        player = Player(name)
        player.add()
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
    stmt = db.select(Player).where(Player.name == name)
    player = db.get(stmt)
    if player:
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
    stmt = db.select(Player).where(Player.name == name)
    player = db.get(stmt)
    bet = Bet(GAME, player)
    bet.add()
    BET_MAP[sid] = bet
    sio.enter_room(sid, GAME.id)
    sio.emit("join_game_result", to=sid)

    payload = GAME.get_waiting_room_details()
    sio.emit("get_waiting_room_details", payload, room=GAME.id)

@sio.event
def get_waiting_room_details(sid):
    game = BET_MAP[sid].game
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
    try:
        game.start()
        sio.emit("start_game_result", True, to=sid)
        sio.emit("wait_game_start", room=game.id)
    except:
        sio.emit("start_game_result", False, to=sid)

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
