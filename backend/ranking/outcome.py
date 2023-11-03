from enum import Enum


class Outcome(float, Enum):
    WIN = 1.
    LOSS = 0.
    DRAW = 0.5
