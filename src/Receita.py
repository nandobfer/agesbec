from datetime import datetime, timezone
import json
config = json.load(open('config.json'))


class Receita():
    def __init__(self, acesso, saida = False):
        self.acesso = acesso
        self.saida = saida
        
        self.buildAPIAttributes()
        
    def buildDate(self, date, _time):
        formated_datetime = f'{date}T{_time}{config["timezone"]}'
        return formated_datetime

    def buildAPIAttributes(self):
        self.tipoOperacao = 'I'
        self.idEvento = ['id Acessos']
        self.dataHoraOcorrencia = format(datetime.now(timezone.utc).astimezone().isoformat())
        print(self.dataHoraOcorrencia)