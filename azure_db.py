import psycopg2
import csv
import logging
from pprint import pprint


def import_pass():
    with open('passwords.txt', 'r') as f:
        data = f.readlines()
    for line in data:
        if "host" in line:
            host = line.split()[-1:][0]
        if "azure user" in line:
            user = line.split()[-1:][0]
        if "dbname" in line:
            dbname = line.split()[-1:][0]
        if "password" in line:
            password = line.split()[-1:][0]
        if "sslmode" in line:
            sslmode = line.split()[-1:][0]
    return host, user, dbname, password, sslmode


class AzureDB():

    def __init__(self):
        self.host, self.user, self.dbname, self.password, \
            self.sslmode = import_pass()
        self.conn = psycopg2.connect(
            f"host={self.host} user={self.user} dbname={self.dbname} password={self.password} sslmode={self.sslmode}")
        self.cursor = self.conn.cursor()
        print("Connection established")

    def __exit__(self, exc_type, exc_val, exc_tb):
        """On exit, commits cleanup"""
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def drop_tables(self):
        """drops all tables in db"""
        self.cursor.execute("DROP TABLE IF EXISTS inventory;")
        print("Finished dropping table (if existed)")

    def create_table(self, table):
        """creates new table"""
        self.cursor.execute(
            "CREATE TABLE inventory (id serial PRIMARY KEY, name VARCHAR(50), quantity INTEGER);")
        print("Finished creating table")

    def insert_data_in_table(self, table, data):
        self.cursor.execute(f"INSERT INTO {table} (name, quantity) VALUES (%s, %s);", ("banana", 150))
        print("Inserted 1 rows of data")


# QRYs
# 1) show are parts in a table.
    # param1:table
    # returns titles (list), data (list of lists)
# 2) enter part, gives next higher or next lower
    # params part number, type ("higher" or "lower")
# 3) IPL. List of lists of lists
    # param 1: Effectivity

# TABLES
    # AP: Customer, Line, Eff
    # Installs: Name, Number, Family, PIN, Status, Type, Starting STA, Ending STA, Location, Restricted use, First Use
    # Parts: Name, Number, Family, PIN, Type, Description
    # Contains: Parent_Table, Par_ID, Child_Table, Child_ID, QTY
