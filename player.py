class Player:
    def __init__(self, name):
        self.id = 0  # TODO: should be unique, should't be sid
        self.name = name
        self.points = 10000
        self.current_game = None
        self.current_bet = None

    def again(self):
        pass

    def leave(self):
        pass