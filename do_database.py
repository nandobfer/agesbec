from src.database_handler import Database
from datetime import datetime
import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect_acessos']
processed_db = config['databases']['processed_acessos']
database = Database()

def printMenu():
    print('Funcionário entrou (1)')
    print('Funcionário saiu (2)')
    print('Visualizar acessos (3)')
    print('Visualizar processados (4)')
    op = input('Opção:')
    return op

def novaSaida():
    sql = f'SELECT * FROM acessos WHERE data_saida is NULL ORDER BY data_entrada, hora_entrada'
    data = database.collect.run(sql)
    if data:
        item = data.pop(0)
        now = datetime.now()
        data_saida = now.date()
        hora_saida = now.time()
        sql = f'UPDATE acessos SET data_saida = "{data_saida}", hora_saida = "{hora_saida}" WHERE id = {item[0]}'
        database.collect.run(sql, commit = True)
        print(f'saida inserida para id {item[0]}')
    else:
        print('nenhuma entrada')

def novaEntrada():
    id = len(database.collect.fetchTable(0, 'acessos'))
    now = datetime.now()
    data_entrada = now.date()
    hora_entrada = now.time()
    sql = f'INSERT INTO acessos (id, nome, cpf, data_entrada, hora_entrada, data_saida, hora_saida) VALUES ({id}, "Fernando Burgos", "02576698506", "{data_entrada}", "{hora_entrada}", NULL, NULL)'
    database.collect.run(sql, commit = True)
    print(f'Entrada inserida com id {id}')
    
def visualizarProcessados():
    data = database.processed.fetchTable(5, 'processados', ordered='id DESC')
    for item in data:
        print(item)

def visualizarAcessos():
    data = database.collect.fetchTable(5, 'acessos', ordered = 'id DESC')
    for item in data:
        print(item)

def start():
    database.collect.connect(collect_db)
    database.processed.connect(processed_db)
    try:
        while True:
            print()
            op = printMenu()
            if op == '1':
                novaEntrada()
            elif op == '2':
                novaSaida()
            elif op == '3':
                visualizarAcessos()
            elif op == '4':
                visualizarProcessados()
                
    except KeyboardInterrupt:
        print('End')
    
    
start()