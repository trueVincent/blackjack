from sqlalchemy import orm, create_engine, types
from sqlalchemy import *

class _Base(object):
    def add(self):
        with orm.Session(engine) as session:
            session.add(self)
            session.commit()

Base = orm.declarative_base(cls=_Base)
engine = create_engine("sqlite:///storage/test.db", echo=True, future=True)  # TODO: don't use memory-only DB

def add_all(entities):
    with orm.Session(engine) as session:
        session.add_all(entities)
        session.commit()

def get(stmt):
    with orm.Session(engine) as session:
        return session.scalars(stmt)

# init
from bet import Bet
from game import Game
from player import Player
Base.metadata.create_all(engine)