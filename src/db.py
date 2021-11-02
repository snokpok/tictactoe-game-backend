from abc import abstractmethod
from typing import Any, Dict, List, Union, Tuple, overload
from configs import DbConfigs
from psycopg2 import extensions
import uuid

cdb_dsn = f"postgres://{DbConfigs.user}:{DbConfigs.pwd}@{DbConfigs.host}:{DbConfigs.port}/{DbConfigs.cluster_name}.{DbConfigs.db}?sslmode=verify-full&sslrootcert={DbConfigs.sslcertpath}"

class BaseDBO(object):
    __tablename__: str
    def __init__(self, tablename: str) -> None:
        self.__tablename__ = tablename

    def __getitem__(self, key):
        this_dict = self.return_serialized()
        return this_dict[key]

    @abstractmethod
    def return_serialized(self) -> Dict[str, Any]:
        raise NotImplementedError()

class Game(BaseDBO):
    id: str
    players: List[str]
    winner: Union[str, None]

    def __init__(self, db_res: Tuple) -> None:
        super().__init__(tablename="games")
        self.id = db_res[0]
        self.players = db_res[1]
        self.winner = db_res[2]
    
    def return_serialized(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "players": self.players,
            "winner": self.winner
        }

class Move(BaseDBO):
    game: str
    number: int
    coord: List[str]
    player: str
    def __init__(self, db_res: Tuple) -> None:
        super().__init__(tablename="moves")
        self.game = db_res[0]
        self.number = db_res[1]
        self.coord = db_res[2]
        self.player = db_res[3]

    def return_serialized(self) -> Dict[str, Any]:
        return {
            "game": self.game,
            "number": self.number,
            "coord": self.coord,
            "player": self.player,
        }

tablenames = ["games", "moves"]

class DatabaseAPI:
    
    def __fetch_batches(self, cur: extensions.cursor, batch_size: int, ClassType: BaseDBO) -> List[BaseDBO]:
        '''
        Fetch batches from a postgres cursor based on batch_size
        Use this after cursor.execute() to fetch the data
        '''
        records: List[ClassType] = []
        batch_cursor_res = None
        while batch_cursor_res == None or (isinstance(batch_cursor_res, list) and len(batch_cursor_res) != 0):
            batch_cursor_res = cur.fetchmany(batch_size)
            for record in batch_cursor_res:
                record_object = ClassType(record)
                records.append(record_object)
        return records

    def __fetch_parse(self, cur: extensions.cursor, ClassType: BaseDBO) -> BaseDBO:
        res = cur.fetchone()
        if not res: return None
        else: return ClassType(res)

    def get_all_from_table(self, conn: extensions.connection, tablename: str) -> List[BaseDBO]:
        GET_ALL_SQL = f'''SELECT * FROM {tablename};'''
        cur = conn.cursor()
        cur.execute(GET_ALL_SQL)
        batch_size = 2
        res = []
        if tablename == "games":
            res = self.__fetch_batches(cur, batch_size, Game)
        elif tablename == "moves":
            res = self.__fetch_batches(cur, batch_size, Move)
        cur.close()
        conn.close()
        return res

    def get_one_from_table(self, conn: extensions.connection, tablename: str, id: str) -> BaseDBO:
        cur = conn.cursor()
        GET_ONE_SQL = f'''SELECT * FROM {tablename} WHERE id = %s'''
        cur.execute(GET_ONE_SQL, [id])
        res = None
        if tablename == "games":
            res = self.__fetch_parse(cur, Game)
        cur.close()
        conn.close()
        return res



    def create_game(self, conn: extensions.connection, players: List[str]) -> Game:
        cur = conn.cursor()
        INSERT_GAME_SQL = '''INSERT INTO games (players) VALUES (%s) RETURNING *;'''
        cur.execute(INSERT_GAME_SQL, [players])
        res = cur.fetchone()
        game_result = Game(res)  
        conn.commit()
        cur.close()
        conn.close()
        return game_result

    def create_move(
        self, 
        conn: extensions.connection,
        game_id: str,
        player: str, 
        move_no: int,
        x: int, y: int
    ) -> Move:
        cur = conn.cursor()
        INSERT_MOVE_SQL = '''
            INSERT INTO moves (game, number, coord, player) VALUES (%s, %s, %s, %s) RETURNING *;
        '''
        cur.execute(INSERT_MOVE_SQL, [game_id, move_no, [x,y], player])
        res = cur.fetchone()
        move_data = Move(res)
        cur.close()
        return move_data

    def update_winner(self, conn: extensions.connection, winner: str, game_id: str) -> Game:
        UPDATE_GAME_WINNER_SQL = '''
            UPDATE games
            SET winner = %(winner)s
            WHERE id = %(id)s
            RETURNING *;
        '''
        cur = conn.cursor()
        cur.execute(UPDATE_GAME_WINNER_SQL, {'winner': winner, 'id': game_id})
        res = cur.fetchone()
        updated_game = Game(res)
        conn.commit()
        cur.close()
        conn.close()
        return updated_game

db_api = DatabaseAPI()