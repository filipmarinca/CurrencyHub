"""Web Scraping Module"""
from typing import Dict
import requests
from bs4 import BeautifulSoup


class Webscraper:
    """
    Web scraper for fetching live currency exchange rates from BNR (Romanian National Bank).
    """
    
    def __init__(self, url: str):
        """
        Initialize the Webscraper with a URL.
        
        Args:
            url: The URL to scrape currency data from
            
        Raises:
            requests.RequestException: If the request fails
            ValueError: If the currency table is not found
        """
        self.url = url
        try:
            self.response = requests.get(self.url, timeout=10)
            self.response.raise_for_status()
        except requests.RequestException as e:
            raise requests.RequestException(f"Failed to fetch data from {url}: {str(e)}")
        
        self.soup = BeautifulSoup(self.response.content, "lxml")
        self.table = self._get_table_with_currencies()
    
    def _get_table_with_currencies(self):
        """
        Extract the table containing currency data from the parsed HTML.
        
        Returns:
            The tbody element of the currency table
            
        Raises:
            ValueError: If the currency table is not found
        """
        table = self.soup.find("table", {"id": "table-currencies"})
        if not table or not table.tbody:
            raise ValueError("Currency table not found on the page")
        return table.tbody
    
    def get_currency_data(self) -> Dict[str, float]:
        """
        Parse the currency table and return exchange rates.
        
        Returns:
            Dictionary mapping currency codes to their exchange rates relative to RON
            
        Raises:
            ValueError: If table parsing fails or data is invalid
        """
        currency_info = {}
        rows = self.table.find_all("tr")
        
        if not rows:
            raise ValueError("No currency data rows found")
        
        for row in rows:
            try:
                data = row.find_all("td")
                if len(data) < 3:
                    continue
                    
                currency = data[0].text.strip()
                value_text = data[2].text.strip().replace(',', '.')
                value = float(value_text)
                
                if value > 0:  # Only include positive rates
                    currency_info[currency] = value
                    
            except (ValueError, IndexError) as e:
                # Skip rows that can't be parsed
                continue
        
        if not currency_info:
            raise ValueError("No valid currency data could be extracted")
            
        return currency_info
