import pymongo

mongo = pymongo.MongoClient(
    'mongodb+srv://kiwi-admin:Test777Boeing@kiwi-jwnc9.azure.mongodb.net/test?retryWrites=true', maxPoolSize=50, connect=False)

db = pymongo.database.Database(mongo, 'irc_db')
col = pymongo.collection.Collection(db, 'parts')
