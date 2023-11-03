from dataclasses import dataclass

from ranking.rating import Rating


@dataclass
class Player:
    name: str
    rating: Rating
