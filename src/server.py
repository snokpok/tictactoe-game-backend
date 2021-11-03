from typing import List, Optional, Union
import uuid
from fastapi import FastAPI
from psycopg2 import pool
from fastapi.exceptions import HTTPException
from starlette.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware

from db import db_api, cdb_dsn
from pydantic import BaseModel
from utils import utils_api

def run_app(mode: str) -> FastAPI:
    app = FastAPI(debug=(mode == "dev"))
    allowed_origins = ["http://0.0.0.0:3000/", "http://localhost:3000/", "https://vincent-tictactoe-game.netlify.app/"]

    app.add_middleware(
        CORSMiddleware, 
        allow_origins=allowed_origins, 
        allow_credentials=True, 
        allow_methods=["*"], 
        allow_headers=["*"]
    )

    cdb_pool = pool.SimpleConnectionPool(1, 20, dsn=cdb_dsn)

    @app.get("/games")
    async def get_all_games():
        conn = cdb_pool.getconn()
        try:
            records = db_api.get_all_from_table(conn, "games")
        except Exception as e:
            raise HTTPException(status_code=400, detail=e)
        cdb_pool.putconn(conn)
        return records

    @app.get("/moves")
    async def get_all_moves():
        conn = cdb_pool.getconn()
        try:
            records = db_api.get_all_from_table(conn, "moves")
        except Exception as e:
            raise HTTPException(status_code=400, detail=e)
        cdb_pool.putconn(conn)
        return records



    @app.get("/game/{id}")
    async def get_one(id: str):
        try:
            uuid.UUID(id)
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid id (not a UUID)")
        conn = cdb_pool.getconn()
        record = db_api.get_one_from_table(conn, "games", id)
        cdb_pool.putconn(conn)
        return record

    class GameCreateBody(BaseModel):
        players: List[str]
    @app.post("/game")
    async def create_game(body: GameCreateBody):
        # create game in its own session
        conn = cdb_pool.getconn()
        game = db_api.create_game(conn, body.players)
        cdb_pool.putconn(conn)
        return game.return_serialized()

    class MoveBody(BaseModel):
        move_no: int
        player: str
        x: int
        y: int
    @app.post("/game/{game_id}/move")
    async def play_move(game_id: str, body: MoveBody):
        # adding the moves into the session
        conn = cdb_pool.getconn(key=game_id)
        move = db_api.create_move(
            conn, 
            game_id, 
            body.player,
            body.move_no,
            body.x, body.y
        )
        return move.return_serialized()

    class UpdateWinnerBody(BaseModel):
        winner: Union[str, None]
    @app.put("/game/{game_id}")
    async def update_winner(game_id: str, body: UpdateWinnerBody):
        # closing it here because game's done
        conn = cdb_pool.getconn(key=game_id)
        game_updated = db_api.update_winner(conn, body.winner, game_id)
        cdb_pool.putconn(conn)
        return game_updated.return_serialized()

    @app.post("/resource/{tablename}/backup")
    async def backupTable(tablename: str, format: Optional[str] = "csv"):
        '''format can be csv'''
        if format == "csv":
            conn = cdb_pool.getconn()
            path = None
            try:
                path = utils_api.parse_table_csv(conn, tablename)
            except Exception as e:
                raise HTTPException(status_code=400, detail=e)
            cdb_pool.putconn(conn)
            return {
                "msg": "success",
                "path": path,
            }
        else: raise HTTPException(status_code=400, detail="Format unsupported")

    @app.get("/resource/{tablename}")
    async def get_data(tablename: str, format: str = "csv"):
        filepath = f"files/{tablename}.{format}"
        try:
            open(file=filepath, mode="r")
        except Exception as e:
            raise HTTPException(status_code=400, detail=e.args[1])
        return FileResponse(
            filepath,
            headers={
                "Cache-Control": "no-store",
            }
        )

    return app
