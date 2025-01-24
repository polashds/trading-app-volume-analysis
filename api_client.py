import requests
from config import FINNHUB_API_KEY
from logging_config import logger


def fetch_stock_data(symbol):
    url = f"https://finnhub.io/api/v1/quote?symbol={symbol}&token={FINNHUB_API_KEY}"
    try: 
        response = requests.get(url)
        response.raise_for_status() #raise an HTTPError if the response was unsuccessful
        
        data = response.json()
        logger.info(f"Fetched data for {symbol} : {data}")
        return {
            "symbol": symbol,
            "price" : data["c"],
            "volume": data["v"]
        }
        
    except requests.exceptions.RequestException as e:
        logger.error(f"Error fetching data for {symbol}: {e}")
        return None