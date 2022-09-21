from src.database_handler import Database
from src.Acesso import Acesso
from src.Receita import Receita
from time import sleep
import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect_acessos']
processed_db = config['databases']['processed_acessos']
database = Database()

def start():
    database.collect.connect()
    database.processed.connect()
    while True:
        collectData()
        # collectData(saida = True)

def collectData(saida = False):
    tipo = 'entrada'
    if saida:
        tipo = 'saida'
        sql = f'SELECT * FROM {config["databases"]["processed_acessos"]["table"]} ORDER BY data_{tipo} DESC, hora_{tipo} DESC LIMIT 10'
    try:
        sql = f'SELECT TOP 10 * FROM {config["databases"]["collect_acessos"]["table"]} ORDER BY data_{tipo} DESC, hora_{tipo} DESC'
        acessos = database.collect.query(sql)['results']
        print(acessos)
        for item in acessos:
            pass
            # acesso = Acesso(item, database)
            # if not saida:
            #     if not acesso.isProcessed():
            #         acesso.process()
            #         request = Receita(acesso)
            # else:
            #     if not acesso.isProcessed(saida = True):
            #         acesso.process(saida = True)
            #         request = Receita(acesso, saida = True)
    except KeyboardInterrupt:
        print('Encerrado pelo usuário')
        database.collect.disconnect()    

start()