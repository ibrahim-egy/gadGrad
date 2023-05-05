from pymongo import MongoClient


mongo_atlas_url = "URL"

client = MongoClient(mongo_atlas_url, 27017)
db = client['DATABASE_NAME']
users = db['COLLECTION_NAME']



