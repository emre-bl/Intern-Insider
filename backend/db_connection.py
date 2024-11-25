from pymongo import MongoClient
from configparser import ConfigParser

config = ConfigParser()
config.read('backend/config.ini')

connection_string = config.get('481-db', 'connection_string')

def connect_to_db():
    try:
        client = MongoClient(connection_string)
        db = client.mydatabase
        return db
    except Exception as e:
        print(f"Error: {e}")
        return None

def connect_to_collection(collection_name):
    try:
        db = connect_to_db()
        if db is None:
            raise Exception("Database bağlantısı kurulamadı.")
        
        collection = db[collection_name]
        print(f"Number of documents in {collection_name} collection: {collection.count_documents({})}")
        print(f"Connected to {collection_name} collection.")
        return collection
    except Exception as e:
        print(f"Error: {e}")
        return None

def create_review(review):
    try:
        collection = connect_to_collection('reviews')
        if collection is None:
            raise Exception("Collection bağlantısı kurulamadı.")
        
        result = collection.insert_one(review)
        return result.inserted_id
    except Exception as e:
        print(f"Error: {e}")
        return None

def get_companies():
    try:
        collection = connect_to_collection('company')
        if collection is None:
            raise Exception("Collection bağlantısı kurulamadı.")
        
        # Şirket isimlerini liste olarak döndür
        companies = collection.find({}, {"_id": 0, "name": 1})
        return [company["name"] for company in companies]
    except Exception as e:
        print(f"Error: {e}")
        return []

