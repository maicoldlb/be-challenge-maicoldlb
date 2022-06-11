from typing import Any, Dict, List

from starlette import status
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, Path, Query, Request
from sqlalchemy.orm import Session

from utils.constants import ERROR_404
from utils.depends import get_db
import controller.football_controller as football_controller
from db.schema import PlayerSchema, TeamSchema


router = APIRouter()


@router.get("/api/v1/players/{leagueCode}", response_model=List[PlayerSchema], response_model_by_alias=True)
def get_players_by_league(
    leagueCode: str = Path(example="PD"), teamName: str = Query(example="Athletic Club"), db: Session = Depends(get_db)
) -> Dict[str, Any]:
    result = football_controller.get_players_by_league(db, leagueCode, teamName)
    if not result:
        return JSONResponse(content=ERROR_404, status_code=status.HTTP_404_NOT_FOUND)
    return result


@router.get("/api/v1/team/{teamName}", response_model=TeamSchema, response_model_by_alias=True)
def get_team(teamName: str = Path(example="Athletic Club"), db: Session = Depends(get_db)) -> Dict[str, Any]:
    result = football_controller.get_team(db, teamName)
    if not result:
        return JSONResponse(content=ERROR_404, status_code=status.HTTP_404_NOT_FOUND)
    return result


@router.get("/api/v1/player/{teamId}", response_model=List[PlayerSchema], response_model_by_alias=True)
def get_players_by_team(teamId: int = Path(example=77), db: Session = Depends(get_db)) -> Dict[str, Any]:
    result = football_controller.get_players_by_team(db, teamId)
    if not result:
        return JSONResponse(content=ERROR_404, status_code=status.HTTP_404_NOT_FOUND)
    return result
