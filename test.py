from datetime import datetime, timezone
from src.Receita import Receita
class Mockado():
    def __init__(self) -> None:
        self.data_entrada = datetime.now().date()
        self.hora_entrada = datetime.now().time()
        self.nome = 'Fernando Burgos'
        self.id = 1
        self.cpf = '02576698506'
        self.identificacao = '1'
        
teste = Receita(Mockado())
teste.requestAcesso()