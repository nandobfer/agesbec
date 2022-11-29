import sys, json
from src.Receita import Receita

if len(sys.argv) > 1:
    request_str = sys.argv[1]
    acesso = json.loads(request_str)

    print(acesso)
    
    
    sys.stdout.flush()
     