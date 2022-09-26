from datetime import datetime
import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect_acessos']
processed_db = config['databases']['processed_acessos']

class Visitante():
    def __init__(self, data, database) -> None:
        self.database = database
        self.data = data
        
        self.nome = data['nome']