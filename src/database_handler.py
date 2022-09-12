from burgos.mysql_handler import Mysql

class Database():
    def __init__(self):
        self.collect = Mysql()
        self.processed = Mysql()



