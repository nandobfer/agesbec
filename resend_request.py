import sys, json
from src.Receita import Receita

if len(sys.argv) > 1:
    acesso = json.loads(sys.argv[1])
    
    print(acesso)   
    
    
    sys.stdout.flush()
     