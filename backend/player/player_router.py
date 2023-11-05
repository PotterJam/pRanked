import sqlite3

from fastapi import APIRouter, HTTPException

from ranking.consts import rating_deviation_default, rating_default
from utility import sqlite_db

router = APIRouter(prefix='/players')


@router.get("/")
async def get_players():
    with sqlite_db.connection() as con:
        result = con.execute("SELECT player_id, username, current_rating, current_rating_deviation FROM players")
        rows = result.fetchall()
        if rows is None:
            raise HTTPException(status_code=404, detail="Players not found")

        def get_response_from_row(row):
            return {
                "player_id": row[0],
                "username": row[1],
                "rating": row[2],
                "rating_deviation": row[3],
            }

        return [get_response_from_row(row) for row in rows]


@router.put("/{username}")
async def add_player(username: str):
    with sqlite_db.connection() as con:
        try:
            result = con.execute("INSERT INTO players (username) VALUES (?)", [username])

            rows_changed = result.rowcount
            if rows_changed != 1:
                raise HTTPException(status_code=500, detail=f"Unexpected number of rows changed when adding player. Changed {rows_changed} rows")

            return {
                "player_id": result.lastrowid,
                "username": username,
                "rating": rating_default,
                "rating_deviation": rating_deviation_default,
            }
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=409, detail="Player already exists")
