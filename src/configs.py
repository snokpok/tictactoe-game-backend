from logging import DEBUG
from dotenv import dotenv_values
from dotenv import dotenv_values, load_dotenv
import os

from dotenv.main import find_dotenv

load_dotenv(find_dotenv())


class DbConfigs:
    sslcertpath = "/Users/vmvu/.postgresql/root.crt"
    user = 'vincent'
    pwd = "Fkusam2212cdb"
    host = "free-tier4.aws-us-west-2.cockroachlabs.cloud"
    port = 26257
    db = "defaultdb"
    cluster_name = os.environ.get("CDB_CLUSTER_NAME")

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