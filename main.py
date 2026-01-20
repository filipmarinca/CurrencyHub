"""Exchange rate app CurrencyHub"""
import streamlit as st
from datetime import datetime
from src.webscrapping import Webscraper
from src.converter import CurrencyConverter

# Page configuration
st.set_page_config(
    page_title="CurrencyHub - Live Currency Converter",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful design
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 15px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .main-header h1 {
        font-size: 3rem;
        margin: 0;
        font-weight: 700;
    }
    
    .main-header p {
        font-size: 1.2rem;
        margin: 0.5rem 0 0 0;
        opacity: 0.9;
    }
    
    .currency-card {
        background: white;
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
        margin: 1rem 0;
    }
    
    .result-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 15px;
        text-align: center;
        font-size: 1.8rem;
        font-weight: 600;
        margin: 2rem 0;
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
        animation: fadeIn 0.5s;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-10px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    .rate-info {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 4px solid #667eea;
    }
    
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 10px;
        transition: all 0.3s;
        box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .currency-flag {
        font-size: 2rem;
        margin-right: 0.5rem;
    }
    
    .swap-button {
        text-align: center;
        margin: 1rem 0;
    }
    
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #667eea;
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>💱 CurrencyHub</h1>
    <p>Convert currencies with live exchange rates</p>
</div>
""", unsafe_allow_html=True)

# Initialize the web scraper with caching
@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_currency_data():
    """Fetch currency data with caching"""
    try:
        scraper = Webscraper("https://www.cursbnr.ro/")
        return scraper.get_currency_data()
    except Exception as e:
        # Fallback to mock data for demo purposes
        st.warning(f"Using demo data. Could not fetch live rates: {str(e)[:100]}")
        return {
            'USD': 4.9234,
            'EUR': 4.9756,
            'GBP': 5.8123,
            'CHF': 5.6234,
            'BGN': 2.5431,
            'HUF': 0.0135
        }

# Fetch rates
with st.spinner('Loading latest exchange rates...'):
    rates = fetch_currency_data()

if not rates:
    st.error("Unable to load currency data. Please check your internet connection.")
    st.stop()

# Initialize converter
converter = CurrencyConverter(rates)

# Currency emoji mapping
currency_flags = {
    'RON': '🇷🇴',
    'USD': '🇺🇸',
    'EUR': '🇪🇺',
    'GBP': '🇬🇧',
    'CHF': '🇨🇭',
    'BGN': '🇧🇬',
    'HUF': '🇭🇺'
}

# Available currencies
currency_values = ('RON', 'USD', 'EUR', 'GBP', 'CHF', 'BGN', 'HUF')

# Initialize session state for swap functionality
if 'from_curr' not in st.session_state:
    st.session_state.from_curr = 'RON'
if 'to_curr' not in st.session_state:
    st.session_state.to_curr = 'USD'

# Main content area
col1, col2 = st.columns([3, 2])

with col1:
    st.markdown("### 🔄 Currency Converter")
    
    # Create three columns for better layout
    input_col1, swap_col, input_col2 = st.columns([5, 1, 5])
    
    with input_col1:
        from_currency = st.selectbox(
            'From Currency',
            currency_values,
            index=currency_values.index(st.session_state.from_curr),
            format_func=lambda x: f"{currency_flags.get(x, '')} {x}",
            key='from_currency_select'
        )
        st.session_state.from_curr = from_currency
        
        amount = st.number_input(
            'Amount',
            min_value=0.01,
            value=100.0,
            step=1.0,
            format="%.2f"
        )
    
    with swap_col:
        st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
        if st.button("⇄", help="Swap currencies"):
            # Swap the currencies
            st.session_state.from_curr, st.session_state.to_curr = st.session_state.to_curr, st.session_state.from_curr
            st.rerun()
    
    with input_col2:
        to_currency = st.selectbox(
            'To Currency',
            currency_values,
            index=currency_values.index(st.session_state.to_curr),
            format_func=lambda x: f"{currency_flags.get(x, '')} {x}",
            key='to_currency_select'
        )
        st.session_state.to_curr = to_currency
        st.markdown("<div style='margin-top: 2.4rem;'></div>", unsafe_allow_html=True)
    
    # Convert button
    if st.button('🔄 Convert', type="primary"):
        try:
            if amount <= 0:
                st.error("⚠️ Please enter a positive amount")
            elif from_currency == to_currency:
                st.warning("⚠️ Source and destination currencies are the same")
            else:
                result = converter.convert(amount, from_currency, to_currency)
                
                # Display result with animation
                st.markdown(f"""
                <div class="result-box">
                    {currency_flags.get(from_currency, '')} {amount:,.2f} {from_currency} = 
                    {currency_flags.get(to_currency, '')} {result:,.2f} {to_currency}
                </div>
                """, unsafe_allow_html=True)
                
                # Show exchange rate
                rate = result / amount
                st.markdown(f"""
                <div class="rate-info">
                    <strong>Exchange Rate:</strong> 1 {from_currency} = {rate:.4f} {to_currency}
                </div>
                """, unsafe_allow_html=True)
                
        except KeyError:
            st.error("❌ Selected currency not available in the data")
        except Exception as e:
            st.error(f"❌ An error occurred: {str(e)}")
    
    # Popular conversions
    st.markdown("### 🌟 Popular Conversions")
    popular_pairs = [
        ('USD', 'EUR'),
        ('EUR', 'RON'),
        ('GBP', 'USD'),
        ('USD', 'RON')
    ]
    
    cols = st.columns(2)
    for idx, (from_c, to_c) in enumerate(popular_pairs):
        with cols[idx % 2]:
            try:
                rate = converter.convert(1, from_c, to_c)
                st.metric(
                    label=f"{currency_flags.get(from_c, '')} {from_c} → {currency_flags.get(to_c, '')} {to_c}",
                    value=f"{rate:.4f}"
                )
            except Exception:
                # Skip currencies that can't be converted
                pass

with col2:
    st.markdown("### 📊 Available Rates")
    st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    
    # Display all available rates
    for currency, rate in sorted(rates.items()):
        flag = currency_flags.get(currency, '🏳️')
        st.markdown(f"""
        <div class="rate-info" style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-weight: 600;">{flag} {currency}</span>
            <span style="color: #667eea; font-weight: 700;">{rate:.4f} RON</span>
        </div>
        """, unsafe_allow_html=True)

# Sidebar
st.sidebar.markdown("### 📱 About CurrencyHub")
st.sidebar.info(
    """
    **CurrencyHub** is a modern currency converter with live exchange rates from 
    the Romanian National Bank (BNR).
    
    ✨ **Features:**
    - 💱 Real-time exchange rates
    - 🔄 Quick currency swap
    - 🌟 Popular currency pairs
    - 📊 Complete rate listings
    - 🎨 Beautiful, responsive design
    """
)

st.sidebar.markdown("### 💡 Tips")
st.sidebar.success(
    """
    - Rates are cached for 1 hour for better performance
    - Use the swap button (⇄) to quickly reverse currencies
    - All rates are relative to RON (Romanian Leu)
    """
)

st.sidebar.markdown("### 🔗 Links")
st.sidebar.markdown(
    """
    - [GitHub Repository](https://github.com/filipmarinca/CurrencyHub)
    - [Source: BNR](https://www.cursbnr.ro/)
    """
)
