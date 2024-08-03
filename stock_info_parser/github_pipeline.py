import pandas as pd
import requests
import yaml
from mongo_handler import MongoDBHandler

class GitHubStockInfoDataCollector:
    BASE_URL = "https://raw.githubusercontent.com/turingplanet/stock-info-demo/main/atlas_csv/"
    LOCAL_CSV_DIR = "./github_data"
    FILES = {
        'nasdaq_100': 'nasdaq_100.csv',
        'company_overview': 'company_overview.csv',
        'stock_weekly_data': 'stock_weekly_data.csv',
        'quarterly_earnings': 'quarterly_earnings.csv',
        'cash_flow': 'cash_flow.csv',
        'news_sentiment': 'news_sentiment.csv'
    }
    MONGODB_DATABASE = 'GitHubStockInfoDB'

    def __init__(self):
        with open("secrets.yaml", "r") as file:
            config = yaml.safe_load(file)
        self.MONGODB_URI = config['mongo']['connection_str']
        self.mongo_handler = MongoDBHandler(self.MONGODB_DATABASE, self.MONGODB_URI)

    def download_csv(self, filename):
        url = self.BASE_URL + filename
        response = requests.get(url)
        if response.status_code == 200:
            with open(f'{self.LOCAL_CSV_DIR}/{filename}', 'wb') as file:
                file.write(response.content)
            print(f"Downloaded {filename} successfully.")
        else:
            print(f"Failed to download {filename}.")

    def fetch_and_save_csv_files(self):
        for _, file_name in self.FILES.items():
            self.download_csv(file_name)

    def save_data_to_mongo(self):
        print("Saving data to MongoDB...")
        for file_key, file_name in self.FILES.items():
            csv_path = f'{self.LOCAL_CSV_DIR}/{file_name}'
            collection_name = file_key.lower()
            print(f"Saving {collection_name} data to MongoDB...")
            self.mongo_handler.save_csv_to_collection(csv_path, collection_name)
        self.mongo_handler.disconnect()
        print("Finished saving all data to MongoDB.")

if __name__ == "__main__":
    print("Starting data collection...")
    collector = GitHubStockInfoDataCollector()
    collector.fetch_and_save_csv_files()
    collector.save_data_to_mongo()
    print("Data collection process completed.")
