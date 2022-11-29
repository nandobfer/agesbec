from src.database_handler import Database
from src.Acesso import Acesso
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
        collectCredenciamento()
        break
        collectAcessos()
        sleep(1)
        collectAcessos(saida = True)
        sleep(1)
        
def collectCredenciamento():
    database.isUp()

    try:
        sql = f'SELECT TOP 1 * FROM {config["databases"]["collect_funcionarios"]["table"]}'
        funcionarios = database.collect.query(sql)['results']
        print(funcionarios)

    except KeyboardInterrupt:
        print('Encerrado pelo usuário')
        database.collect.disconnect() 

def collectAcessos(saida = False):
    database.isUp()
    tipo = 'entrada'
    if saida:
        tipo = 'saida'
        sql = f'SELECT * FROM {config["databases"]["processed_acessos"]["table"]} ORDER BY data_{tipo} DESC, hora_{tipo} DESC LIMIT 20'
    try:
        sql = f'SELECT TOP 10 * FROM {config["databases"]["collect_acessos"]["table"]} ORDER BY data_{tipo} DESC, hora_{tipo} DESC'
        acessos = database.collect.query(sql)['results']
        for item in acessos:
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