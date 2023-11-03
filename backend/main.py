from fastapi import FastAPI

from player import player

app = FastAPI()
app.include_router(player.router)
