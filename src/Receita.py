from datetime import datetime, timezone
import json
config = json.load(open('config.json'))


class Receita():
    def __init__(self, acesso, saida = False):
        self.acesso = acesso
        self.saida = saida
        
        if saida:
            self.data = acesso.data_saida
            self.hora = acesso.hora_saida
        else:
            self.data = acesso.data_entrada
            self.hora = acesso.hora_entrada
        
        self.buildAPIAttributes()
        
    def buildDate(self, date, _time):
        formated_datetime = f'{date}T{_time}{config["timezone"]}'
        return formated_datetime

    def buildAPIAttributes(self):
        self.tipoOperacao = 'I'
        self.idEvento = ['id Acessos']
        self.dataHoraOcorrencia = self.buildDate(self.data, self.hora)
        self.dataHoraRegistro = format(datetime.now(timezone.utc).astimezone().isoformat())
        self.contingencia = False
        self.codigoRecinto = None # ONDE?
        if self.saida:
            self.direcao = 'S'
        else:
            self.direcao = 'E'
        self.nome = self.acesso.nome