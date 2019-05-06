import pymongo
import csv
import logging
from pprint import pprint
from bson.json_util import dumps


def import_pass():
    with open('passwords.txt', 'r') as f:
        data = f.readlines()
    for line in data:
        if "cluster admin user" in line:
            user = line.split()[-1:][0]
        if "cluster admin pw" in line:
            pw = line.split()[-1:][0]
    return user, pw


class MongoCloud():
    """Mongo Atlas Connection"""

    def __init__(self):
        self.user, self.user_pw = import_pass()
        self.connection = None

    def __enter__(self):
        conn_str = f'mongodb+srv://{self.user}:{self.user_pw}@kiwi-jwnc9.azure.mongodb.net/test?retryWrites=true'
        print("Connection Established")
        self.connection = pymongo.MongoClient(conn_str, maxPoolSize=50)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()
        print("Connection Closed")

    def add_db(self, db):
        self.connection().database.Database(mongo, db)

    def add_col(self, col):
        self.connection().collection.Collection(self.db, col)


def log_setup():
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s \
    %(message)s"
    logging.basicConfig(level=logging.WARNING, format=log_format, filename='app_log/logs.log')


# queries:
# all features of single part
# all parts
# all keys of part collection. returns dict[collection]: [Features of type list]
# all parts with kw filter
# all next higher (part number)
# all next lower (part_number)

# function(collection, dict[col]: values
#   returns json of query

def connect_db(db):
    client = MongoCloud()
    with client:
        database = client.connection[db]
    return database


def add_collection_csv(collection, f_name_path=""):
    """Reads csv by line. Uses csv dict iterator to loop through csv and add to collection
    param1: target collection
    param2: relative path and filename to csv data
    """

    cd = db[collection]
    with open(f_name_path, mode='r', encoding='utf-8-sig') as csv_f:
        reader = csv.DictReader(csv_f)
        for row in reader:
            try:
                cd.insert_one(row)
            except ValueError:
                logging.debug("Error Parsing data: {}".format(row))


def collection_search(col_name, search_d, p_console=False):
    qry = list(db[col_name].find(search_d))
    if p_console:
        pprint(qry)
    return qry


if __name__ == "__main__":
    db = connect_db('kiwi_db')
