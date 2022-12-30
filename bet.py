from cards import Cards


BASE_BET = 1000

class Bet:
    def __init__(self, game, player):
        self.id = 0
        self.points = BASE_BET
        self.cards = Cards()
        self.is_dealer = False
        self.is_resign = False
        self.game = game
        self.player = player
        self.balance = 0

    def be_dealer(self):
        success = self.game.be_dealer(self)
        if success:
            self.is_dealer = True
        return success

    def resign(self):
        self.is_regisn = True

    def hit(self):
        card = self.game.hit()
        self.cards.add_card(card)
        return card