from dataclasses import dataclass
from enum import Enum


class Outcome(float, Enum):
    WIN = 1.
    LOSS = 0.
    DRAW = 0.5


@dataclass
class Rating:
    value: int
    deviation: int


@dataclass
class Player:
    name: str
    rating: Rating
