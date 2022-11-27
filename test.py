from datetime import datetime, timezone
from src.Receita import Receita
class Mockado():
    def __init__(self) -> None:
        self.data_entrada = str(datetime.now().date())
        self.hora_entrada = str(datetime.now().time())
        self.nome = 'Fernando Burgos'
        self.id = 1
        self.cpf = '02576698506'
        self.identificacao = '1'
        
teste = Receita(Mockado())
teste.requestAcesso()

# now: 2022-11-26 21:39:43.096219
# {'Set-Token': 'eyJhbGciOiJSUzI1NiJ9.eyJleHRlbnNhbyI6IiIsInN1YiI6IjQ0MzUyNDI1MDAwMTM1IiwidGlwbyI6IlBKIiwiYW1iaWVudGUiOiJUUkUiLCJpcCI6IjE5MS43LjIwLjI2IiwiaXNzIjoiUFJJViIsImlkY2MiOjIxMzgzLCJub21lIjoiUklDQVJETyBEUkFHTyIsImlwT3JpZ2VtIjoiMTkxLjcuMjAuMjYiLCJkZXNjcmljYW8iOiJBUk1BWkVOUyBHRVJBSVMgRSBFTlRSRVBPU1RPUyBTQU8gQkVSTkFSRE8gRE8gQ0FNIiwicGVyZmlzIjoiSDRzSUFBQUFBQUFBQUl1dUxpbEt6Q3RPVE01UExiYUtEbkwyQzNFTmNfVUw4ZGR4ZG5SeGRBbjNjd3dKMGdrSmNYWjE5dmNMQ0hXSzFjbE1zWEp4RGZBUDlnelJTVWt0VHJaeVNTM0lMODRzT2J5d0tET19OaFlBVGpXRWFrNEFBQUE9IiwiY3JlZGVuY2lhbCI6NiwiY3BmIjoiMjY2MjMzMTQ4ODEiLCJpYXQiOjE2Njk1MDk1MzIsImNvbnRyb2xlIjo3LCJoYXNoIjoiODAyMzU3MWIxOTQ5MzcxMTNkZmFkMWU3M2RhYzM4ZGYifQ.qkgWk5KSJWa-IerwrIxEUJ0d3ZCBo-MtE78xAXkBnfPZm_lqK76FeUOp4KukDooSjZ2uS4D_yax0S0rPwfHSy5fktaKR0TKMzfXJ2RjtC6t7WYKRPHAlHtubQxZ6R10e2eF5daXeXdLSTfZ1Wv11J2Ov-CGlSuz76B-aop5m-oUE0AxJ677pBLPADhArbacG1MhU8KPBWxyA6TcQRALxybx9qQkLRyvEreshOIIPLa72OcGi2a8dcUA77W6zWaiT9RIcLV0Tx3ChQZvUeI9Yz4XCfg-hrJFGb1dJCcxZgMAwf-BMCCBKLa6WjWC2M30xUy7ypVFv7nEXqCO2qo_1rQ', 'X-CSRF-Token': 'nPrvEC+S59tQSynCfOe/f+k489XAzfz4yfDIdPtvtYK6UPUOXULSx3u1Wb3NdOT0F+GmhTDGpY4=', 'X-CSRF-Expiration': '1669513146518'}