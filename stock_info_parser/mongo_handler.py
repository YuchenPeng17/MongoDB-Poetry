import pandas as pd
from pymongo import MongoClient

class MongoDBHandler:
    def __init__(self, database_name, connection_uri="mongodb://localhost:27017/"):
        self.client = MongoClient(connection_uri)
        self.database = self.client[database_name]

    def save_csv_to_collection(self, csv_path, collection_name):
        data_frame = pd.read_csv(csv_path)
        data_frame.drop_duplicates(inplace=True)
        collection = self.database[collection_name]
        collection.insert_many(data_frame.to_dict(orient='records'))

    def disconnect(self):
        self.client.close()

