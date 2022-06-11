from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from utils.database import Base, engine


class CompetitionModel(Base):
    __tablename__ = "competition"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, unique=True, index=True)
    name = Column(String)
    area_name = Column(String)
    teams = relationship("TeamModel", back_populates="competition")


class TeamModel(Base):
    __tablename__ = "team"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    tla = Column(String)
    short_name = Column(String)
    area_name = Column(String)
    email = Column(String)
    competition_id = Column(Integer, ForeignKey("competition.id"))
    competition = relationship("CompetitionModel", back_populates="teams")
    players = relationship("PlayerModel", back_populates="team")


class PlayerModel(Base):
    __tablename__ = "player"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    position = Column(String)
    date_of_birth = Column(String)
    country_of_birth = Column(String)
    nationality = Column(String)
    team_id = Column(Integer, ForeignKey("team.id"))
    team = relationship("TeamModel", back_populates="players")


try:
    Base.metadata.create_all(engine)
except:
    pass
