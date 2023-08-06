import os
from mysql.connector import connect
from dotenv import load_dotenv


load_dotenv()


class Database():
    
    def __init__(self):
        self.host = os.getenv('DB_HOST')
        self.user = os.getenv('DB_USER')
        self.password = os.getenv('DB_PASS')
        self.connection = connect(
            host=self.host,
            user=self.user,
            password=self.password,
            port='3306',
            auth_plugin='mysql_native_password',
            use_pure=True,
            ssl={}
        )
        
        # check if database exists and create it if it doesn't exist
        cursor = self.connection.cursor()
        cursor.execute('CREATE DATABASE IF NOT EXISTS {db_name}'.format(db_name=os.getenv('DB_NAME')))
        self.connection.commit()
        
        # set the connection's database to the created one
        self.connection.database = os.getenv('DB_NAME')
    
    def get_cursor(self):
        ''' Return the cursor for the database connection '''
        
        cursor = self.connection.cursor()
        return cursor
    
    def create_table(self, table_sql):
        ''' Create a table using a generated SQL statement '''
        
        cursor = self.get_cursor()
        cursor.execute(table_sql)
        
        self.connection.commit()
    
    def select_all_rows(self, table):
        ''' Select all rows in the specified table '''
        
        sql = "SELECT * FROM {table}".format(table=table)
        
        cursor = self.get_cursor()
        cursor.execute(sql)
        
        rows = cursor.fetchall()
        
        return rows
    
    def select_by_id(self, table, row_id):
        ''' Select a single row from a table with the specified id '''
        
        sql = "SELECT * FROM {table} WHERE id = {row_id}".format(table=table, row_id=row_id)
        
        cursor = self.get_cursor()
        cursor.execute(sql)
        
        row = cursor.fetchone()
        
        return row
    
    def select_where(self, table, column, value, limit=None):
        ''' Selects all rows with a specific value from the given column with an optional limit '''
        
        sql = "SELECT * FROM {table} WHERE {column} = %s".format(table=table, column=column)
        
        if limit is not None and limit > 0:
            sql += " LIMIT {limit}".format(limit=limit)
        
        values = (value, )
        
        cursor = self.get_cursor()
        cursor.execute(sql, values)
        
        rows = cursor.fetchall()
        
        return rows
    
    def insert_row(self, table, columns, values):
        """ Inserts a row into a specified table in the active database """
        
        sql = "INSERT INTO {table} (".format(table=table)
        
        for column in columns:
            sql += "{column}".format(column=column)
            if columns.index(column) == len(columns) - 1:
                sql += ") VALUES ("
            else:
                sql += ", "
        
        for value in values:
            sql += "%s"
            if values.index(value) == len(values) - 1:
                sql += ");"
            else:
                sql += ", "
        
        print("Preparing insert statement: {sql} with values: ".format(sql=sql), values)
        
        cursor = self.get_cursor()
        cursor.execute(sql, values)
        
        self.connection.commit()
        
        print("Successfully inserted a new record into the {table} table.".format(table=table))
    
    def update_by_id(self, table, columns, values, row_id):
        """ Updates a table record's values based on the given row Id """
        
        sql = "UPDATE {table} SET ".format(table=table)
        
        for column in columns:
            sql += "{column} = %s".format(column=column)
            if columns.index(column) == len(columns) - 1:
                sql += ", updated_at = current_timestamp WHERE id = {row_id}".format(row_id=row_id)
            else:
                sql += ", "
        
        print("Preparing update statement: {sql} with values: {values}, at row Id: {row_id}".format(sql=sql, values=values, row_id=row_id))
        
        cursor = self.get_cursor()
        cursor.execute(sql, values)
        
        self.connection.commit()
        
        print("Successfully updated existing record with Id of {row_id} in the {table} table.".format(row_id=row_id, table=table))
    
    def delete_by_id(self, table, row_id):
        """ Deletes a record in a table by its row Id, therefore only one row is deleted """
        
        sql = "DELETE FROM {table} WHERE id = {row_id}".format(table=table, row_id=row_id)
        
        print("Preparing delete statement: {sql} for record with Id: {row_id}.".format(sql=sql, row_id=row_id))
        
        cursor = self.get_cursor()
        cursor.execute(sql)
        
        self.connection.commit()
        
        print("Successfully deleted record in {table} table with Id: {row_id}.".format(table=table, row_id=row_id))