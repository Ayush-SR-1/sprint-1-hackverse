# Parallel Analyst Threads for FIRA
import time
from pydantic import BaseModel, Field

class AnalystOutput(BaseModel):
    analyst_name: str
    rating: str = Field(description="BUY, SELL, or HOLD")
    score: float = Field(description="Score from -1.0 to +1.0")
    confidence: float = Field(description="Confidence from 0.0 to 1.0")
    justification: str
    latency_ms: float

def run_fundamental_analyst(ticker: str, metrics: dict, contexts: list) -> AnalystOutput:
    """Evaluates balance sheet health, leverage levels, and capital allocation."""
    start = time.time()
    time.sleep(0.08) # Network simulation
    
    debt = metrics.get("debt_to_equity", 0.5)
    context_str = " ".join(contexts)
    
    if "debt-to-equity ratio of 1.10" in context_str:
        justification = "Filing flags moderate balance sheet leverage of 1.10. While manageable in the private banking sector, standard overlays apply for risk-averse allocators."
        rating = "HOLD"
        score = -0.15
    elif "Debt-to-Equity of 0.00" in context_str:
        justification = "Pristine capital structure with zero long-term bank debt. Capital allocation supports hotel demerger and dividends."
        rating = "BUY"
        score = 0.90
    else:
        if debt > 1.0:
            rating = "HOLD"
            score = -0.20
            justification = f"Stock carries leverage above safety limits ({debt:.2f}). Neutral ratings enforced."
        else:
            rating = "BUY"
            score = 0.55
            justification = f"Balanced debt-to-equity ratio of {debt:.2f} with healthy liquidity buffers."

    return AnalystOutput(
        analyst_name="Fundamental Auditor",
        rating=rating,
        score=score,
        confidence=0.88,
        justification=justification,
        latency_ms=round((time.time() - start) * 1000, 2)
    )

def run_quantitative_analyst(ticker: str, metrics: dict) -> AnalystOutput:
    """Evaluates moving averages, volume thresholds, and RSI momentum."""
    start = time.time()
    time.sleep(0.05)
    
    price = metrics.get("price", 100)
    rsi = metrics.get("rsi", 50)
    dma_50 = metrics.get("dma_50", price)
    dma_200 = metrics.get("dma_200", price)
    vol = metrics.get("volume_24h", 1)
    avg_vol = metrics.get("avg_volume_20d", 1)
    
    vol_surge = (vol / avg_vol) > 1.4
    bullish_trend = dma_50 > dma_200 and price > dma_50
    
    if rsi > 70:
        rating = "SELL"
        score = -0.65
        justification = f"Ticker is technically overextended with an overbought RSI of {rsi:.1f}. High risk of immediate mean reversion."
    elif bullish_trend or vol_surge:
        rating = "BUY"
        score = 0.80
        justification = f"Bullish trend confirmed (50-DMA > 200-DMA). High volume anomaly of +{((vol/avg_vol)-1)*100:.1f}% indicates institutional demand."
    else:
        rating = "HOLD"
        score = 0.05
        justification = f"RSI in neutral range ({rsi:.1f}). Consolidation continues with stable average trading volume."

    return AnalystOutput(
        analyst_name="Quantitative Modeler",
        rating=rating,
        score=score,
        confidence=0.92,
        justification=justification,
        latency_ms=round((time.time() - start) * 1000, 2)
    )

def run_sentiment_analyst(ticker: str, contexts: list) -> AnalystOutput:
    """Parses corporate briefings, earnings reports, and sector outlooks."""
    start = time.time()
    time.sleep(0.12)
    
    context_str = " ".join(contexts).lower()
    
    if "generative ai projects" in context_str:
        rating = "BUY"
        score = 0.70
        justification = "Bullish executive tone surrounding GenAI pipeline doubling QoQ. Healthy order book at $10.2B TCV."
    elif "hotel segment demerger" in context_str:
        rating = "BUY"
        score = 0.65
        justification = "Positive shareholder sentiment on hospitality demerger unlocking consumer value. FMCG premiumization maintains pricing power."
    else:
        rating = "HOLD"
        score = 0.00
        justification = "Neutral sentiment signals. Executive guidelines indicate conservative strategic roadmap for the coming fiscal quarters."

    return AnalystOutput(
        analyst_name="Sentiment Scraper",
        rating=rating,
        score=score,
        confidence=0.78,
        justification=justification,
        latency_ms=round((time.time() - start) * 1000, 2)
    )
