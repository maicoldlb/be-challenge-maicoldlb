from typing import List, Optional

from pydantic import BaseModel


def to_camel(string: str) -> str:
    return "".join(word.capitalize() for word in string.split("_"))


class PlayerSchema(BaseModel):

    id: int
    name: str
    position: Optional[str]
    date_of_birth: Optional[str]
    country_of_birth: Optional[str]
    nationality: Optional[str]
    team_id: int

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "Id": 2294,
                "Name": "Álex Berenguer",
                "Position": "Midfield",
                "DateOfBirth": "1995-07-04",
                "CountryOfBirth": "Spain",
                "Nationality": "Spain",
                "TeamId": 77,
            },
        }


class TeamSchema(BaseModel):

    id: int
    name: str
    tla: str
    short_name: str
    area_name: str
    email: str
    competition_id: int
    players: List[PlayerSchema] = []

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
        schema_extra = {
            "example": {
                "Id": 77,
                "Name": "Athletic Club",
                "Tla": "ATH",
                "ShortName": "Athletic",
                "AreaName": "Spain",
                "Email": "prensa@athletic-club.net",
                "CompetitionId": 2014,
                "Players": [
                    {
                        "Id": 2294,
                        "Name": "Álex Berenguer",
                        "Position": "Midfield",
                        "DateOfBirth": "1995-07-04",
                        "CountryOfBirth": "Spain",
                        "Nationality": "Spain",
                        "TeamId": 77,
                    }
                ],
            },
        }


class CompetitionSchema(BaseModel):

    id: int
    code: str
    name: str
    area_name: str
    teams: List[TeamSchema] = []

    class Config:
        orm_mode = True
        alias_generator = to_camel
        allow_population_by_field_name = True
