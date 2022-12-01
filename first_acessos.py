from src.database_handler import Database
from src.Acesso import Acesso
from time import sleep
from datetime import datetime, timedelta
import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect_acessos']
processed_db = config['databases']['processed_acessos']
database = Database('acessos')

def start():
    database.collect.connect()
    database.processed.connect()
    
    collectAcessos()
    collectAcessos(saida = True)
        
def collectAcessos(saida = False):
    database.isUp()
    tipo = 'entrada'
    if saida:
        tipo = 'saida'
        sql = f'SELECT * FROM {config["databases"]["processed_acessos"]["table"]} ORDER BY data_{tipo} DESC, hora_{tipo} DESC LIMIT 20'
    try:
        sql = f'SELECT * FROM {config["databases"]["collect_acessos"]["table"]} ORDER BY data_{tipo} DESC, hora_{tipo} DESC'
        acessos = database.collect.query(sql)['results']
        for item in acessos:
            acesso = Acesso(item, database)
            if not acesso.isProcessed(saida = saida):
                acesso.process(saida = saida)

            if acessos.index(item) > 0 and acessos.index(item) % 100 == 0:
                print()
                print(f"""sleeping until {datetime.now() + timedelta(minutes=60)}.""")
                print()
                sleep(60 * 60)


    except KeyboardInterrupt:
        print('Encerrado pelo usuário')
        database.collect.disconnect() 

start()