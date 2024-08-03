import yaml
import pandas as pd
from nasdaq_fetcher import NasdaqDataFetcher
from alpha_api import AlphaVantageAPI
from mongo_handler import MongoDBHandler


class StockDataCollector:

    nasdaq_company_list_file = './data/nasdaq_100.csv'
    COMPANY_OVERVIEW_FILE = './data/company_overview.csv'
    STOCK_WEEKLY_DATA_FILE = './data/stock_weekly_data.csv'
    QUARTERLY_EARNINGS_FILE = './data/quarterly_earnings.csv'
    CASH_FLOW_FILE = './data/cash_flow.csv'
    NEWS_SENTIMENT_FILE = './data/news_sentiment.csv'
    MONGODB_DATABASE = 'StockInfoDB'

    def __init__(self):
        with open("secrets.yaml", "r") as file:
            config = yaml.safe_load(file)
        # self.MONGODB_URI = config.get("MONGO_URI", 'mongodb://localhost:27017/')
        self.mongo_connection_string = config['mongo']['connection_str']
        self.nasdaq_data_fetcher = NasdaqDataFetcher()
        self.alpha_vantage = AlphaVantageAPI()
        self.mongo_handler = MongoDBHandler(self.MONGODB_DATABASE, self.mongo_connection_string)

    def collect_nasdaq_data(self):
        nasdaq_url = "https://en.wikipedia.org/wiki/Nasdaq-100"
        data = self.nasdaq_data_fetcher.fetch_data(nasdaq_url)
        if data:
            columns = ['Company', 'Ticker', 'GICS Sector', 'GICS Sub-Industry']
            df = pd.DataFrame(data, columns=columns)
            df.to_csv(self.nasdaq_company_list_file, index=False)
            print("Finished collecting NASDAQ data.")

    def fetch_and_save_alpha_data(self):
        print("Fetching and saving AlphaVantage data...")
        nasdaq_data = pd.read_csv(self.nasdaq_company_list_file)
        tickers = nasdaq_data['Ticker'].tolist()
        symbols = tickers
        start_date, end_date = '2021-01-01', '2023-12-31'
        
        print("Fetching company overview data...")
        company_overviews = [self.alpha_vantage.fetch_company_overview(symbol) for symbol in symbols]
        pd.DataFrame(company_overviews).to_csv(self.COMPANY_OVERVIEW_FILE, index=False)
        print("Finished fetching company overview data.")
        
        print("Fetching weekly series data...")
        self.alpha_vantage.save_to_csv(self.alpha_vantage.fetch_time_series_weekly, symbols, self.STOCK_WEEKLY_DATA_FILE, start_date, end_date)
        print("Finished fetching weekly series data.")
        
        print("Fetching quarterly earnings data...")
        self.alpha_vantage.save_to_csv(self.alpha_vantage.fetch_quarterly_earnings, symbols, self.QUARTERLY_EARNINGS_FILE, start_date, end_date)
        print("Finished fetching quarterly earnings data.")
        
        print("Fetching quarterly cash flow data...")
        self.alpha_vantage.save_to_csv(self.alpha_vantage.fetch_quarterly_cash_flow, symbols, self.CASH_FLOW_FILE, start_date, end_date)
        print("Finished fetching quarterly cash flow data.")
        
        print("Fetching news sentiment data...")
        self.alpha_vantage.analyze_sentiment(symbols, self.NEWS_SENTIMENT_FILE)
        print("Finished fetching news sentiment data.")
        
        print("Finished fetching and saving all AlphaVantage data.")

    def save_data_to_mongo(self):
        print("Saving data to MongoDB...")
        files_and_collections = {
            self.COMPANY_OVERVIEW_FILE: 'company_overview',
            self.STOCK_WEEKLY_DATA_FILE: 'stock_weekly_data',
            self.QUARTERLY_EARNINGS_FILE: 'quarterly_earnings',
            self.CASH_FLOW_FILE: 'cash_flow',
            self.NEWS_SENTIMENT_FILE: 'news_sentiment'
        }
        for csv_file, collection_name in files_and_collections.items():
            print(f"Saving {collection_name} data to MongoDB...")
            self.mongo_handler.save_csv_to_collection(csv_file, collection_name)
        self.mongo_handler.disconnect()
        print("Finished saving all data to MongoDB.")

if __name__ == "__main__":
    print("Starting data collection...")
    collector = StockDataCollector()
    collector.collect_nasdaq_data()
    collector.fetch_and_save_alpha_data()
    collector.save_data_to_mongo()
    print("Data collection process completed.")
