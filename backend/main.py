from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import run_sqlite_migrations
from games import games_router
from player import player_router

app = FastAPI()

origins = [
    '*',

    # If this becomes a problem we can restrict it to the actual domains
    # "http://localhost:5173",
    # "https://p-ranking.com",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    run_sqlite_migrations.main()

app.include_router(player_router.router)
app.include_router(games_router.router)
