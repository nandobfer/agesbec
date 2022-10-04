from datetime import datetime, timezone
import json, requests, base64
config = json.load(open('config.json'))

class Mockado():
    def __init__(self) -> None:
        self.data_entrada = datetime.now().date()
        self.hora_entrada = datetime.now().time()
        self.nome = 'Edinaldo Bueno Costa'
        self.id = 1
        self.cpf = '14254811837'
        self.identificacao = '1'

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
        self.idEvento = f'{self.acesso.id}'
        self.dataHoraOcorrencia = self.buildDate(self.data, self.hora)
        self.dataHoraRegistro = format(datetime.now(timezone.utc).astimezone().isoformat())
        self.contingencia = False
        self.codigoRecinto = config["recinto"]
        if self.saida:
            self.direcao = 'S'
        else:
            self.direcao = 'E'
        self.nome = self.acesso.nome
        self.cpf = self.acesso.cpf
        
    def request(self):
        url = f'{config["url"]}/{self.endpoint}'
        print(f'request para: {url}')
        data = dict((vars(self)))
        data.pop('acesso')
        data.pop('saida')
        data.pop('endpoint')
        data.pop('data')
        data.pop('hora')
        
        token = self.getToken()
        
        print(json.dumps(
            data, sort_keys=True,
            indent=4,
            separators=(',', ': ')
            ))
        
        response = requests.post(url, json=data, headers={
            'Authorization': f'Bearer {token["access_token"]}',
            'Authorization-Pucomex': token["jwt_pucomex"],
            })
        response_data = json.loads(response.text)
        # print(response.request.headers)
        # print()
        print(response_data)
        
        if response_data['code'] == 'PUCX-ER0201':
            self.credenciar(dict(data), token)
            self.request()
        
        
    def getToken(self):
        url = config["authentication"]["url"]
        consumer = base64.b64encode(config["authentication"]["consumer"].encode()).decode()
        headers = {
            "authorization": "Basic %s" % consumer,
            "role-type": config["authentication"]["role-type"],
            "content-type": "application/json",
            "Pucomex": "true"
        }
        data = {
            "uri": config["url"]
        }
        
        # print(headers)
        response = requests.post(url, headers=headers, json=data, cert=['/home/suporte/certificado/rubimar.crt', '/home/suporte/certificado/rubimar.pem'])
        data = json.loads(response.text)
        token = data['access_token']
        return data
    
    def credenciar(self, data, token):
        data.pop('direcao')
        url = f'{config["url"]}/sapi/ext/credenciamento-pessoas'
        print(f'request para: {url}')

        print(json.dumps(
            data, sort_keys=True,
            indent=4,
            separators=(',', ': ')
            ))
        
        response = requests.post(url, json=data, headers={
            'Authorization': f'Bearer {token["access_token"]}',
            'Authorization-Pucomex': token["jwt_pucomex"],
            })
        response_data = json.loads(response.text)
        print(response_data)
        
        
teste = Receita(Mockado())
teste.request()