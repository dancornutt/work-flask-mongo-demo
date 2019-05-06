import pymongo
import csv
import logging
from pprint import pprint


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


class MongoDB():
    """Mongo Atlas database object"""

    def __init__(self, db_name):
        self.name = db_name,
        client = MongoCloud()
        with client:
            database = client.connection[db_name]
        self.db = database

    def collection_search(self, coll_name, search_d, p_console=False):
        values = []
        qry = list(self.db[coll_name].find(search_d))
        keys = list(qry[0].keys())[1:]
        for item in qry:
            values.append([v for v in item.values()][1:])
        if p_console:
            pprint(values)
        return keys, values

    def add_collection_csv(self, collection, f_name_path=""):
        """Reads csv by line. Uses csv dict iterator to loop through csv and add to collection
        param1: target collection
        param2: relative path and filename to csv data
        """

        with open(f_name_path, mode='r', encoding='utf-8-sig') as csv_f:
            reader = csv.DictReader(csv_f)
            for row in reader:
                try:
                    self.db[collection].insert_one(row)
                except ValueError:
                    logging.debug("Error Parsing data: {}".format(row))


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


if __name__ == "__main__":
    db = MongoDB('kiwi_db')
    k, v = db.collection_search('parts', {}, p_console=True)
