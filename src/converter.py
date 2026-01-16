"""CurrencyConverter module"""
from typing import Dict


class CurrencyConverter:
    """
    Currency converter that converts amounts between different currencies.
    
    All exchange rates are relative to RON (Romanian Leu).
    """
    
    def __init__(self, currency_data: Dict[str, float]):
        """
        Initialize the CurrencyConverter with exchange rates.
        
        Args:
            currency_data: Dictionary mapping currency codes to their exchange rates relative to RON
        """
        self.currency_data = currency_data

    def convert(self, amount: float, from_currency: str, to_currency: str) -> float:
        """
        Convert an amount from one currency to another.
        
        Args:
            amount: The amount to convert
            from_currency: Source currency code (e.g., 'USD', 'EUR')
            to_currency: Target currency code (e.g., 'RON', 'GBP')
            
        Returns:
            The converted amount rounded to 2 decimal places
            
        Raises:
            ValueError: If amount is negative or zero
            KeyError: If currency code is not found in the rates
        """
        if amount <= 0:
            raise ValueError("Amount must be positive")
        
        # Get exchange rate for source currency (relative to RON)
        if from_currency == "RON":
            rate_from = 1.0
        else:
            if from_currency not in self.currency_data:
                raise KeyError(f"Currency {from_currency} not found in exchange rates")
            rate_from = self.currency_data[from_currency]
        
        # Get exchange rate for target currency (relative to RON)
        if to_currency == "RON":
            rate_to = 1.0
        else:
            if to_currency not in self.currency_data:
                raise KeyError(f"Currency {to_currency} not found in exchange rates")
            rate_to = self.currency_data[to_currency]
        
        # Calculate the converted amount
        # First convert to RON, then to target currency
        result = (amount * rate_from) / rate_to
        return round(result, 2)
    
    def get_exchange_rate(self, from_currency: str, to_currency: str) -> float:
        """
        Get the exchange rate between two currencies.
        
        Args:
            from_currency: Source currency code
            to_currency: Target currency code
            
        Returns:
            The exchange rate from source to target currency
        """
        return self.convert(1.0, from_currency, to_currency)
