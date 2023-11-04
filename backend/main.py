from fastapi import FastAPI

from games import games_router
from player import player_router

app = FastAPI()
app.include_router(player_router.router)
app.include_router(games_router.router)
