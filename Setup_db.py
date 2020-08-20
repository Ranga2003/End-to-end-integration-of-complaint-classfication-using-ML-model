"""
Author: Pandurang Pampatwar
Date: Created: 4th July 2020
Purpose:
    1. This is the script to create new database and establish the connection to the same.
    2. New table can be created in the database.

"""
import sqlite3
from sqlite3 import Error

#function to establish connection to the database
def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
    return conn


conn = create_connection(".\complaints_log.db")

# function to create a table in to the mentioned database.
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
        c.execute("commit")
    except Error as e:
        print(e)

database = ".\complaints_log.db"

sql_create_table = """ CREATE TABLE IF NOT EXISTS complaints (
                                        Name text,
                                        OrderID text,
                                        OrderDate text,
                                        product text,
                                        Category text,
                                        UserNarrative text,
                                        Status text,
                                        ReferenceNumber text
                                    ); """

if conn is not None:
    create_table(conn, sql_create_table)
    print("table created")
    conn.close()
else:
    print("Error! cannot create the database connection.")
"""    
Results:
    1. New database was created successfully.
    2. New table was inserted into the same database.

"""