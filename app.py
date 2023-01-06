import socketio

from shared import db  # init first
from game import Game
from player import Player
from bet import Bet
from cards import Cards

sio = socketio.Server(async_mode='eventlet', cors_allowed_origins="*")
app = socketio.WSGIApp(sio, static_files={
    '/': './public/'
})
# Command to start server: gunicorn -b 0.0.0.0:80 -k eventlet -w 1 --reload app:app

GAME_ID = -1
BET_MAP = {}  # sid: bet

# FIX: 斷線處理
# TODO: 封裝 DB layer，處理 DB session 連線太亂

def create_game():
    global GAME_ID
    GAME_ID = Game().add()

@sio.event
def create_player(sid, name):
    payload = {
        "name": "",
        "points": 0,
        "success": False
    }
    with db.orm.Session(db.engine) as session:
        player = session.query(Player).filter_by(name=name).first()
    if not player:
        player = Player(name)
        payload["name"] = name
        payload["points"] = player.points
        payload["success"] = True
        player.add()
    sio.emit("create_player_result", payload, to=sid)

@sio.event
def get_player(sid, name):
    payload = {
        "name": "",
        "points": 0,
        "success": False
    }
    with db.orm.Session(db.engine) as session:
        player = session.query(Player).filter_by(name=name).first()
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
    global GAME_ID
    session = db.create_session()
    game = session.query(Game).filter_by(id=GAME_ID).first()
    if GAME_ID == -1 or not game or game.is_full():
        game = Game()
        session.add(game)
        session.commit()
        GAME_ID = game.id

    cards = Cards(game.cards)
    cards.set_deck_of_cards()
    game.cards = cards.cards

    name = sio.get_session(sid)["name"]
    player = session.query(Player).filter_by(name=name).first()
    bet = Bet(game, player)
    session.add_all([bet, game])
    session.commit()
    BET_MAP[sid] = bet.id
    game_id = game.id
    payload = game.get_waiting_room_details()
    session.close()

    sio.enter_room(sid, game_id)
    sio.emit("join_game_result", to=sid)
    sio.emit("get_waiting_room_details", payload, room=game_id)

@sio.event
def get_waiting_room_details(sid):
    session = db.create_session()
    bet = session.query(Bet).filter_by(id=BET_MAP[sid]).first()
    game = bet.game
    payload = game.get_waiting_room_details()
    sio.emit("get_waiting_room_details", payload, to=sid)
    session.close()

@sio.event
def be_dealer(sid):
    session = db.create_session()
    bet = session.query(Bet).filter_by(id=BET_MAP[sid]).first()
    game = bet.game
    res = bet.be_dealer()
    session.add(bet)
    session.commit()
    sio.emit("be_dealer_result", res, to=sid)

    if res:
        payload = game.get_waiting_room_details()
        sio.emit("get_waiting_room_details", payload, room=game.id)
    session.close()

@sio.event
def start_game(sid):
    session = db.create_session()
    bet = session.query(Bet).filter_by(id=BET_MAP[sid]).first()
    game = bet.game
    if game.can_start():
        game.start()
        session.add(game)
        session.add_all(game.bets)
        session.commit()
        sio.emit("start_game_result", True, to=sid)
        sio.emit("wait_game_start", room=game.id)
    else:
        sio.emit("start_game_result", False, to=sid)
    session.close()

# keep doing from here
@sio.event
def get_game_detail(sid):
    session = db.create_session()
    bet = session.query(Bet).filter_by(id=BET_MAP[sid]).first()
    game = bet.game
    payload = game.get_game_detail()
    sio.emit("get_game_detail", payload, to=sid)
    session.close()

@sio.event
def hit(sid):
    session = db.create_session()
    bet = session.query(Bet).filter_by(id=BET_MAP[sid]).first()
    game = bet.game
    bet.hit()
    if Cards(bet.cards).is_bust():
        if game.is_last_bet():
            game.close()
            sio.emit("game_end", room=game.id)
        else:
            game.next_bet()
    payload = game.get_game_detail()
    sio.emit("get_game_detail", payload, room=game.id)
    session.add_all(game.bets)
    session.add(game)
    session.commit()
    session.close()

@sio.event
def stand(sid):
    session = db.create_session()
    bet = session.query(Bet).filter_by(id=BET_MAP[sid]).first()
    game = bet.game
    if game.is_last_bet():
        game.close()
        sio.emit("game_end", room=game.id)
    else:
        game.next_bet()
        payload = game.get_game_detail()
        sio.emit("get_game_detail", payload, room=game.id)
    session.add_all(game.bets)
    session.add(game)
    session.commit()
    session.close()
    
@sio.event
def get_result(sid):
    session = db.create_session()
    bet = session.query(Bet).filter_by(id=BET_MAP[sid]).first()
    game = bet.game
    payload = game.get_result()
    sio.emit("get_result", payload, to=sid)
    session.close()
