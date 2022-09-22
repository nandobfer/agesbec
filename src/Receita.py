from datetime import datetime, timezone
import json, requests
config = json.load(open('config.json'))

class Mockado():
    def __init__(self) -> None:
        self.data_entrada = datetime.now().date()
        self.hora_entrada = datetime.now().time()
        self.nome = 'Fernando Burgos'

class Receita():
    def __init__(self, acesso, saida = False):
        self.acesso = acesso
        self.saida = saida
        self.endpoint = "/sapi/ext/acesso-pessoas"
        
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
        self.idEvento = ['id acessos']
        self.dataHoraOcorrencia = self.buildDate(self.data, self.hora)
        self.dataHoraRegistro = format(datetime.now(timezone.utc).astimezone().isoformat())
        self.contingencia = False
        self.codigoRecinto = None # ONDE?
        if self.saida:
            self.direcao = 'S'
        else:
            self.direcao = 'E'
        self.nome = self.acesso.nome
        
    def request(self):
        url = f'{config["url"]}/{self.endpoint}'
        print(f'request para: {url}')
        data = (vars(self))
        data.pop('acesso')
        data.pop('saida')
        data.pop('endpoint')
        data.pop('data')
        data.pop('hora')
        
        print(json.dumps(
            data, sort_keys=True,
            indent=4,
            separators=(',', ': ')
            ))
        
        response = requests.post(url, json=data)
        print(response.text)
        
teste = Receita(Mockado())
teste.request()