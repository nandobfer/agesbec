from src.database_handler import Database
from src.Acesso import Acesso
from time import sleep
import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect']
processed_db = config['databases']['processed']
database = Database()

def start():
    database.collect.connect(collect_db)
    database.processed.connect(processed_db)
    while True:
        collectData()
        collectData(saida = True)

def collectData(saida = False):
    tipo = 'entrada'
    if saida:
        tipo = 'saida'
    try:
        sql = f'SELECT * FROM {config["databases"]["collect"]["table"]} ORDER BY data_{tipo} DESC, hora_{tipo} DESC LIMIT 10'
        acessos = database.collect.run(sql)
        for item in acessos:
            # print(item)
            acesso = Acesso(item, database)
            if not saida:
                if not acesso.isProcessed():
                    acesso.process()
            else:
                if not acesso.isProcessed(saida = True):
                    acesso.process(saida = True)
    except KeyboardInterrupt:
        print('Encerrado pelo usuário')
        database.collect.disconnect()    

start()