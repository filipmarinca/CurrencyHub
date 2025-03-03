"""Web Scraping Module"""
import requests
from bs4 import BeautifulSoup

class Webscraper:
    """Webscrapper class"""
    def __init__(self, url):
        self.url = url
        self.response = requests.get(self.url, timeout=10)
        self.soup = BeautifulSoup(self.response.content, "lxml")
        self.table = self._get_table_with_currencies()
    # Initializes the Webscraper with a specified URL and fetches the HTML content.
    def _get_table_with_currencies(self):
        return self.soup.find("table",  {"id": "table-currencies"}).tbody
    # Extracts the table containing currency data from the parsed HTML.
    def get_currency_data(self):
        """Parses the currency table and returns a dictionary of currency exchange rates."""
        currency_info = {}
        rows = self.table.find_all("tr")
        for row in rows:
            data = row.find_all("td")
            currency = data[0].text
            value = float(data[2].text)
            currency_info[currency] = value
        return currency_info
