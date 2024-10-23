from pymongo import MongoClient
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')

psw = config.get('481-db','psw')
connection_string = config.get('481-db','connection_string')

def connect_to_db(collection_name = "reviews"):
    try:
        client = MongoClient(connection_string)
        db = client["Intern-insider"]
        collection = db[collection_name]
        print(f"Connected to {collection_name} collection")
        return collection
    except Exception as e:
        print(f"Error: {e}")
        return None
