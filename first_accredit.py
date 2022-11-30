from src.database_handler import Database
from src.Funcionario import Funcionario
from time import sleep
import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect_funcionarios']
processed_db = config['databases']['processed_funcionarios']
database = Database('funcionarios')

def start():
    database.collect.connect()
    database.processed.connect()
    
    collectCredenciamento()
        
def collectCredenciamento():
    try:
        sql = f"""SELECT * FROM {config["databases"]["collect_funcionarios"]["table"]} WHERE recisao='0' ORDER BY codigo DESC"""
        funcionarios = database.collect.query(sql)['results']
        print(len(funcionarios))
        
        for item in funcionarios:
            funcionario = Funcionario(item, database)
            funcionario.process()

            if funcionarios.index(item) > 0 and funcionarios.index(item) % 20 == 0:
                sleep(60 * 60)


    except KeyboardInterrupt:
        print('Encerrado pelo usuário')
        database.collect.disconnect() 

start()