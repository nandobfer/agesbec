from datetime import datetime, timezone
import json, requests, base64, os
from print_dict import pd
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
        
    def buildDate(self, date, time_str):
        _time = datetime.strptime(time_str, '%H:%M').time().strftime('%H:%M:%S.%f')[:-3]
        formated_datetime = f'{date}T{_time}{config["timezone"]}'
        # formated_datetime = formated_datetime[:-9]+formated_datetime[-6:]
        # print(f'dataHoraOcorrencia: {formated_datetime}')
        return formated_datetime
    
    def buildNow(self):
        now = format(datetime.now(timezone.utc).astimezone().isoformat())
        now = now[:-9]+now[-6:]
        now = now[:-3]+now[-2:]
        # print(f'dataHoraRegistro: {now}')
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
        global tokens, expiration
                
        url = f'{config["url"]}{self.endpoint}'
        # print(f'request para: {url}')
        data = dict((vars(self)))
        data.pop('acesso')
        data.pop('saida')
        data.pop('endpoint')
        data.pop('data')
        data.pop('hora')
        
        response = requests.post(url, json=data, headers={
            'Authorization': tokens["Set-Token"],
            'X-CSRF-Token': tokens["X-CSRF-Token"],
            })
        response_data = json.loads(response.text)
        request_data = {'header': response.request.headers, 'body': response.request.body}
        full_response = {'request': request_data, 'response': response_data}
        # pd(full_response)
        if full_response['response']['tag'] == '[RCNT-KIEICW9ZK5]':
            getToken()
            return self.requestAcesso()
            
        # print('request.headers')
        # print(response.request.headers)
        # print()
        # print('request.body')
        # print(response.request.body)
        # print()
        # print('response.headers:')
        # print(response.headers)
        # print()
        # print('response.body')
        # print(response_data)
        
        # if response_data['code'] == 'PUCX-ER0201':
        #     self.credenciar(dict(data), tokens)
        #     self.requestAcesso()
            
        return full_response
            
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
        
def isTokenExpired():
    global expiration
    now = datetime.now()
    

    delta = expiration - now
    print(f"expiration: {expiration}")
    print(f"now: {now}")
    print(f"delta: {delta}")
    if delta.days:
        return True
        
        
def getToken():
    global tokens, expiration
    url = config["authentication"]["url"]
    headers = {
        "role-type": config["authentication"]["role-type"],
        "content-type": "application/json",
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
    # data = json.loads(response.text)
    new_tokens = {
        'Set-Token': response.headers['Set-Token'],
        'X-CSRF-Token': response.headers['X-CSRF-Token'],
        'X-CSRF-Expiration': response.headers['X-CSRF-Expiration']
    }
    with open('log.txt', 'w') as f:
        f.write(f"now: {datetime.now()} \n{new_tokens}")
    expiration = datetime.fromtimestamp(int(new_tokens['X-CSRF-Expiration']) / 1000)
    print(new_tokens)
    return new_tokens
    
        
expiration = None
tokens = getToken()