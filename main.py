from src.webscrapping import Webscraper
from src.converter import CurrencyConverter
import streamlit as st

st.title("Welcome to CurrencyHub!")
st.image("https://cdn.corporatefinanceinstitute.com/assets/foreign-exchange-1024x684.jpeg")

scraper = Webscraper("https://www.cursbnr.ro/")
rates = scraper.get_currency_data()
converter = CurrencyConverter(rates)

from_currency = st.selectbox('From which currency', ('RON', 'USD', 'EUR', 'GBP', 'CHF', 'BGN', 'HUF'))
to_currency = st.selectbox('To which currency', ('EUR', 'USD', 'RON', 'GBP', 'CHF', 'BGN', 'HUF'))
amount = st.text_input('Enter the amount here: ')

st.sidebar.title("About CurrencyHub")
st.sidebar.info(
    """
    CurrencyHub is a simple currency converter application that uses live exchange rates.
    Select your currencies, enter the amount, and get the converted value instantly!
    """
)

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
