from typing import Any, Dict

from starlette import status
from starlette.responses import JSONResponse
from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session

from utils.depends import get_db
from utils.constants import ERROR_404
import controller.import_controller as import_controller


router = APIRouter()


@router.get("/api/v1/importLeague/{leagueCode}")
def import_league(leagueCode: str = Path(example="PD"), db: Session = Depends(get_db)) -> Dict[str, Any]:
    result = import_controller.import_league(db, leagueCode)
    if not result:
        return JSONResponse(content=ERROR_404, status_code=status.HTTP_404_NOT_FOUND)
    return result
