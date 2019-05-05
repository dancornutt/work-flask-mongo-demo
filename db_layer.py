import pymongo
import csv
import logging


class MongoCloud():
    """Mongo Atlas Connection"""

    def __init__(self):
        self.user, self.user_pw = import_pass()
        self.connect = None

    def __enter__(self):
        self.connection = pymongo.MongoClient(f'mongodb+srv://{self.user}:{self.pw}@kiwi-jwnc9.azure.mongodb.net/test?retryWrites=true', maxPoolSize=50, connect=False)

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.connection.close()

    def import_pass():
        with open('passwords.txt', 'r') as f:
            data = f.readlines()
        for line in data:
            if "cluster admin user" in line:
                user = line.split()[-1:][0]
            if "cluster admin pw" in line:
                pw = line.split()[-1:][0]
        return user, pw


def log_setup():
    log_format = "%(asctime)s %(filename)s:%(lineno)-3d %(levelname)s \
    %(message)s"
    logging.basicConfig(level=logging.WARNING, format=log_format, filename='mylog.log')


def add_db(db):


mongo = pymongo.MongoClient(
    'mongodb+srv://{user}:{user_pw}@kiwi-jwnc9.azure.mongodb.net/test?retryWrites=true'.format(user=), maxPoolSize=50, connect=False)

db = pymongo.database.Database(mongo, 'irc_db')
col = pymongo.collection.Collection(db, 'parts')


# queries:
# all features of single part
# all parts
# all keys of part collection. returns dict[collection]: [Features of type list]
# all parts with kw filter
# all next higher (part number)
# all next lower (part_number)
