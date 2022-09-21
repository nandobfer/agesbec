from src.database_handler import Database

database = Database()
print(database.collect)

cursor = database.cursor()
cursor.execute('select Nome from Acessos where nome like "%fabio%"')
