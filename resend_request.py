import sys, json
from src.Receita import Receita

if len(sys.argv) > 1:
    acesso = sys.argv[1]
    
    try:
        acesso = json.loads(acesso)
        request = Receita(True, "/acesso-pessoas", node=True).getResponse(acesso)
        print(json.dumps(request))
    except Exception as error:
        print(error)
    
    sys.stdout.flush()
     