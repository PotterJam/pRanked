from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.staticfiles import StaticFiles

import auth
import run_sqlite_migrations
from games import games_router
from player import player_router

app = FastAPI()
frontend = FastAPI()
api = FastAPI()

# If this becomes a problem we can restrict it to the actual domains
origins = [
    '*',
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


class SPAStaticFiles(StaticFiles):
    async def get_response(self, path: str, scope):
        try:
            return await super().get_response(path, scope)
        except (HTTPException, StarletteHTTPException) as ex:
            if ex.status_code == 404:
                return await super().get_response("index.html", scope)
            else:
                raise ex


frontend.mount("/", SPAStaticFiles(directory="/code/frontend/dist/", html=True), name="spa-static-files")

app.mount('/api', app=api)
app.mount('/', app=frontend)

api.include_router(player_router.router)
api.include_router(games_router.router)
api.include_router(auth.router)
