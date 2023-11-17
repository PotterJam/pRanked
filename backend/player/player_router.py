import sqlite3
import re
from datetime import timedelta, date, datetime

from fastapi import APIRouter, HTTPException, Request

from auth import is_authenticated
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


@router.put("/{username_request}")
async def add_player(username_request: str, request: Request):
    if not is_authenticated(request):
        raise HTTPException(status_code=404)

    # Trim whitespace
    username = username_request.strip()

    if len(username) < 2:
        raise HTTPException(status_code=400, detail="Username must be at least 2 characters long")

    # Make sure the username is alphanumeric with at most one space in between words
    valid_username_pattern = r"^[a-zA-Z0-9]+( [a-zA-Z0-9]+)?$"
    if not re.match(valid_username_pattern, username):
        raise HTTPException(status_code=400, detail="Username must be alphanumeric with at most one space in between words")

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


# This is disgusting, but I was lazy and let copilot write most of it
@router.get("/rating-history")
async def get_all_players_rating_history():
    # Get the rating history for all the players in the form
    #
    # export interface RatingHistoryResponse {
    #     player_name: string;
    #     rating_history: {date_played: string, rating: number}[];
    # }
    #
    # Such that the rating history is sorted by the date played, with the oldest game first
    # and the date is only the date part of the timestamp
    # and for each player, the rating history must include every date between the first game played and the last game played of everyone, with a rating of None for dates where the player didn't play
    # also include the latest game played at the end of their rating history

    with sqlite_db.connection() as con:
        players_result = con.execute("SELECT player_id, username, current_rating, last_game_played FROM players")
        player_rows = players_result.fetchall()
        if player_rows is None:
            raise HTTPException(status_code=404, detail="Players not found")

        players = {row[0]: row[1] for row in player_rows}

        # fetch games so I can form the history
        games_result = con.execute("SELECT winner_id, winner_rating, loser_id, loser_rating, date_played FROM games")
        games_rows = games_result.fetchall()
        if games_rows is None:
            raise HTTPException(status_code=404, detail="Games not found")

        # group player rating history by player_id
        player_rating_history = {}

        for row in games_rows:
            winner_id = row[0]
            winner_rating = row[1]
            loser_id = row[2]
            loser_rating = row[3]
            date_played = datetime.fromisoformat(row[4]).date()

            winner_name = players[winner_id]
            loser_name = players[loser_id]

            build_rating_history(player_rating_history, winner_name, winner_rating, date_played)
            build_rating_history(player_rating_history, loser_name, loser_rating, date_played)

        # get the oldest date played
        oldest_date_played = min([datetime.fromisoformat(row[4]).date() for row in games_rows])

        for player_name, rating_history in player_rating_history.items():
            # for every day from the oldest date till todays date, fill in the missing dates with a rating of None
            rating_history_dates_played = map(lambda x: x["date_played"], rating_history)

            current_date = oldest_date_played
            while current_date != date.today() + timedelta(days=1):
                if current_date not in rating_history_dates_played:
                    rating_history.append({
                        "date_played": current_date,
                        "rating": None
                    })
                current_date = current_date + timedelta(days=1)

            # sort the rating history by date played
            rating_history.sort(key=lambda x: x["date_played"])

        # I then need to consolidate each day to only show the data point with their last ranking for that day
        for player_name, rating_history in player_rating_history.items():
            consolidated_rating_history = []
            for rating_history_entry in rating_history:
                if len(consolidated_rating_history) == 0:
                    consolidated_rating_history.append(rating_history_entry)
                else:
                    last_rating_history_entry = consolidated_rating_history[-1]
                    if last_rating_history_entry["date_played"] == rating_history_entry["date_played"]:
                        if rating_history_entry["rating"] is not None:
                            consolidated_rating_history[-1] = rating_history_entry
                    else:
                        consolidated_rating_history.append(rating_history_entry)
            player_rating_history[player_name] = consolidated_rating_history

        # and for the last day, it should always be their current rating
        for player_name, rating_history in player_rating_history.items():
            rating_history[-1]["rating"] = player_rows[[row[1] for row in player_rows].index(player_name)][2]

        # transform dictionary into a flat list of player name and rating history
        player_rating_history = [{"player_name": player_name, "rating_history": rating_history} for player_name, rating_history in player_rating_history.items()]
        player_rating_history.sort(key=lambda x: x["rating_history"][-1]["rating"], reverse=True)

        return player_rating_history


def build_rating_history(rating_history, player_name, rating, date_played):
    if player_name not in rating_history:
        rating_history[player_name] = []

    rating_history[player_name].append({
        "date_played": date_played,
        "rating": rating
    })

