import math
from typing import Optional

from ranking.consts import rating_deviation_default
from ranking.outcome import Outcome
from ranking.rating import Rating


class Calculator:
    def __init__(self):
        self.C = 15.8
        self.Q = math.log(10) / 400

    # implemented from http://www.glicko.net/glicko/glicko.pdf
    def score_games(self, initial_rating: Rating, game_results_from_period: [(Outcome, Rating)], periods_missed: Optional[int] = None) -> object:
        t = 1 if periods_missed is None else periods_missed + 1
        rating_deviation_for_period = min(int(math.sqrt((initial_rating.deviation ** 2) + (self.C ** 2) * t)), rating_deviation_default)
        rating_for_period = Rating(initial_rating.value, rating_deviation_for_period)

        # Corresponds to g in the paper
        def calc_volatility(rating: Rating):
            return 1 / math.sqrt(1 + 3 * self.Q ** 2 * (rating.deviation ** 2) / math.pi ** 2)

        # Corresponds to E in the paper
        def guess_outcome(rating: Rating, opponent_rating: Rating, opponent_volatility: float):
            return 1 / (1 + 10 ** (-opponent_volatility * (rating.value - opponent_rating.value) / 400))

        difference_from_expected = 0
        d_squared_accumulator = 0
        for outcome, versus_rating in game_results_from_period:
            volatility = calc_volatility(versus_rating)
            expected_outcome = guess_outcome(rating_for_period, versus_rating, volatility)
            difference_from_expected += volatility * (outcome - expected_outcome)
            d_squared_accumulator += (volatility ** 2) * expected_outcome * (1 - expected_outcome)

        d_squared = 1 / ((self.Q ** 2) * d_squared_accumulator)
        new_rating = rating_for_period.value + (self.Q / (1 / (rating_for_period.deviation ** 2) + (1 / d_squared))) * difference_from_expected
        new_rating_deviation = math.sqrt(1 / ((1 / rating_for_period.deviation ** 2) + (1 / d_squared)))
        return Rating(new_rating, new_rating_deviation)
