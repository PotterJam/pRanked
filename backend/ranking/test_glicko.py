import unittest

import glicko
from ranking.outcome import Outcome
from ranking.rating import Rating


class GlickoCalculatorTests(unittest.TestCase):
    def test_winning_against_similar_rating_should_increase_rating(self):
        initial_rating = Rating(1500, 350)
        games = [(Outcome.WIN, Rating(1500, 350))]

        rating = glicko.Calculator().score_games(initial_rating, games)
        self.assertGreater(rating.value, initial_rating.value)

    def test_losing_against_similar_rating_should_decrease_rating(self):
        initial_rating = Rating(1500, 350)
        games = [(Outcome.LOSS, Rating(1500, 350))]

        rating = glicko.Calculator().score_games(initial_rating, games)
        self.assertLess(rating.value, initial_rating.value)

    def test_winning_against_high_volatility_with_same_rating_should_increase_rating_less(self):
        initial_rating = Rating(1500, 350)

        # first calculate a normal volatility outcome
        games = [(Outcome.WIN, Rating(1500, 350))]
        low_volatility_rating = glicko.Calculator().score_games(initial_rating, games)

        # then a high volatility outcome
        games = [(Outcome.WIN, Rating(1500, 1000))]
        high_volatility_rating = glicko.Calculator().score_games(initial_rating, games)

        self.assertGreater(low_volatility_rating.value, high_volatility_rating.value)

    def test_losing_against_high_volatility_with_same_rating_should_decrease_rating_more(self):
        initial_rating = Rating(1500, 350)

        # first calculate a normal volatility outcome
        games = [(Outcome.LOSS, Rating(1500, 350))]
        low_volatility_rating = glicko.Calculator().score_games(initial_rating, games)

        # then a high volatility outcome
        games = [(Outcome.LOSS, Rating(1500, 1000))]
        high_volatility_rating = glicko.Calculator().score_games(initial_rating, games)

        self.assertLess(low_volatility_rating.value, high_volatility_rating.value)

    def test_losing_against_high_volatility_lower_rating_should_decrease_rating_more(self):
        initial_rating = Rating(1500, 350)

        # first calculate a normal volatility outcome
        games = [(Outcome.LOSS, Rating(1000, 350))]
        low_volatility_rating = glicko.Calculator().score_games(initial_rating, games)

        # then a high volatility outcome
        games = [(Outcome.LOSS, Rating(1000, 1000))]
        high_volatility_rating = glicko.Calculator().score_games(initial_rating, games)

        self.assertLess(low_volatility_rating.value, high_volatility_rating.value)

    def test_draw_against_same_rating_does_not_change_rating(self):
        initial_rating = Rating(1500, 350)
        games = [(Outcome.DRAW, Rating(1500, 350))]

        rating = glicko.Calculator().score_games(initial_rating, games)
        self.assertEqual(rating.value, initial_rating.value)

    def test_draw_against_higher_rating_increases_rating(self):
        initial_rating = Rating(1500, 350)
        games = [(Outcome.DRAW, Rating(2000, 56))]

        rating = glicko.Calculator().score_games(initial_rating, games)
        self.assertGreater(rating.value, initial_rating.value)

    def test_consistency_over_multiple_periods_reduces_deviation(self):
        initial_rating = Rating(1500, 350)

        games = [
            (Outcome.LOSS, Rating(1500, 56)),
            (Outcome.WIN, Rating(1500, 74)),
            (Outcome.LOSS, Rating(1500, 45)),
            (Outcome.WIN, Rating(1500, 56)),
        ]

        rating = glicko.Calculator().score_games(initial_rating, games)
        self.assertLess(rating.deviation, initial_rating.deviation)

        rating2 = glicko.Calculator().score_games(rating, games)
        self.assertLess(rating2.deviation, rating.deviation)

        rating3 = glicko.Calculator().score_games(rating2, games)
        self.assertLess(rating3.deviation, rating2.deviation)

    def test_volatile_outcomes_decreases_deviation_less(self):
        initial_rating = Rating(1500, 350)

        games = [
            (Outcome.LOSS, Rating(1500, 56)),
            (Outcome.WIN, Rating(1500, 74)),
            (Outcome.LOSS, Rating(1500, 45)),
            (Outcome.WIN, Rating(1500, 56)),
         ]

        first_period_rating = glicko.Calculator().score_games(initial_rating, games)

        volatile_games = [
            (Outcome.WIN, Rating(2500, 35)),
            (Outcome.WIN, Rating(2500, 37)),
            (Outcome.WIN, Rating(1900, 35)),
        ]

        rating_after_volatile = glicko.Calculator().score_games(first_period_rating, volatile_games)

        non_volatile_deviation_difference = initial_rating.deviation - first_period_rating.deviation
        volatile_deviation_difference = first_period_rating.deviation - rating_after_volatile.deviation
        self.assertLess(volatile_deviation_difference, non_volatile_deviation_difference)

    def test_missing_periods_with_volatile_games_increases_deviation(self):
        initial_rating = Rating(1000, 100)

        games = [
            (Outcome.LOSS, Rating(2500, 56)),
            (Outcome.WIN, Rating(2500, 74)),
            (Outcome.LOSS, Rating(2500, 45)),
            (Outcome.WIN, Rating(2500, 56)),
        ]

        rating = glicko.Calculator().score_games(initial_rating, games, periods_missed=10)
        self.assertGreater(rating.deviation, initial_rating.deviation)


if __name__ == '__main__':
    unittest.main()
