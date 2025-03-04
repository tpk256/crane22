from enum import Enum
from typing import Optional

from pydantic import BaseModel


class State(Enum):
    WAIT_START = 0
    IN_PROGRESS = 1
    COMPLETED = 2


class Place(BaseModel):
    id: int
    name: str
    poss: tuple[float, float]
    height: float
    width: float
    color: str


class Zone(BaseModel):
    id: int
    poss: tuple[float, float]
    height: float
    width: float
    name: str
    color: str
    places: list[Place]


class BaseTask(BaseModel):
    from_id: int
    to_id: int
    count: int
    comment: Optional[str] = ""


class Task(BaseTask):
    id: int
    state: State
    creation_date: str
    start_date: str
    end_date: str

