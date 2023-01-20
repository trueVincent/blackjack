from sqlalchemy import orm, create_engine, types
from sqlalchemy import *
from sqlalchemy.ext.mutable import MutableList

class _Base(object):
    def add(self):
        with orm.Session(engine) as session:
            session.add(self)
            session.commit()

Base = orm.declarative_base(cls=_Base)
engine = create_engine("sqlite:///storage/data.db", echo=False, future=True)

def add_all(entities):
    with orm.Session(engine) as session:
        session.add_all(entities)
        session.commit()

def get(stmt):
    with orm.Session(engine) as session:
        return session.scalars(stmt)

def create_session():
    Session = orm.sessionmaker(bind=engine)
    session = Session()
    return session

# init
from bet import Bet
from game import Game
from player import Player
Base.metadata.create_all(engine)