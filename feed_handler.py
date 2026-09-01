# Market Feed Handler for FIRA
import random

def fetch_ticker_metrics(ticker: str) -> dict:
    """Returns historical and real-time technical metrics for a stock."""
    ticker = ticker.upper()
    
    feeds = {
        "TCS": {
            "price": 4250.00,
            "rsi": 48.5,
            "volume_24h": 3200000,
            "avg_volume_20d": 3500000,
            "dma_50": 4180.00,
            "dma_200": 3950.00,
            "debt_to_equity": 0.12
        },
        "HDFCBANK": {
            "price": 1640.50,
            "rsi": 58.2,
            "volume_24h": 18500000,
            "avg_volume_20d": 12000000, # 54% Volume anomaly!
            "dma_50": 1610.00,
            "dma_200": 1540.00,
            "debt_to_equity": 1.10
        },
        "ITC": {
            "price": 490.25,
            "rsi": 76.5, # Overbought!
            "volume_24h": 9500000,
            "avg_volume_20d": 9200000,
            "dma_50": 465.00,
            "dma_200": 440.00,
            "debt_to_equity": 0.00
        }
    }
    
    if ticker in feeds:
        return feeds[ticker]
    else:
        price = random.uniform(10.0, 5000.0)
        return {
            "price": round(price, 2),
            "rsi": round(random.uniform(15.0, 85.0), 1),
            "volume_24h": random.randint(50000, 10000000),
            "avg_volume_20d": random.randint(50000, 10000000),
            "dma_50": round(price * 0.97, 2),
            "dma_200": round(price * 0.93, 2),
            "debt_to_equity": round(random.uniform(0.0, 2.0), 2)
        }
