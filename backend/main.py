from fastapi import FastAPI

from player import player_router

app = FastAPI()
app.include_router(player_router.router)
