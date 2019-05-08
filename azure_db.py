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
        print("I am exiting this BS")
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

    def drop_tables(self, table):
        """drops all tables in db"""
        self.cursor.execute(f"DROP TABLE IF EXISTS {table};")
        print(f"Finished dropping {table} (if existed)")

    def create_table(self, table, fields):
        """creates new table"""
        self.cursor.execute(
            f"CREATE TABLE {table} ({fields});")
        # APs ==> id serial PRIMARY KEY, customer VARCHAR(50), line_number VARCHAR(4), tail VARCHAR(15), status VARCHAR(50)
        # Installs ==> id serial PRIMARY KEY, owned_by VARCHAR(20), install_name VARCHAR(40), install_number VARCHAR(40), family VARCHAR(50), pin VARCHAR(20), status_type VARCHAR(20), starting VARCHAR(20), ending VARCHAR(20), location VARCHAR(20), restricted_use VARCHAR(20), first_use VARCHAR(20), comments VARCHAR(500), iws_comments VARCHAR(500)
        # Parts ==> id serial PRIMARY KEY, part_number VARCHAR(50), part_name VARCHAR(50), part_type VARCHAR(10), revision VARCHAR(3), pin VARCHAR(10), family_type VARCHAR(50), clg_type VARCHAR(10), side VARCHAR(20), location VARCHAR(20), sta VARCHAR(10), part_restriction VARCHAR(30), first_use VARCHAR(20), comments VARCHAR(500), similar_to VARCHAR(50), iws_comments VARCHAR(500)
        # Contains ==>
        print("Finished creating table")

    def import_csv(self, table, fields, abs_path, delimiter=","):
        self.cursor.execute(
            f"""COPY {table}({fields})
            FROM '{abs_path}' DELIMITER '{delimiter}' CSV HEADER;"""
        )

    def insert_data_in_table(self, table, csv_r_path):
        with open(csv_r_path, 'r') as f:
            headers = next(f).strip()
            headers = headers.replace(',', ', ')
            data = f.readlines()
        for line in data:
            values = "'" + line.replace(",", "', '").strip() + "'"
            com_str = f"INSERT INTO {table} ({headers}) VALUES ({values});"
            print(com_str)
            self.cursor.execute(f"INSERT INTO {table} ({headers}) VALUES ({values});")
            print("Inserted 1 rows of data: {values}")


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

if __name__ == "__main__":
    db = AzureDB()
