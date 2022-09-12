from burgos.mysql_handler import Mysql
import pypyodbc as sqlServer
import json

config = json.load(open('config.json'))
sql_server_config = config['databases']['collect_acessos']

class Database():
    def __init__(self):
        self.collect = sqlServer.connect(connection_string)
        self.processed = Mysql()


DRIVER_NAME = '{ODBC Driver 18 for SQL Server}'
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
    Encrypt=no
"""

