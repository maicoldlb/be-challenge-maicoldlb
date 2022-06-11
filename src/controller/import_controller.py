import logging
from typing import Any, Dict

import requests
from sqlalchemy import true
from sqlalchemy.orm import Session

from config import config
from db.models import CompetitionModel, TeamModel, PlayerModel


logger = logging.getLogger("uvicorn.error")


HEADERS = {"X-Auth-Token": config.football_api.token}
IMPORT_PLAYER = False
IMPORT_TEAM = False


def import_league(db: Session, league_code: str) -> Dict[str, Any]:
    global IMPORT_PLAYER
    global IMPORT_TEAM

    competition = db.query(CompetitionModel).filter(CompetitionModel.code == league_code).first()
    if competition is None:
        url = f"{config.football_api.url}/v2/competitions/{league_code}/"
        payload = {}

        response = requests.get(url, headers=HEADERS, data=payload)
        competition = response.json()
        logger.info(f"import_league {league_code}: {response.ok}")
        if response.ok:

            competition_id = competition.get("id")
            competition_data = {
                "id": competition_id,
                "name": competition.get("name"),
                "code": competition.get("code"),
                "area_name": competition.get("area", {}).get("name"),
            }
            if db.query(CompetitionModel).filter(CompetitionModel.id == competition_id).first() is None:
                db_competition = CompetitionModel(**competition_data)
                db.add(db_competition)
                db.commit()
                db.refresh(db_competition)
    else:
        competition_id = competition.id

    teams = get_teams(league_code)
    IMPORT_TEAM = True
    for team in teams:
        team_id = team.get("id")
        squad = import_team(db, team_id, competition_id)
        IMPORT_PLAYER = True
        for member in squad:
            member_id = member.get("id")
            role = member.get("role")
            if role != "PLAYER":
                continue
            import_player(db, member_id, team_id)

    return competition


def get_teams(league_code):
    url = f"{config.football_api.url}/v2/competitions/{league_code}/teams"
    response = requests.get(url, headers=HEADERS)
    teams_by_competition = response.json()
    teams = list()
    logger.info(f"get_teams {league_code}: {response.ok}")
    if response.ok:
        teams = teams_by_competition.get("teams")
    return teams


def import_team(db: Session, team_id, competition_id):
    global IMPORT_TEAM
    global IMPORT_PLAYER

    squad = list()

    if not IMPORT_TEAM:
        return squad

    team = db.query(TeamModel).filter(TeamModel.id == team_id).first()
    url = f"{config.football_api.url}/v2/teams/{team_id}"
    response = requests.get(url, headers=HEADERS)

    logger.info(f"import_team {team_id}: {response.ok}")

    if response.ok:
        squad_by_team = response.json()
        squad = squad_by_team.get("squad")

        if team is None:
            team_data = {
                "id": team_id,
                "name": squad_by_team.get("name"),
                "tla": squad_by_team.get("tla"),
                "short_name": squad_by_team.get("shortName"),
                "area_name": squad_by_team.get("area", {}).get("name"),
                "email": squad_by_team.get("email"),
                "competition_id": competition_id,
            }
            db_team = TeamModel(**team_data)
            db.add(db_team)
            db.commit()
            db.refresh(db_team)
        else:
            logger.info(f"squad_api: {len(squad)}, squad_db: {len(team.players)}")
    else:
        IMPORT_TEAM = False
        IMPORT_PLAYER = False

    return squad


def import_player(db: Session, player_id, team_id):
    global IMPORT_PLAYER
    global IMPORT_TEAM

    player = db.query(PlayerModel).filter(PlayerModel.id == player_id).first()

    if IMPORT_PLAYER and player is None:
        url = f"{config.football_api.url}/v2/players/{player_id}"
        response = requests.get(url, headers=HEADERS)
        player = response.json()
        logger.info(f"import_player {player_id}: {response.ok}")
        if response.ok:
            player_data = {
                "id": player_id,
                "name": player.get("name"),
                "position": player.get("position"),
                "date_of_birth": player.get("dateOfBirth"),
                "country_of_birth": player.get("countryOfBirth"),
                "nationality": player.get("nationality"),
                "team_id": team_id,
            }
            db_player = PlayerModel(**player_data)
            db.add(db_player)
            db.commit()
            db.refresh(db_player)
        else:
            IMPORT_PLAYER = False
            IMPORT_TEAM = False
