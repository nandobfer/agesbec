from datetime import datetime
from src.Receita import Receita
import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect_funcionarios']
processed_db = config['databases']['processed_funcionarios']

class Funcionario():
    def __init__(self, data, database):
        self.database = database
        self.id = data['codigo']
        self.nome = data['nome']
        self.cpf = data['cpf'].replace('.', '').replace('-', '').replace(' ', '').replace(',', '') if data['cpf'] else None
        self.demitido = int(data['recisao'])
        self.inclusao = data['inclusao']
                
    def isProcessed(self):
        sql = f"""SELECT * FROM {processed_db['table']} WHERE codigo = '{self.id}' ;"""
        data = self.database.processed.run(sql)
        if data:
            return True
        else:
            return False
        
    def isResigned(self):
        sql = f"""SELECT * FROM {processed_db['table']} WHERE codigo = '{self.id}' AND demitido = 1 ;"""
        data = self.database.processed.run(sql)
        if data:
            return True
        else:
            return False
        
        
    def process(self):
        request = json.dumps(Receita(self, "/credenciamento-pessoas", credenciamento=True).requestCredenciamento())
        columns = '(codigo, nome, cpf, demitido, status, inclusao)'
        
        sql = f"""INSERT INTO {processed_db["table"]} {columns} VALUES (%s,%s,%s,%s,%s,%s);"""
        values = (self.id, self.nome, self.cpf, self.demitido, request, self.inclusao)
        
        try:
            self.database.processed.run(sql, prepared=True, values=values)
            print(datetime.now().time())
            print(f'accredited code {self.id}, name: {self.nome}')
        except Exception as error:
            print(error)
            
    def resign(self):
        request = json.dumps(Receita(self, "/credenciamento-pessoas", credenciamento=True, demissao=True).requestCredenciamento())
        columns = '(codigo, nome, cpf, demitido, status, inclusao)'
        
        sql = f"""UPDATE {processed_db["table"]} SET demitido = 1 WHERE codigo = %s ;"""
        values = self.id
        
        try:
            self.database.processed.run(sql, prepared=True, values=values)
            print(datetime.now().time())
            print(f'resigned code {self.id}, name: {self.nome}')
        except Exception as error:
            print(error)
