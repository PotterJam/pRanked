from fastapi import FastAPI

from routers import player

app = FastAPI()
app.include_router(player.router)
