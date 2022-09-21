from src.database_handler import Database

database = Database()
print(database.collect)

cursor = database.collect.cursor()
cursor.execute('select Nome from Acessos')
