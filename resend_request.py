import sys, json
from src.Receita import Receita

if len(sys.argv) > 1:
    acesso = sys.argv[1]
    
    print(acesso)   
    sys.stdout.flush()

    with open('test.txt', 'w') as f:
        f.write(str(acesso))
     