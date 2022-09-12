from src.database_handler import Database
from src.Receita import Receita
from time import sleep
import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect_visitantes']
processed_db = config['databases']['processed_visitantes']
database = Database()

def start():
    database.collect.connect(collect_db)
    database.processed.connect(processed_db)
    while True:
        collectData()

def collectData():
    tipo = 'entrada'
    try:
        sql = f'SELECT * FROM {collect_db["table"]} ORDER BY data_{tipo} DESC, hora_{tipo} DESC LIMIT 10'
        acessos = database.collect.run(sql)
        for item in acessos:
            # print(item)
            visitante = Visitante(item, database)
            if not visitante.isProcessed():
                visitante.process()
                request = Receita(visitante=True)
    except KeyboardInterrupt:
        print('Encerrado pelo usuário')
        database.collect.disconnect()    

start()