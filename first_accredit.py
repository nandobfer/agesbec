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
    
    while True:
        collectCredenciamento()
        sleep(1)
        
def collectCredenciamento():
    try:
        sql = f"""SELECT * FROM {config["databases"]["collect_funcionarios"]["table"]} WHERE recisao='0' ORDER BY codigo DESC"""
        funcionarios = database.collect.query(sql)['results']
        for item in funcionarios:
            print(item)
            # funcionario = Funcionario(item, database)

            # if not funcionario.isProcessed():
            #     funcionario.process()

    except KeyboardInterrupt:
        print('Encerrado pelo usuário')
        database.collect.disconnect() 

start()