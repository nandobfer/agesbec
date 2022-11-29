import sys, json
from src.Receita import Receita

if len(sys.argv) > 1:
    acesso = sys.argv[1]
    
    try:
        acesso = json.loads(acesso)
        print(acesso)   
        request = Receita(node=True).getResponse(acesso)
        print(request)
    except Exception as error:
        print(error)
    
    sys.stdout.flush()
     