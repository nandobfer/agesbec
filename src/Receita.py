from datetime import datetime, timezone, timedelta
import json, requests, base64, os, sys
from print_dict import pd
config = json.load(open('config.json'))

class Receita():
    def __init__(self, object, endpoint, saida = False, node = False, credenciamento = False, demissao = False):
        self.endpoint = endpoint
        self.credenciamento = credenciamento
        self.demissao = demissao

        if not node:
            self.object = object
            self.saida = saida
        
            if not credenciamento:
                if saida:
                    self.data = object.data_saida
                    self.hora = object.hora_saida
                else:
                    self.data = object.data_entrada
                    self.hora = object.hora_entrada
            
            self.buildAPIAttributes()
        
    def buildDate(self, date, time_str):
        _time = datetime.strptime(time_str, '%H:%M').time().strftime('%H:%M:%S.%f')[:-3]
        formated_datetime = f'{date}T{_time}{config["timezone"]}'
        # formated_datetime = formated_datetime[:-9]+formated_datetime[-6:]
        # print(f'dataHoraOcorrencia: {formated_datetime}')
        return formated_datetime
    
    def buildNow(self):
        now = format((datetime.now(timezone.utc)- timedelta(seconds=60)).astimezone().isoformat())
        now = now[:-9]+now[-6:]
        now = now[:-3]+now[-2:]
        # print(f'dataHoraRegistro: {now}')
        return now

    def buildAPIAttributes(self):
        self.tipoOperacao = "R" if self.demissao else "I"
        self.idEvento = f'{self.object.id}'
        self.dataHoraOcorrencia = self.buildDate(self.data, self.hora) if not self.credenciamento else self.buildNow()
        self.dataHoraRegistro = self.buildDate(self.data, self.hora) if not self.credenciamento else self.buildNow()
        self.contingencia = False
        self.codigoRecinto = config["recinto"]
        if self.saida:
            self.direcao = 'S'
        else:
            self.direcao = 'E'
        self.nome = self.object.nome
        self.cpf = self.object.cpf
        
    def getResponse(self, data):
        global tokens, expiration
        url = f'{config["url"]}{self.endpoint}'
        
        if isTokenExpired():
            tokens = getToken()
        
        response = requests.post(url, json=data, headers={
            'Authorization': tokens["Set-Token"],
            'X-CSRF-Token': tokens["X-CSRF-Token"],
            })
        
        response_data = json.loads(response.text)
        request_data = {'body': json.loads(response.request.body)}
        full_response = {'request': request_data, 'response': response_data}
        
        return full_response
    
    def requestCredenciamento(self):
        data = dict((vars(self)))
        data.pop('object')
        data.pop('saida')
        data.pop('endpoint')
        data.pop('direcao')
        data.pop('credenciamento')
        data.pop('demissao')
        
        data.update({"credenciamentoAtivo": not self.demissao})
        
        response = self.getResponse(data)
        
        return response
        
    def requestAcesso(self):
        # print(f'request para: {url}')
        data = dict((vars(self)))
        data.pop('credenciamento')
        data.pop('demissao')
        data.pop('object')
        data.pop('saida')
        data.pop('endpoint')
        data.pop('data')
        data.pop('hora')
        
        response = self.getResponse(data)

        # pd(full_response)
            
        return response
    
        
def isTokenExpired():
    global expiration
    now = datetime.now()
    
    if now >= expiration:
        return True

def getToken():
    global tokens, expiration
    url = 'https://val.portalunico.siscomex.gov.br/portal/api/autenticar'
    headers = {
        "role-type": "DEPOSIT",
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

    expiration = datetime.fromtimestamp(int(new_tokens['X-CSRF-Expiration']) / 1000)
    # print(new_tokens)
    return new_tokens

expiration = None
tokens = getToken()