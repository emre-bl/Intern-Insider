import random
from pymongo import MongoClient
from configparser import ConfigParser
from datetime import datetime, timedelta

# Veritabanı bağlantısı
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

# Rastgele tarih atama fonksiyonu
def assign_random_feedback_dates():
    reviews_collection = connect_to_collection('reviews')
    
    if reviews_collection is None:
        print("reviews collection'a bağlanılamadı.")
        return

    # Rastgele tarihlerin seçileceği yıl
    year = 2024
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    total_days = (end_date - start_date).days + 1  # Toplam gün sayısı

    # Tüm belgeleri sırayla güncelle
    reviews = reviews_collection.find()
    for review in reviews:
        # Rastgele gün seçimi
        random_days = random.randint(0, total_days - 1)
        random_date = start_date + timedelta(days=random_days)
        formatted_date = random_date.strftime("%d/%m/%Y")
        
        # Belgeyi güncelle
        reviews_collection.update_one(
            {"_id": review["_id"]},
            {"$set": {"feedback_date": formatted_date}}
        )
        print(f"Updated document {review['_id']} with new date {formatted_date}")

if __name__ == "__main__":
    assign_random_feedback_dates()
