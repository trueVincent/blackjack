import datetime

from cards import Cards
from shared import db


BASE_BET = 1000

class Bet(db.Base):
    __tablename__ = "bet"

    id = db.Column(db.Integer, primary_key=True)
    points = db.Column(db.Integer, default=BASE_BET)
    is_dealer = db.Column(db.Boolean, default=False)
    is_resign = db.Column(db.Boolean, default=False)
    is_current = db.Column(db.Boolean, default=False)
    balance = db.Column(db.Integer, default=0)
    cards = db.Column(db.MutableList.as_mutable(db.PickleType), default=[])
    created_time = db.Column(db.DateTime, default=datetime.datetime.now())

    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)
    game = db.orm.relationship("Game", back_populates="bets")

    player_id = db.Column(db.Integer, db.ForeignKey("player.id"), nullable=False)
    player = db.orm.relationship("Player")

    def __init__(self, game, player):
        self.game = game
        self.player = player
        self.cards = []

    def be_dealer(self):
        if self.game.dealer_bet:
            return False
        self.is_dealer = True
        return True

    def resign(self):
        self.is_regisn = True
        self.add()

    def hit(self):
        cards = Cards(self.cards)
        card = self.game.hit()
        cards.add_card(card)
        self.cards = cards.cards
        return card