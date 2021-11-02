from dotenv import load_dotenv
import os

from dotenv.main import find_dotenv

load_dotenv(find_dotenv())


class DbConfigs:
    sslcertpath = f'{os.getenv("HOME")}/.postgresql/root.crt'
    user = os.getenv("CDB_USER")
    pwd = os.getenv("CDB_PWD")
    host = os.getenv("CDB_HOST")
    port = os.getenv("CDB_PORT")
    db = os.getenv("CDB_DB")
    cluster_name = os.getenv("CDB_CLUSTER_NAME")

    def __repr__(self) -> str:
        return f"""DbConfigs<
                user={self.user}, 
                pwd={self.pwd} 
                host={self.host} 
                port={self.port} 
                db={self.db} 
                clustername={self.cluster_name}
                sslcertpath={self.sslcertpath}
            >"""

DEBUG_MODE = True