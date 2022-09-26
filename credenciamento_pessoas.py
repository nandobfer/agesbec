from src.database_handler import Database
from src.Receita import Receita
from time import sleep
from src.Visitante import Visitante
import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect_visitantes']
processed_db = config['databases']['processed_visitantes']
database = Database('visitantes')

def start():
    database.collect.connect()
    database.processed.connect()
    while True:
        collectData()
        sleep(5)

def collectData():
    tipo = 'entrada'
    try:
        sql = f'SELECT TOP 1 * FROM {collect_db["table"]} ORDER BY codigo DESC'
        acessos = database.collect.query(sql)['results']
        for item in acessos:
            print(item)
            visitante = Visitante(item, database)
            if not visitante.isProcessed():
                visitante.process()
            #     request = Receita(visitante=True)
    except KeyboardInterrupt:
        print('Encerrado pelo usuário')
        database.collect.disconnect()    

start()