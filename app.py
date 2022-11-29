from src.database_handler import Database
from src.Acesso import Acesso
from src.Funcionario import Funcionario
from time import sleep
import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect_acessos']
processed_db = config['databases']['processed_acessos']
database = Database('acessos')
funcionarios_db = Database('funcionarios')

def start():
    database.collect.connect()
    database.processed.connect()
    
    funcionarios_db.collect.connect()
    funcionarios_db.processed.connect()
    
    while True:
        collectCredenciamento()
        sleep(1)
        collectAcessos()
        sleep(1)
        collectAcessos(saida = True)
        sleep(1)
        
def collectCredenciamento():
    try:
        sql = f'SELECT TOP 5 * FROM {config["databases"]["collect_funcionarios"]["table"]} ORDER BY codigo DESC'
        funcionarios = funcionarios_db.collect.query(sql)['results']
        for item in funcionarios:
            funcionario = Funcionario(item, funcionarios_db)

            if not funcionario.isProcessed():
                funcionario.process()

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
            if not acesso.isProcessed(saida = saida):
                acesso.process(saida = saida)
                
    except KeyboardInterrupt:
        print('Encerrado pelo usuário')
        database.collect.disconnect()    

start()