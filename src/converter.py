class CurrencyConverter:
    def __init__(self, currency_data):
        self.currency_data = currency_data

    def convert(self, amount, from_currency, to_currency):
        # This convert everything to RON
        if from_currency == "RON":
            rate_from = 1
        else:
            rate_from = self.currency_data[from_currency]
        if to_currency == "RON":
            rate_to = 1
        else:
            rate_to = self.currency_data[to_currency]
        # Conversion formula
        result = (amount * rate_from) / rate_to
        return round(result, 2)