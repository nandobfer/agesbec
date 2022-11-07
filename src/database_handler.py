from burgos.mysql_handler import Mysql
from datetime import datetime
import pypyodbc
import json

config = json.load(open('config.json'))
sql_server_config = config['databases']['collect_acessos']

class SqlServer():
    def __init__(self, table:str) -> None:
        self.DRIVER_NAME = '{ODBC Driver 17 for SQL Server}'
        self.SERVER_NAME = config['databases'][f'collect_{table}']['host']
        self.DATABASE_NAME = config['databases'][f'collect_{table}']['database']
        self.USER_NAME = config['databases'][f'collect_{table}']['user']
        self.PASSWORD = config['databases'][f'collect_{table}']['password']

        self.connection_string = f"""
            DRIVER={self.DRIVER_NAME};
            SERVER={self.SERVER_NAME};
            DATABASE={self.DATABASE_NAME};
            Trust_Connection=yes;
            UID={self.USER_NAME};
            PWD={self.PASSWORD};
            TrustServerCertificate=yes;
        """

    def connect(self):
        self.connection = pypyodbc.connect(self.connection_string)
        
        
    def run(self, sql):
        cursor = self.connection.cursor()
        cursor.execute(sql)
        data = cursor.fetchall()
        return data
    
    def query(self, query_str):
        cursor = self.connection.cursor()
        cursor.execute(query_str)
        return {'results':
                [dict(zip([column[0] for column in cursor.description], row))
                for row in cursor.fetchall()]}
        
class Database():
    def __init__(self, table:str):
        self.collect = SqlServer(table)
        self.processed = Mysql(auth=config['databases'][f'processed_{table}'], login_table=None)
        
    def isUp(self):
        now = datetime.now()
        sql = f"UPDATE acticity SET lastping = '{now}';"
        self.processed.run(sql)

    # Encryption

