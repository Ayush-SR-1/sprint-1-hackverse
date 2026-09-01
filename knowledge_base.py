# Local Ingestion and RAG Search Engine for FIRA
import re

DOCUMENTS = {
    "TCS": [
        "[Segment 1] SEBI Corporate Filing (Q1): TCS balance sheet reports a low debt-to-equity ratio of 0.12. Leverage risk remains extremely low, making it attractive for risk-averse allocation.",
        "[Segment 2] Earnings Transcript (August 2026): CFO stated, 'Our order book remains strong with $10.2B in TCV. Generative AI projects doubled QoQ, though margins faced salary headwinds.'",
        "[Segment 3] Market Insight: TCS continues to gain market share in the European financial services vertical despite global IT spending moderation."
    ],
    "HDFCBANK": [
        "[Segment 1] Corporate Disclosure: HDFC Bank reports a consolidated debt-to-equity ratio of 1.10. Leverage is standard for private commercial banks, though risk-averse investors may apply overlays.",
        "[Segment 2] Analyst Call: Executive Director noted, 'Net interest margin stabilized at 4.1%. Loan growth was driven primarily by retail mortgages, which expanded by 18% YoY.'",
        "[Segment 3] Regulatory Update: Basel III capital adequacy ratio remains healthy at 16.5%, comfortably above the minimum regulatory requirements."
    ],
    "ITC": [
        "[Segment 1] Corporate Filing: ITC reports zero long-term bank debt (Debt-to-Equity of 0.00). Cash flow generation from the core FMCG and paperboards divisions remains robust.",
        "[Segment 2] Earnings Transcript: Chairman commented, 'Hotel segment demerger is on track for completion by Q3. Non-cigarette FMCG margins expanded by 120 basis points, driven by premiumization.'",
        "[Segment 3] Industry Report: Agricultural segment exports faced headwinds due to regulatory trade restrictions, offset by a recovery in the paperboard sector."
    ]
}

def query_knowledge_base(ticker: str, query: str) -> list:
    """Simulated semantic search context retrieval."""
    ticker = ticker.upper()
    if ticker not in DOCUMENTS:
        return []
    
    keywords = re.findall(r'\w+', query.lower())
    chunks = DOCUMENTS[ticker]
    scored = []
    
    for i, chunk in enumerate(chunks):
        score = sum(1 for kw in keywords if kw in chunk.lower())
        scored.append((score, i, chunk))
        
    scored.sort(reverse=True)
    return [f"[{ticker} Ref {idx+1}] {text}" for score, idx, text in scored[:2]]
