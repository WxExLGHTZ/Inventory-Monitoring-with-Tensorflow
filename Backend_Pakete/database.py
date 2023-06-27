import pyodbc

from Backend_Pakete.errormanager import *

class Database:


    def __init__(self):
        print("Database object created")


    def connection(self):
        server = 'txt-model-factory-db.database.windows.net'
        database = 'TxtModelFactoryDashboard'
        username = 'team3'
        password = 'SWE2021!'

        # Connection
        try:
            cnxn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server}; \
                                                 SERVER=' + server + '; \
                                                 DATABASE=' + database + '; \
                                                 UID=' + username + '; \
                                                 PWD=' + password)
            # print("connection to database successful")

        except pyodbc.Error as ex:
            raise DatabaseError
            # print("failed to connect to database")

        return cnxn






    # insert data in database
    def insert_data(self, date_time, error_msg, a1=0, a2=0, a3=0, b1=0, b2=0, b3=0, c1=0, c2=0, c3=0):

        cnxn = self.connection()

        # connection cursor
        cursor = cnxn.cursor()

        errorlog_id = ""

        # insert data in ErrorLog
        sql_insert_query_err = """INSERT INTO ErrorLog (id, CreatedOn, ErrorLog) VALUES (NEWID(), ?, ?)"""
        insert_parameters_err = (date_time, error_msg)

        cursor.execute(sql_insert_query_err, insert_parameters_err)
        cnxn.commit()


        # get ErrorLogId of recent recognition
        returned_data = cursor.execute('SELECT e.id from ErrorLog e WHERE e.CreatedOn = ?', (date_time))

        for row in returned_data:
            errorlog_id = row[0]


        # instert data in WarehouseStock
        sql_insert_query_stock = """INSERT INTO WarehouseStock (id, A1, A2, A3, B1, B2, B3, C1, C2, C3, CreatedOn, ErrorLogId) VALUES (NEWID(), ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )"""
        insert_parameters_stock = (a1, a2, a3, b1, b2, b3, c1, c2, c3, date_time, errorlog_id)

        cursor.execute(sql_insert_query_stock, insert_parameters_stock)
        cnxn.commit()

        errorlog_id = ""

#----------------------------------------------------------------------------------------
# nachfolgender code ist für den Benutzer nicht relevant
#----------------------------------------------------------------------------------------
    # # delete all data
    # def delete_all(self, table):
    #
    #     cnxn = self.connection()
    #     cursor = cnxn.cursor()
    #
    #     sql_query = 'DELETE from ' + table
    #
    #     cursor.execute(sql_query)
    #     cnxn.commit()


    # # view all data
    # def view_all(self, table):
    #
    #     cnxn = self.connection()
    #     cursor = cnxn.cursor()
    #
    #     sql_query = 'SELECT * from ' + table
    #     all = cursor.execute(sql_query)
    #
    #     for row in all:
    #         print(row)
