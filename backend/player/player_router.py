import sqlite3

from fastapi import APIRouter, HTTPException

from ranking.consts import rating_deviation_default, rating_default
from utility import sqlite_db

router = APIRouter(prefix='/player')


@router.get("/{username}")
async def get_player(username: str):
    with sqlite_db.connection() as con:
        result = con.execute("SELECT username, current_rating, current_rating_deviation FROM players WHERE username = ?", [username])
        row = result.fetchone()
        if row is None:
            raise HTTPException(status_code=404, detail="Player not found")
        return {
            "username": row[0],
            "rating": row[1],
            "rating_deviation": rating_deviation_default,
        }


@router.put("/{username}")
async def add_player(username: str):
    with sqlite_db.connection() as con:
        try:
            con.execute("INSERT INTO players (username) VALUES (?)", [username])
            return {
                "username": username,
                "rating": rating_default,
                "rating_deviation": rating_deviation_default,
            }
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=409, detail="Player already exists")
