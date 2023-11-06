from datetime import datetime

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from ranking import glicko
from ranking.outcome import Outcome
from ranking.rating import Rating
from utility import sqlite_db

router = APIRouter(prefix='/games')


@router.get("/")
async def get_games():
    with sqlite_db.connection() as con:
        game_result = con.execute("SELECT game_id, draw, winner_id, winner_rating, winner_rating_gained, loser_id, loser_rating, loser_rating_lost FROM games")
        game_rows = game_result.fetchall()
        if game_rows is None:
            raise HTTPException(status_code=404, detail="Games not found")

        players_result = con.execute("SELECT player_id, username FROM players")
        player_rows = players_result.fetchall()
        if player_rows is None:
            raise HTTPException(status_code=404, detail="Players not found")

        players = {row[0]: row[1] for row in player_rows}

        def row_to_response(row):
            return {
                "game_id": row[0],
                "draw": row[1],
                "winner_id": row[2],
                "winner_username": players[row[2]],
                "winner_rating": row[3],
                "winner_rating_gained": row[4],
                "loser_id": row[5],
                "loser_username": players[row[5]],
                "loser_rating": row[6],
                "loser_rating_lost": row[7],
            }

        return [row_to_response(row) for row in game_rows]


class SubmitGameRequest(BaseModel):
    winner_id: int
    loser_id: int
    draw: bool = False


# TODO: extract this into a service so I can test it properly
@router.post("/submit")
async def submit_game(submit_game_request: SubmitGameRequest):
    with sqlite_db.connection() as con:
        # Get the winner_rating, loser_rating, winner_rating_deviation, loser_rating_deviation from the players table for both players
        winner_result = con.execute("SELECT current_rating, current_rating_deviation, last_game_played FROM players WHERE player_id = ?", [submit_game_request.winner_id])
        loser_result = con.execute("SELECT current_rating, current_rating_deviation, last_game_played FROM players WHERE player_id = ?", [submit_game_request.loser_id])
        winner_rating, winner_rating_deviation, winner_last_played = winner_result.fetchone()
        loser_rating, loser_rating_deviation, loser_last_played = loser_result.fetchone()

        # Make sure the winner and loser exist
        if winner_rating is None or winner_rating_deviation is None:
            raise HTTPException(status_code=404, detail="Player with that winner id doesn't exist")
        if loser_rating is None or loser_rating_deviation is None:
            raise HTTPException(status_code=404, detail="Player with that loser id doesn't exist")

        # TODO: another thing to extract that'll be nice in a player service
        # Calculate number of months since the winner and loser last played a game
        def get_months_since_playing(last_played: str | None):
            if last_played is None:
                # Doesn't matter if they haven't played a game yet
                return 0

            delta = relativedelta(datetime.now(), datetime.fromisoformat(last_played))
            return delta.months + (delta.years * 12)

        winner_months_away = get_months_since_playing(winner_last_played)
        loser_months_away = get_months_since_playing(loser_last_played)

        # Update the winner and loser ratings using glicko
        new_winner_rating = glicko.Calculator().score_games(
            Rating(winner_rating, winner_rating_deviation),
            [(Outcome.WIN, Rating(loser_rating, loser_rating_deviation))],
            months_since_playing=winner_months_away)
        new_loser_rating = glicko.Calculator().score_games(
            Rating(loser_rating, loser_rating_deviation),
            [(Outcome.LOSS, Rating(winner_rating, winner_rating_deviation))],
            months_since_playing=loser_months_away)

        # Update the winner and loser ratings in the players table
        con.execute("UPDATE players SET current_rating = ?, current_rating_deviation = ?, last_game_played = CURRENT_TIMESTAMP WHERE player_id = ?",
                    [new_winner_rating.value, new_winner_rating.deviation, submit_game_request.winner_id])
        con.execute("UPDATE players SET current_rating = ?, current_rating_deviation = ?, last_game_played = CURRENT_TIMESTAMP WHERE player_id = ?",
                    [new_loser_rating.value, new_loser_rating.deviation, submit_game_request.loser_id])

        # Add the rating changes into the players_rating_history table
        con.execute(
            "INSERT INTO players_rating_history (player_id, rating, rating_deviation) VALUES (?, ?, ?)",
            [submit_game_request.winner_id, new_winner_rating.value, new_winner_rating.deviation])
        con.execute(
            "INSERT INTO players_rating_history (player_id, rating, rating_deviation) VALUES (?, ?, ?)",
            [submit_game_request.loser_id, new_loser_rating.value, new_loser_rating.deviation])

        winner_rating_gained = new_winner_rating.value - winner_rating
        loser_rating_lost = loser_rating - new_loser_rating.value

        # Get id of inserted game
        game_insert_result = con.execute(
            "INSERT INTO games (draw, winner_id, winner_rating, winner_rating_gained, winner_rating_deviation, loser_id, loser_rating, loser_rating_lost, loser_rating_deviation) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            [
                submit_game_request.draw,
                submit_game_request.winner_id,
                winner_rating,
                winner_rating_gained,
                winner_rating_deviation,
                submit_game_request.loser_id,
                loser_rating,
                loser_rating_lost,
                loser_rating_deviation
            ])

        game_id = game_insert_result.lastrowid

        return {
            "old_winner_rating": winner_rating,
            "old_loser_rating": loser_rating,
            "new_winner_rating": new_winner_rating,
            "new_loser_rating": new_loser_rating,
            "winner_rating_gained": winner_rating_gained,
            "loser_rating_lost": loser_rating_lost,
            "game_id": game_id
        }
