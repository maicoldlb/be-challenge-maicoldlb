import logging
from typing import Any, Dict, List

from sqlalchemy.orm import Session

from config import config
from db.models import CompetitionModel, TeamModel

logger = logging.getLogger("uvicorn.error")

HEADERS = {"X-Auth-Token": config.football_api.token}


def get_players_by_league(db: Session, league_code: str, team_name: str) -> List[Dict[str, Any]]:
    competition = db.query(CompetitionModel).filter(CompetitionModel.code == league_code).first()
    teams = competition and competition.teams or []
    if team_name and teams:
        teams = list(filter(lambda t: t.name.lower() == team_name.lower(), competition.teams))
    return [player for team in teams for player in team.players] if competition else []


def get_team(db: Session, name: str) -> Dict[str, Any]:
    team = db.query(TeamModel).filter(TeamModel.name == name).first()
    return team or {}


def get_players_by_team(db: Session, team_id: int) -> Dict[str, Any]:
    team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    return [player for player in team.players] if team else []
