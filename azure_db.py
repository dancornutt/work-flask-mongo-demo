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

    def drop_table(self, table):
        """Drops all table in db
        table: (str) table to be dropped"""
        self.cursor.execute(f"DROP TABLE IF EXISTS {table};")
        print(f"Finished dropping {table} (if existed)")

    def create_table(self, table, fields):
        """creates new table"""
        self.cursor.execute(
            f"CREATE TABLE {table} ({fields});")

        print("Finished creating table")

    def insert_data_in_table(self, table, csv_r_path):
        with open(csv_r_path, 'r') as f:
            headers = next(f).strip()
            headers = headers.replace(',', ', ')
            data = f.readlines()
        for line in data:
            values = "'" + line.replace(",", "', '").strip() + "'"
            self.cursor.execute(f"INSERT INTO {table} ({headers}) VALUES ({values});")


def collection_search(table, search_d={}, p_console=False):
    db = AzureDB()
    db.cursor.execute(f"SELECT * FROM {table};")
    data = db.cursor.fetchall()
    db.cursor.execute(f"SELECT COLUMN_NAME FROM information_schema.COLUMNS WHERE TABLE_NAME = '{table}';")
    h_data = db.cursor.fetchall()
    headers = []
    for item in h_data:
        headers.append(item[0])
    return headers, data


def ap_install(ap):
    pass


def part_lower_search(part_number):
    """Searches next lower for specified part number
    part_number: str() parent part number
    return: headers[list], data[list of lists]
    """
    db = AzureDB()
    db.cursor.execute(f"""SELECT Child.*, br.quantity
                      FROM parts AS Parent
                      INNER JOIN parent_child AS br
                      ON Parent.id=br.parent_id
                      INNER JOIN parts as Child
                      ON br.child_id=Child.id
                      WHERE Parent.part_number={part_number}
                      """)


def airplane_lower_search(line_number):
    """Searches next lower for specified line number
    part_number: str() parent part number
    return: headers[list], data[list of lists]
    """
    db = AzureDB()
    s_str = f"""SELECT install.*, br.quantity
                      FROM airplanes AS AP
                      INNER JOIN airplane_install AS br
                      ON AP.id=br.ap_id
                      INNER JOIN installs as install
                      ON br.install_id=install.id
                      WHERE AP.line_number = '{line_number}';
                      """
    print(s_str)
    db.cursor.execute(s_str)
    db.conn.commit()
    return None, db.cursor.fetchall()
