from pymongo import MongoClient
import yaml

# 1. Load the configuration file
def load_config():
    with open('secrets.yaml', 'r') as file:
        return yaml.safe_load(file)
config = load_config()
connection_string = config['mongo']['connection_str']

# 2. Connect to MongoDB
uri = connection_string
client = MongoClient(uri)

db = client['mangoapp02']
collection = db['mycollection']

def insert_data():
    # Insert a single document
    document = {"name": "Alice", "age": 25, "city": "New York"}
    collection.insert_one(document)

    # Insert multiple documents
    documents = [
        {"name": "Bob", "age": 30, "city": "Chicago"},
        {"name": "Charlie", "age": 35, "city": "San Francisco"}
    ]
    collection.insert_many(documents)
    print("Data inserted successfully")

def query_data():
    # Query a single document
    result = collection.find_one({"name": "Alice"})
    print("Single document:", result)

    # Query multiple documents
    results = collection.find({"age": {"$gt": 25}})
    print("Multiple documents:")
    for doc in results:
        print(doc)

def update_data():
    # Update a single document
    collection.update_one({"name": "Alice"}, {"$set": {"age": 26}})
    print("Single document updated")

    # Update multiple documents
    collection.update_many({"city": "Chicago"}, {"$set": {"city": "Boston"}})
    print("Multiple documents updated")

def delete_data():
    # Delete a single document
    collection.delete_one({"name": "Alice"})
    print("Single document deleted")

    # Delete multiple documents
    collection.delete_many({"age": {"$lt": 30}})
    # collection.delete_many({"age": {"$gte": 30}})
    print("Multiple documents deleted")

def aggregate_data():
    # Aggregation operation
    pipeline = [
        {"$match": {"age": {"$gt": 20}}},
        {"$group": {"_id": "$city", "average_age": {"$avg": "$age"}}}
    ]
    results = collection.aggregate(pipeline)
    print("Aggregated data:")
    for doc in results:
        print(doc)

if __name__ == "__main__":
    print(f"Insert Data:____ ")
    insert_data()
    print(f"Query Data:____ ")
    query_data()
    print(f"Update Data:____ ")
    update_data()
    print(f"Delete Data:____ ")
    delete_data()
    print(f"Aggregate Data:____ ")
    aggregate_data()