from src.database_handler import Database
from src.Acesso import Acesso
from src.Receita import Receita
from time import sleep
import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect_acessos']
processed_db = config['databases']['processed_acessos']
database = Database('acessos')

def start():
    database.collect.connect()
    database.processed.connect()
    while True:
        collectData()
        sleep(1)
        collectData(saida = True)
        sleep(1)

def collectData(saida = False):
    database.isUp()
    tipo = 'entrada'
    if saida:
        tipo = 'saida'
        sql = f'SELECT * FROM {config["databases"]["processed_acessos"]["table"]} ORDER BY data_{tipo} DESC, hora_{tipo} DESC LIMIT 10'
    try:
        sql = f'SELECT TOP 1 * FROM {config["databases"]["collect_acessos"]["table"]} ORDER BY data_{tipo} DESC, hora_{tipo} DESC'
        acessos = database.collect.query(sql)['results']
        for item in acessos:
            acesso = Acesso(item, database)
            print(acesso.nome)
            if not saida:
                if not acesso.isProcessed():
                    request = Receita(acesso).requestAcesso()
                    acesso.process(request = json.dumps(request))
            else:
                if not acesso.isProcessed(saida = True):
                    request = Receita(acesso, saida = True).requestAcesso()
                    acesso.process(request = json.dumps(request), saida = True)
    except KeyboardInterrupt:
        print('Encerrado pelo usuário')
        database.collect.disconnect()    

start()