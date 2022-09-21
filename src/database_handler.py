from burgos.mysql_handler import Mysql
import pypyodbc
import json

config = json.load(open('config.json'))
sql_server_config = config['databases']['collect_acessos']

class SqlServer():
    def __init__(self) -> None:
        self.connection = pypyodbc.connect(connection_string)
        
    def run(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        return data
class Database():
    def __init__(self):
        self.collect = SqlServer(connection_string)
        self.processed = Mysql(auth=config['databases']['processed_acessos'], login_table=None)


DRIVER_NAME = '{ODBC Driver 17 for SQL Server}'
SERVER_NAME = sql_server_config['host']
DATABASE_NAME = sql_server_config['database']
USER_NAME = sql_server_config['user']
PASSWORD = sql_server_config['password']

connection_string = f"""
    DRIVER={DRIVER_NAME};
    SERVER={SERVER_NAME};
    DATABASE={DATABASE_NAME};
    Trust_Connection=yes;
    UID={USER_NAME};
    PWD={PASSWORD};
    TrustServerCertificate=yes;
"""
    # Encryption

