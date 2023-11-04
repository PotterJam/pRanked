from dataclasses import dataclass

from ranking.rating import Rating


@dataclass
class Player:
    id: int
    username: str
    rating: Rating
