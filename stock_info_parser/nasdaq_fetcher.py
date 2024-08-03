import requests
from bs4 import BeautifulSoup

class NasdaqDataFetcher:
    
    def fetch_data(self, url):
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
            return None
        soup = BeautifulSoup(response.text, 'html.parser')
        return self._parse_table(soup)
    
    def _parse_table(self, soup):
        table = soup.find('table', {'id': 'constituents'})
        if table is None:
            print("Table with id 'constituents' not found.")
            return None
        rows = []
        for tr in table.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) >= 4:
                row = [td.text.strip() for td in tds[:4]]
                rows.append(row)
        return rows

