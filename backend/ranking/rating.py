from dataclasses import dataclass


@dataclass
class Rating:
    value: int
    deviation: int
