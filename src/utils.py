from psycopg2 import extensions
from enum import Enum
import csv

from meta import table_metas
from db import db_api

class OptionDownload(Enum):
    EXCEL: str
    CSV: str

class UtilsAPI:
    def parse_table_csv(self, conn: extensions.connection, tablename: str) -> str:
        filepath = f"files/{tablename}.csv"
        if tablename not in [*table_metas.keys()]:
            raise ValueError("Invalid table name")
        with open(filepath, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            # writing the header
            writer.writerow(table_metas[tablename]["header"])
            for record in db_api.get_all_from_table(conn, tablename):
                writer.writerow([record[header] for header in table_metas[tablename]["header"]])
        return filepath

utils_api = UtilsAPI()