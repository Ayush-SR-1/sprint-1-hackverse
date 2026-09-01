# Multi-Agent Consensus Orchestrator for FIRA
import concurrent.futures
from analysts import run_fundamental_analyst, run_quantitative_analyst, run_sentiment_analyst
from investor_profile import InvestorProfile

def synthesize_consensus(ticker: str, metrics: dict, contexts: list, profile: InvestorProfile, simulate_fault: str = None) -> dict:
    """Runs specialized analysts in parallel, applies risk overlays, and re-normalizes weights on failures."""
    analyst_outputs = []
    
    run_fund = simulate_fault != "FUNDAMENTALS_DOWN"
    run_quant = simulate_fault != "TECHNICAL_DOWN"
    run_sent = simulate_fault != "SENTIMENT_DOWN"

    # Parallel threading execution
    with concurrent.futures.ThreadPoolExecutor(max_workers=3) as executor:
        futures = {}
        if run_fund:
            futures["fundamentals"] = executor.submit(run_fundamental_analyst, ticker, metrics, contexts)
        if run_quant:
            futures["quantitative"] = executor.submit(run_quantitative_analyst, ticker, metrics)
        if run_sent:
            futures["sentiment"] = executor.submit(run_sentiment_analyst, ticker, contexts)

        for key, fut in futures.items():
            try:
                analyst_outputs.append(fut.result())
            except Exception:
                pass # Gracefully degrade on thread failure

    if not analyst_outputs:
        return {
            "verdict": "HOLD",
            "consensus_score": 0.0,
            "reliability": 0.0,
            "logic": "Critical System Fault: All analyst threads timed out. Consolidated rating defaulted to HOLD to shield capital.",
            "overlays": ["SYSTEM_OUTAGE_FALLBACK"],
            "analysts": []
        }

    # Weight settings based on investor profile
    if profile.risk_class == "RISK_AVERSE":
        weights = {"Fundamental Auditor": 0.55, "Quantitative Modeler": 0.20, "Sentiment Scraper": 0.25}
    else:
        weights = {"Fundamental Auditor": 0.15, "Quantitative Modeler": 0.40, "Sentiment Scraper": 0.45}

    # Re-normalize weights in case of degraded dependency state
    active_weights = {a.analyst_name: weights.get(a.analyst_name, 0.33) for a in analyst_outputs}
    total_active_w = sum(active_weights.values())
    normalized_w = {name: w / total_active_w for name, w in active_weights.items()}

    # Compute consensus metrics
    weighted_score = sum(a.score * normalized_w[a.analyst_name] for a in analyst_outputs)
    avg_confidence = sum(a.confidence for a in analyst_outputs) / len(analyst_outputs)

    final_score = weighted_score
    overlays_applied = []
    logic_notes = []

    # 1. Risk-Averse Debt Shield
    debt = metrics.get("debt_to_equity", 0.0)
    if profile.risk_class == "RISK_AVERSE" and debt > profile.debt_ceiling:
        overlays_applied.append("LEVERAGE_CEILING_SHIELD")
        final_score = -0.15 # Override to conservative HOLD rating
        logic_notes.append(
            f"[LEVERAGE SHIELD TRIP] Ticker debt-to-equity of {debt:.2f} violates Rohan's conservative safety ceiling of {profile.debt_ceiling:.2f}. "
            "Rating overrode to HOLD to mitigate systemic balance sheet leverage."
        )

    # 2. Growth-Seeking Momentum Booster
    vol = metrics.get("volume_24h", 1)
    avg_vol = metrics.get("avg_volume_20d", 1)
    vol_multiplier = vol / avg_vol
    if profile.risk_class == "GROWTH_SEEKING" and vol_multiplier > 1.5:
        overlays_applied.append("CATALYTIC_MOMENTUM_BOOST")
        final_score = min(1.0, final_score + 0.20) # Apply 20% score boost
        logic_notes.append(
            f"[MOMENTUM BOOSTER ACTIVE] Ticker volume is {((vol_multiplier)-1)*100:.1f}% above historical averages. "
            "Scoring weight boosted by +20% due to strong catalyst indicators."
        )

    # Translate score to verdict label
    if final_score >= 0.25:
        verdict = "BUY"
    elif final_score <= -0.25:
        verdict = "SELL"
    else:
        verdict = "HOLD"

    base_justifications = "; ".join([f"{a.analyst_name} voted {a.rating} ({a.justification})" for a in analyst_outputs])
    full_logic = " ".join(logic_notes) + " Consensus Reasoning: " + base_justifications

    return {
        "verdict": verdict,
        "consensus_score": round(final_score, 2),
        "reliability": round(avg_confidence, 2),
        "logic": full_logic,
        "overlays": overlays_applied,
        "analysts": [a.model_dump() for a in analyst_outputs]
    }
