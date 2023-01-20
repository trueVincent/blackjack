import random


class Odds:
    blackjack = 1.5
    straight = 3
    three_seven = 3
    five_cards = 3

class Cards:
    def __init__(self, cards):
        self.cards = cards

    def set_deck_of_cards(self):
        for _ in range(4):
            self.cards.extend([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13])

    def add_card(self, num: int):
        if 0 < num < 14:
            self.cards.append(num)
        else:
            raise Exception("card should between 1 and 13")

    def sum(self):
        sum = 0
        has_ace = False
        for card in self.cards:
            if card == 1:
                has_ace = True
            if card > 10:
                sum += 10
            else:
                sum += card
        if has_ace and sum <= 11:
            sum += 10
        return sum

    def get_odds(self):
        sum = self.sum()
        if len(self.cards) >= 5:
            return Odds.five_cards
        if sum == 21 and len(self.cards) == 2:
            return Odds.blackjack
        if sum == 21 and len(self.cards) == 3 and len(set(self.cards)) == 1:
            return Odds.three_seven
        if sum == 21 and sorted(self.cards) == [5, 6, 7]:
            return Odds.straight
        return 1

    def draw_random_card(self):
        card = random.choice(self.cards)
        self.cards.remove(card)
        return card

    def is_bust(self):
        return True if self.sum() > 21 else False