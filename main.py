"""Main module"""
import streamlit as st
from src.webscrapping import Webscraper
from src.converter import CurrencyConverter

# Set up the Streamlit interface
st.title("Welcome to CurrencyHub!")
st.image("https://cdn.corporatefinanceinstitute.com/assets/foreign-exchange-1024x684.jpeg")


# Initialize the web scraper to fetch currency data
scraper = Webscraper("https://www.cursbnr.ro/")
rates = scraper.get_currency_data()

# Initialize the currency converter with the fetched rates
converter = CurrencyConverter(rates)

# User input for currency conversion
currency_values = ('RON', 'USD', 'EUR', 'GBP', 'CHF', 'BGN', 'HUF')
from_currency = st.selectbox('From which currency', currency_values)
to_currency = st.selectbox('To which currency', currency_values)
amount = st.text_input('Enter the amount here: ')


# Sidebar information
st.sidebar.title("About CurrencyHub")
st.sidebar.info(
    """
    CurrencyHub is a simple currency converter application that uses live exchange rates.
    Select your currencies, enter the amount, and get the converted value instantly!
    """
)

# Handle the conversion when the submit button is clicked
if st.button('Submit'):
    if not amount:
        st.error("Please enter an amount")
    else:
        try:
            amount_float = float(amount)
            result = converter.convert(amount_float, from_currency, to_currency)
            st.write(f"{amount} {from_currency} = {result} {to_currency}")
        except ValueError:
            st.error("Please enter a valid number")
        except KeyError:
            st.error("Selected currency not available in the data")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
