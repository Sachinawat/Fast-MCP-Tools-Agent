import random
from servers.config import logger

def get_stock_price(ticker: str):
    """
    Simulates fetching a stock price. 
    In production, you would use 'yfinance' or AlphaVantage API here.
    """
    logger.info(f"Fetching stock price for: {ticker}")
    
    # Mock Logic for Demo
    ticker = ticker.upper()
    mock_price = round(random.uniform(100, 500), 2)
    
    if ticker == "AAPL":
        return {"ticker": "AAPL", "price": 175.50, "currency": "USD"}
    elif ticker == "GOOGL":
        return {"ticker": "GOOGL", "price": 140.20, "currency": "USD"}
    
    # Default random for others
    return {"ticker": ticker, "price": mock_price, "currency": "USD", "note": "Simulated Data"}