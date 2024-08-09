import requests
from bs4 import BeautifulSoup

class NasdaqDataFetcher:
    
    def fetch_data(self, url):
        # Check if we got the resposne
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None
        # If yes, use BeautifulSoup to parse the information in the URL
        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_table(soup)
    
    def _parse_table(self, soup):
        # Find the target information, table with id 'constituents' in this situaion
        table = soup.find('table', {'id': 'constituents'})
        if table is None:
            print("Table with id 'constituents' not found.")
            return None
        
        # Each row is exactly one line entry in the website
        # Company | Ticker | GJCS Sector | GICS Sub-Industry
        rows = []
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) >= 4:
                row = [td.text.strip() for td in tds[:4]]
                rows.append(row)
        return rows

