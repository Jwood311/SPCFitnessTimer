from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()


class Time(Base):
    __tablename__ = 'TimerEntries'

    id = Column(Integer, primary_key=True)
    time = Column(String)

    def to_json(self):
        return self.time

    def __repr__(self):
        return "<Time(time='%s')>" % (self.time)