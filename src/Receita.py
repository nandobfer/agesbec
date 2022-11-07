from datetime import datetime, timezone
import json, requests, base64
config = json.load(open('config.json'))

class Receita():
    def __init__(self, acesso, saida = False):
        self.acesso = acesso
        self.saida = saida
        self.endpoint = "/acesso-pessoas"
        
        if saida:
            self.data = acesso.data_saida
            self.hora = acesso.hora_saida
        else:
            self.data = acesso.data_entrada
            self.hora = acesso.hora_entrada
        
        self.buildAPIAttributes()
        
    def buildDate(self, date, _time):
        formated_datetime = f'{date}T{_time}.000{config["timezone"]}'
        formated_datetime = formated_datetime[:-9]+formated_datetime[-6:]
        print(f'dataHoraOcorrencia: {formated_datetime}')
        return formated_datetime
    
    def buildNow(self):
        now = format(datetime.now(timezone.utc).astimezone().isoformat())
        now = now[:-9]+now[-6:]
        now = now[:-3]+now[-2:]
        print(f'dataHoraRegistro: {now}')
        return now

    def buildAPIAttributes(self):
        self.tipoOperacao = 'I'
        self.idEvento = f'{self.acesso.id}'
        self.dataHoraOcorrencia = self.buildDate(self.data, self.hora)
        self.dataHoraRegistro = self.buildDate(self.data, self.hora)
        self.contingencia = False
        self.codigoRecinto = config["recinto"]
        if self.saida:
            self.direcao = 'S'
        else:
            self.direcao = 'E'
        self.nome = self.acesso.nome
        self.cpf = self.acesso.cpf
        
    def requestAcesso(self):
        url = f'{config["url"]}{self.endpoint}'
        print(f'request para: {url}')
        data = dict((vars(self)))
        data.pop('acesso')
        data.pop('saida')
        data.pop('endpoint')
        data.pop('data')
        data.pop('hora')
        
        tokens = self.getToken()
        
        # print(json.dumps(
        #     data, sort_keys=True,
        #     indent=4,
        #     separators=(',', ': ')
        #     ))
        
        response = requests.post(url, json=data, headers={
            'Authorization': tokens["Set-Token"],
            'X-CSRF-Token': tokens["X-CSRF-Token"],
            })
        response_data = json.loads(response.text)
        print('request.headers')
        print(response.request.headers)
        print()
        print('request.body')
        print(response.request.body)
        print()
        print('response.headers:')
        print(response.headers)
        print()
        print('response.body')
        print(response_data)
        
        if response_data['code'] == 'PUCX-ER0201':
            self.credenciar(dict(data), tokens)
            self.requestAcesso()
            
        return response_data
            
    def credenciar(self, data, token):
        data.pop('direcao')
        url = f'{config["url"]}/credenciamento-pessoas'
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
        
        
    def getToken(self):
        url = config["authentication"]["url"]
        consumer = base64.b64encode(config["authentication"]["consumer"].encode()).decode()
        headers = {
            # "authorization": "Basic %s" % consumer,
            "role-type": config["authentication"]["role-type"],
            "content-type": "application/json",
            # "Pucomex": "true"
        }
        
        # print(headers)
        response = requests.post(
            url, 
            headers=headers, 
            cert=[
                '/home/suporte/certificado/agesbec/agesbec.crt', 
                '/home/suporte/certificado/agesbec/agesbec.pem'
                ]
        )
        data = json.loads(response.text)
        tokens = {
            'Set-Token': response.headers['Set-Token'],
            'X-CSRF-Token': response.headers['X-CSRF-Token'],
            'X-CSRF-Expiration': response.headers['X-CSRF-Expiration']
        }
        # print(tokens)
        return tokens
    
        
