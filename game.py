from cards import Cards


class GameStatus:
    waiting = 0
    starting = 1
    playerSpecialActing = 2
    playerCalling = 3
    dealerCalling = 4
    ending = 5


class Game:
    MAX_PLAYER_NUM = 6

    def __init__(self, id):
        self.id = id
        self.status = GameStatus.waiting
        self.cards = Cards()
        self.cards.set_deck_of_cards()
        self.player_bets = []
        self.dealer_bet = None
        self.current_bet = None

    def start(self):
        def can_start():
            return self.dealer_bet and self.player_bets

        if not can_start():
            return False
        self.status = GameStatus.starting
        for bet in self.player_bets:
            bet.hit()
            bet.hit()
        self.dealer_bet.hit()
        self.dealer_bet.hit()
        self.next_bet()
        self.status = GameStatus.playerCalling
        return True

    def close(self):
        self.current_bet = None
        dealer_cards_sum = self.dealer_bet.cards.sum()
        dealer_cards_len = len(self.dealer_bet.cards.cards)
        for bet in self.player_bets:
            player_cards_sum = bet.cards.sum()
            player_cards_len = len(bet.cards.cards)

            if (dealer_cards_sum > 21 and player_cards_sum > 21) or (dealer_cards_sum == player_cards_sum) or (dealer_cards_len >= 5 and player_cards_len >= 5):
                odds = 0
            elif dealer_cards_sum > 21 or player_cards_len >= 5:
                odds = bet.cards.get_odds()
            elif player_cards_sum > 21 or dealer_cards_len >= 5:
                odds = -self.dealer_bet.cards.get_odds()
            elif dealer_cards_sum > player_cards_sum:
                odds = -self.dealer_bet.cards.get_odds()
            elif dealer_cards_sum < player_cards_sum:
                odds = bet.cards.get_odds()

            self.dealer_bet.balance += bet.points * -odds
            self.dealer_bet.player.points += bet.points * -odds
            bet.balance = bet.points * odds
            bet.player.points += bet.points * odds

        self.status = GameStatus.ending

    def hit(self):
        return self.cards.get_random_card()

    def add_bet(self, bet):
        if self.status == GameStatus.waiting and len(self.player_bets) <= self.MAX_PLAYER_NUM:
            self.player_bets.append(bet)
            return True
        else:
            return False

    def is_full(self):
        if self.status != GameStatus.waiting or len(self.player_bets) >= self.MAX_PLAYER_NUM:
            return True
        return False

    def be_dealer(self, bet):
        if self.dealer_bet:
            return False
        self.dealer_bet = bet
        self.player_bets.remove(bet)
        return True

    def next_bet(self):
        if not self.current_bet:
            self.current_bet = self.player_bets[0]
            return
        idx = self.player_bets.index(self.current_bet)
        if idx + 1 == len(self.player_bets):
            self.current_bet = self.dealer_bet
            return
        self.current_bet = self.player_bets[idx + 1]

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
                "cards": self.dealer_bet.cards.cards,
                "cards_sum": self.dealer_bet.cards.sum(),
                "is_current": self.current_bet == self.dealer_bet,
            },
            "players": [{
                "name": bet.player.name,
                "bet": bet.points,
                "cards": bet.cards.cards,
                "cards_sum": bet.cards.sum(),
                "is_current": self.current_bet == bet,
            } for bet in self.player_bets],
        }

    def is_last_bet(self):
        return self.current_bet == self.dealer_bet

    def get_result(self):
        return {
            "dealer": {
                "name": self.dealer_bet.player.name,
                "bet": self.dealer_bet.points,
                "cards": self.dealer_bet.cards.cards,
                "balance": self.dealer_bet.balance,
            },
            "players": [{
                "name": bet.player.name,
                "bet": bet.points,
                "cards": bet.cards.cards,
                "balance": bet.balance,
            } for bet in self.player_bets],
        }