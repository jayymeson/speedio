from pymongo import MongoClient

uri = "mongodb://localhost:27017"

client = MongoClient(uri)
db = client['speedio']
collection_name = db['infos']