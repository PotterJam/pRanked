from dataclasses import dataclass

from ranking.rating import Rating


@dataclass
class Player:
    username: str
    rating: Rating
