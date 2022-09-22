from datetime import datetime
import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect_acessos']
processed_db = config['databases']['processed_acessos']

class Acesso():
    def __init__(self, data, database):
        self.database = database
        self.id = data['id']
        self.nome = data['nome']
        self.cpf = data['cpf'].replace('.', '').replace('-', '') if data['cpf'] else None
        self.data_entrada = data['data_entrada']
        self.hora_entrada = data['hora_entrada']
        self.data_saida = data['data_saida']
        self.hora_saida = data['hora_saida']
        self.saida = bool(self.data_saida)
                
        try:
            self.data_entrada = self.data_entrada.date()
            self.data_saida = self.data_saida.date()
        except:
            pass
            

    def isProcessed(self, saida = False):
        tipo = 'entrada'
        if saida:
            tipo = 'saida'
            sql = f"select * from {processed_db['table']} where cpf = '{self.cpf}' and data_{tipo} = '{self.data_saida}' and hora_{tipo} = '{self.hora_saida}';"
        else:
            sql = f"select * from {processed_db['table']} where cpf = '{self.cpf}' and data_{tipo} = '{self.data_entrada}' and hora_{tipo} = '{self.hora_entrada}';"
        data = self.database.processed.run(sql)
        if data:
            return True
        else:
            return False
        
    def process(self, saida = False):
        if not saida:
            columns = '(id, nome, cpf, data_entrada, hora_entrada, data_saida, hora_saida)'
            values = (self.id, self.nome, self.cpf, self.data_entrada, self.hora_entrada, self.data_saida, self.hora_saida)
            sql = f"insert into {processed_db['table']} {columns} values ({self.id}, '{self.nome}', '{self.cpf}', '{self.data_entrada}', '{self.hora_entrada}', '{self.data_saida}', '{self.hora_saida}');"
        else:
            sql = f'SELECT * FROM {processed_db["table"]} WHERE id = {self.id} AND data_saida like "%None%"'
            exists = self.database.processed.run(sql)
            if exists:
                sql = f'UPDATE {processed_db["table"]} SET data_saida = "{self.data_saida}", hora_saida = "{self.hora_saida}" WHERE id = {self.id}'
            else:
                return False
        
        try:
            self.database.processed.run(sql)
            print(datetime.now().time())
            print(f'processed id {self.id}, name: {self.nome}, {"saida" if saida else "entrada"}')
        except Exception as error:
            print(error)
            
            

        # ENVIAR PRA API AQUI
