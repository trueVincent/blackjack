from cards import Cards
from shared import db


class GameStatus:
    waiting = 0
    playerSpecialActing = 1
    playerCalling = 2
    dealerCalling = 3
    ending = 4


class Game(db.Base):
    __tablename__ = "game"

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, default=GameStatus.waiting)
    cards = db.Column(db.PickleType)

    bets = db.orm.relationship("Bet", back_populates="game")

    MAX_PLAYER_NUM = 6

    @property
    def dealer_bet(self):
        for bet in self.bets:
            if bet.is_dealer: return bet

    @property
    def player_bets(self):
        return [bet for bet in self.bets if not bet.is_dealer]

    @property
    def current_bet(self):
        for bet in self.bets:
            if bet.is_current: return bet

    def __init__(self):
        cards = Cards([])
        cards.set_deck_of_cards()
        self.cards = cards.cards

    def can_start(self):
        return self.dealer_bet and len(self.bets) >= 2

    def start(self):
        if not self.can_start():
            raise Exception("Need a dealer and at least a player to start the game.")
        [bet.hit() for bet in self.bets]
        self.next_bet()
        self.status = GameStatus.playerCalling
        self.add()

    def close(self):
        dealer_cards = Cards(self.dealer_bet.cards)
        dealer_cards_sum = dealer_cards.sum()
        dealer_cards_len = len(dealer_cards.cards)
        for bet in self.player_bets:
            player_cards = Cards(bet.cards)
            player_cards_sum = player_cards.sum()
            player_cards_len = len(player_cards.cards)

            if (dealer_cards_sum > 21 and player_cards_sum > 21) or (dealer_cards_sum == player_cards_sum) or (dealer_cards_len >= 5 and player_cards_len >= 5):
                odds = 0
            elif dealer_cards_sum > 21 or player_cards_len >= 5:
                odds = player_cards.get_odds()
            elif player_cards_sum > 21 or dealer_cards_len >= 5:
                odds = -dealer_cards.get_odds()
            elif dealer_cards_sum > player_cards_sum:
                odds = -dealer_cards.get_odds()
            elif dealer_cards_sum < player_cards_sum:
                odds = player_cards.get_odds()

            self.dealer_bet.balance += bet.points * -odds
            self.dealer_bet.player.points += bet.points * -odds
            bet.balance = bet.points * odds
            bet.player.points += bet.points * odds

        self.status = GameStatus.ending
        self.add()
        db.add_all(self.bets)

    def hit(self):
        cards = Cards(self.cards)
        card = cards.draw_random_card()
        self.cards = cards.cards
        self.add()
        return card

    def add_bet(self, bet):
        if self.status == GameStatus.waiting and len(self.bets) <= self.MAX_PLAYER_NUM:
            self.bets.append(bet)
            return True
        else:
            return False

    def is_full(self):
        if self.status != GameStatus.waiting or len(self.bets) >= self.MAX_PLAYER_NUM:
            return True
        return False

    def be_dealer(self, bet):
        if self.dealer_bet:
            return False
        self.dealer_bet = bet
        self.player_bets.remove(bet)
        self.add()
        return True

    def is_last_bet(self):
        return self.current_bet == self.dealer_bet

    def next_bet(self):
        if not self.current_bet:
            self.player_bets[0].is_current = True
            self.player_bets[0].add()
            return
        idx = self.player_bets.index(self.current_bet)
        if idx + 1 == len(self.player_bets):
            self.current_bet = self.dealer_bet
            return
        self.player_bets[idx + 1].is_current = True
        self.player_bets[idx].is_current = False
        db.add_all(self.player_bets[idx + 1], self.player_bets[idx])

    def get_waiting_room_details(self):
        return {
            "game_id": self.id,
            "dealer_name": self.dealer_bet.player.name if self.dealer_bet else "",
            "player_names": [bet.player.name for bet in self.player_bets],
        }

    def get_game_detail(self):
        return {
            "dealer": {
                "name": self.dealer_bet.player.name,
                "bet": self.dealer_bet.points,
                "cards": self.dealer_bet.cards,
                "cards_sum": self.dealer_bet.cards.sum(),
                "is_current": self.dealer_bet.is_current,
            },
            "players": [{
                "name": bet.player.name,
                "bet": bet.points,
                "cards": bet.cards.cards,
                "cards_sum": bet.cards.sum(),
                "is_current": bet.is_current,
            } for bet in self.player_bets],
        }

    def get_result(self):
        return {
            "dealer": {
                "name": self.dealer_bet.player.name,
                "bet": self.dealer_bet.points,
                "cards": self.dealer_bet.cards,
                "balance": self.dealer_bet.balance,
            },
            "players": [{
                "name": bet.player.name,
                "bet": bet.points,
                "cards": bet.cards.cards,
                "balance": bet.balance,
            } for bet in self.player_bets],
        }