import sys, json
from src.Receita import Receita

if len(sys.argv) > 1:
    acesso = sys.argv[1]
    
    print(acesso)   
    print(type(acesso))
    
    sys.stdout.flush()
     