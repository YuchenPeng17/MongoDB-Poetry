import yaml
import requests
import pandas as pd


class AlphaVantageAPI:
    BASE_URL = "https://www.alphavantage.co/query"

    def __init__(self):
        with open("secrets.yaml", "r") as file:
            config = yaml.safe_load(file)
        self.api_key = config['alpha']['api_key']

    def fetch_data_from_url(self, function, symbol):
        url = f'https://www.alphavantage.co/query?function={function}&symbol={symbol}&apikey={self.api_key}'
        return requests.get(url).json()
    
    def filter_dataframe(self, df, symbol, start_date, end_date, date_col):
        # 1. Create a new column for company symbol
        SYMBOL_COL = 'symbol'
        df[SYMBOL_COL] = symbol
        # 2. Reorder the symbol column to the front
        cols = [SYMBOL_COL] + [col for col in df if col != SYMBOL_COL]
        df = df[cols]
        # 3. Filters the DataFrame to include only those rows where the date in date_col is within the timeFrame.
        return df[(df[date_col] >= start_date) & (df[date_col] <= end_date)]

    def fetch_company_overview(self, symbol):
        return self.fetch_data_from_url('OVERVIEW', symbol)

    def fetch_time_series_weekly(self, symbol, start_date, end_date):
        data = self.fetch_data_from_url('TIME_SERIES_WEEKLY', symbol)
        print(data)
        """
        Creates a pandas DataFrame from the JSON data under the key 'Weekly Time Series',
        then transposes it and reset the index's name to 'date'
        """
        df = pd.DataFrame(data['Weekly Time Series']).T
        WEEKLY_SERIES_DATE_COL = 'date'
        df = df.reset_index().rename(columns={'index': WEEKLY_SERIES_DATE_COL})
        # Filter the data based on the specified `start_date` and `end_date`
        return self.filter_dataframe(df, symbol, start_date, end_date, WEEKLY_SERIES_DATE_COL)

    def fetch_quarterly_earnings(self, symbol, start_date, end_date):
        date = self.fetch_data_from_url('EARNINGS', symbol)
        df = pd.DataFrame(date['quarterlyEarnings'])
        return self.filter_dataframe(df, symbol, start_date, end_date, 'fiscalDateEnding')

    def fetch_quarterly_cash_flow(self, symbol, start_date, end_date):
        data = self.fetch_data_from_url('CASH_FLOW', symbol)
        df = pd.DataFrame(data['quarterlyReports'])
        return self.filter_dataframe(df, symbol, start_date, end_date, 'fiscalDateEnding')

    def fetch_news_sentiment(self, symbol):
        return self.fetch_data_from_url('NEWS_SENTIMENT', symbol)

    def save_to_csv(self, processor_func, symbols, output_file, start_date, end_date):
        # Use specified function `processor_func` to process each symbol
        combined_df = pd.concat([processor_func(symbol, start_date, end_date) for symbol in symbols], ignore_index=True)
        combined_df.to_csv(output_file, index=False)

    def analyze_sentiment(self, symbols, output_file):
        all_data_frames = []

        for symbol in symbols:
            data = self.fetch_news_sentiment(symbol)
            rows = [{
                'ticket_number': ticker_info['ticker'],
                'relevance_score': ticker_info['relevance_score'],
                'sentiment_score': ticker_info['ticker_sentiment_score'],
                'sentiment_label': ticker_info['ticker_sentiment_label'],
                'title': item['title'],
                'time_published': item['time_published'],
                'summary': item['summary'],
                'url': item['url'],
            } for item in data['feed'] for ticker_info in item['ticker_sentiment']]
            
            all_data_frames.append(pd.DataFrame(rows))

        combined_df = pd.concat(all_data_frames, ignore_index=True)
        combined_df.to_csv(output_file, index=False)
