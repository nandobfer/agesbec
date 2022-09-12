import mysql.connector


class Mysql():
    def __init__(self, login_table):
        self.login_table = login_table
    
    def run(self, sql):
        cursor = self.connection.cursor(buffered=True)
        cursor.execute(sql)
        data = None
        
        if sql.split()[0].lower() == 'select':
            data = cursor.fetchall()
            
        self.connection.commit()  

        cursor.close()
        return data

    def connect(self, auth:dict):
        ''' Try to connect to a database with auth params defined in config file '''
        try:
            self.connection = mysql.connector.connect(host=auth['host'],
                                                      database=auth['database'],
                                                      user=auth['user'],
                                                      password=auth['password'])
            if self.connection.is_connected():
                db_Info = self.connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = self.connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)
                # cursor.close()
                self.auth = auth

                return self.connection

        except Exception as e:
            print(e)

    def disconnect(self):
        ''' Disconnect from database '''
        if self.connection.is_connected():
            self.connection.close()
            print("MySQL connection is closed")

    def fetchTable(self, table, rows = 0, where=[], reversed=None, ordered=None):
        ''' Fetch a number of rows from a table that exists in database.
        Number of rows and table defined in config file.
        if number of rows equals to 0, will try to fetch all rows.'''

        if where:
            sql = f'SELECT * FROM `{table}` WHERE {where[0]} = "{where[1]}"'
            if reversed:
                sql = f'SELECT * FROM `{table}` WHERE {where[0]} = "{where[1]}" ORDER BY {reversed} DESC'
        else:
            sql = f"SELECT * FROM `{table}` WHERE 1"

        if ordered:
            sql = f'{sql} ORDER BY {ordered}'

        cursor = self.connection.cursor(buffered=True)
        cursor.execute(sql)
        if rows > 1:
            records = cursor.fetchmany(rows)
        else:
            records = cursor.fetchall()

        # print(f'Total number of rows in table: {cursor.rowcount}')
        # print(f'Rows fetched: {len(records)}')

        data = []
        for row in records:
            row = list(row)
            data.append(row)

        cursor.close()
        return data

    def updateTable(self, table, id, column, value, id_column):
        command = f'Update {table} set {column} = "{value}" where {id_column} = {id}'
        cursor = self.connection.cursor()
        cursor.execute(command)
        self.connection.commit()
        cursor.close()
        print("Record Updated successfully ")
