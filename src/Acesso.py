import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect']
processed_db = config['databases']['processed']

class Acesso():
    def __init__(self, data, database):
        self.database = database
        self.id = data[0]
        self.nome = data[1]
        self.cpf = data[2]
        self.data_entrada = data[3]
        self.hora_entrada = data[4]
        self.data_saida = data[5]
        self.hora_saida = data[6]

    def isProcessed(self):
        sql = f"select * from {processed_db['table']} where cpf = '{self.cpf}' and data_entrada = '{self.data_entrada}' and hora_entrada = '{self.hora_entrada}';"
        data = self.database.processed.run(sql)
        if data:
            return True
        else:
            return False
        
    def process(self):
        columns = '(id, nome, cpf, data_entrada, hora_entrada, data_saida, hora_saida)'
        values = (self.id, self.nome, self.cpf, self.data_entrada, self.hora_entrada, self.data_saida, self.hora_saida)
        sql = f"insert into {processed_db['table']} {columns} values ({self.id}, '{self.nome}', '{self.cpf}', '{self.data_entrada}', '{self.hora_entrada}', '{self.data_saida}', '{self.hora_saida}');"
        self.database.processed.run(sql, commit = True)

        # ENVIAR PRA API AQUI

        print(f'processed id {self.id}')