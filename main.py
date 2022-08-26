from database_handler import Database
import json

config = json.load(open('config.json'))
collect_db = config['databases']['collect']
database = Database()

def start():
    database.collect.connect(collect_db)



def end():
    database.collect.disconnect()    
    
start()
end()