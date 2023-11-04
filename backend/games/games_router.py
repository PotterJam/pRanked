import sqlite3

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from utility import sqlite_db

router = APIRouter(prefix='/games')


@router.get("/{game_id}")
async def get_game(game_id: int):
    with sqlite_db.connection() as con:
        result = con.execute("SELECT game_id, draw, winner_id, loser_id, winner_rating, loser_rating, winner_rating_deviation, loser_rating_deviation, rating_period_id FROM games WHERE game_id = ?", [game_id])
        row = result.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Game not found")
        return {
            "game_id": row[0],
            "draw": row[1],
            "winner_id": row[2],
            "loser_id": row[3],
            "winner_rating": row[4],
            "loser_rating": row[5],
            "winner_rating_deviation": row[6],
            "loser_rating_deviation": row[7],
            "rating_period_id": row[8],
        }


class SubmitGameRequest(BaseModel):
    winner_id: int
    loser_id: int
    draw: bool = False


@router.post("/submit")
async def submit_game(submit_game_request: SubmitGameRequest):
    with sqlite_db.connection() as con:
        # Get the current rating_period_id, this will also compute the games for the previous period if needed
        rating_period_id = get_latest_or_compute_period_and_create_new_period(con)

        # Get the winner_rating, loser_rating, winner_rating_deviation, loser_rating_deviation from the players table for both players
        winner_result = con.execute("SELECT current_rating, current_rating_deviation FROM players WHERE player_id = ?", [submit_game_request.winner_id])
        loser_result = con.execute("SELECT current_rating, current_rating_deviation FROM players WHERE player_id = ?", [submit_game_request.loser_id])
        winner_rating, winner_rating_deviation = winner_result.fetchone()
        loser_rating, loser_rating_deviation = loser_result.fetchone()

        # Make sure the winner and loser exist
        if winner_rating is None or winner_rating_deviation is None:
            raise HTTPException(status_code=404, detail="Player with that winner id doesn't exist")
        if loser_rating is None or loser_rating_deviation is None:
            raise HTTPException(status_code=404, detail="Player with that loser id doesn't exist")

        # Get id of inserted game
        game_insert_result = con.execute(
            "INSERT INTO games (draw, winner_id, loser_id, winner_rating, loser_rating, winner_rating_deviation, loser_rating_deviation, rating_period_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            [submit_game_request.draw, submit_game_request.winner_id, submit_game_request.loser_id, winner_rating, loser_rating, winner_rating_deviation, loser_rating_deviation, rating_period_id])

        # Make sure only one row was inserted
        rows_changed = game_insert_result.rowcount
        if rows_changed != 1:
            raise HTTPException(status_code=500, detail=f"Unexpected number of rows changed when adding game. Changed {rows_changed} rows")

        game_id = game_insert_result.lastrowid
        return {
            "game_id": game_id
        }


def get_latest_or_compute_period_and_create_new_period(con: sqlite3.Connection):
    # Get the current rating_period_id
    rating_period_result = con.execute("SELECT MAX(rating_period_id) FROM rating_period")
    rating_period_id = rating_period_result.fetchone()[0]

    if rating_period_id is None:
        # todo: compute the new rankings for the last period
        # No rating_period_id found, so create a new rating_period
        rating_period_insert_result = con.execute("INSERT INTO rating_period DEFAULT VALUES")
        rows_changed = rating_period_insert_result.rowcount
        if rows_changed != 1:
            raise HTTPException(status_code=500, detail=f"Unexpected number of rows changed when adding rating_period. Changed {rows_changed} rows")
        rating_period_id = rating_period_insert_result.lastrowid

    return rating_period_id
