from src.database_handler import Database

database = Database()
print(database.collect)

cursor = database.collect.cursor()
data = cursor.execute('select Nome from Acessos')
print(data)
