from shared import db


class Player(db.Base):
    __tablename__ = "player"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True)
    points = db.Column(db.Integer)

    def __init__(self, name):
        self.name = name
        self.points = 10000