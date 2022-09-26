from datetime import datetime
import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect_visitantes']
processed_db = config['databases']['processed_visitantes']

class Visitante():
    def __init__(self, data, database):
        self.database = database
        self.data = data
        
        self.nome = data['nome']
        self.rg = data['rg']
        
    def isProcessed(self):
        sql = f"SELECT * FROM {processed_db['table']} WHERE rg = '{self.rg}' ;"
        data = self.database.processed.run(sql)
        if data:
            return True
        else:
            return False
        
    def process(self, saida = False):
        columns = '(nome, rg)'
        values = f'("{self.nome}", "{self.rg}")'
        sql = f"insert into {processed_db['table']} {columns} values {values} ;"
        print(sql)
        
        try:
            self.database.processed.run(sql)
            print(datetime.now().time())
            print(f'processed visitante, name: {self.nome}, rg: {self.rg}')
        except Exception as error:
            print(error)