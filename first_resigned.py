from src.database_handler import Database
from src.Funcionario import Funcionario
from time import sleep
from datetime import datetime, timedelta
import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect_funcionarios']
processed_db = config['databases']['processed_funcionarios']
database = Database('funcionarios')

def start():
    database.collect.connect()
    database.processed.connect()
    
    collectCredenciamento()
        
def collectCredenciamento():
    try:
        sql = f"""SELECT * FROM {config["databases"]["collect_funcionarios"]["table"]} WHERE recisao='1' ORDER BY codigo DESC"""
        funcionarios = database.collect.query(sql)['results']
        print(len(funcionarios))
        
        for item in funcionarios:
            funcionario = Funcionario(item, database)

            if not funcionario.isProcessed():
                columns = '(codigo, nome, cpf, demitido, status, inclusao)'
        
                sql = f"""INSERT INTO {processed_db["table"]} {columns} VALUES (%s,%s,%s,%s,%s);"""
                values = (funcionario.id, funcionario.nome, funcionario.cpf, funcionario.demitido, funcionario.inclusao)
                
                try:
                    database.processed.run(sql, prepared=True, values=values)
                    print(datetime.now().time())
                    print(f'resigned code {funcionario.id}, name: {funcionario.nome}')
                except Exception as error:
                    print(error)

    except KeyboardInterrupt:
        print('Encerrado pelo usuário')
        database.collect.disconnect() 

start()