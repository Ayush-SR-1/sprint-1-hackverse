# Investor Profiling Module for FIRA
from pydantic import BaseModel

class InvestorProfile(BaseModel):
    investor_name: str
    risk_class: str # RISK_AVERSE or GROWTH_SEEKING
    valuation_cap_pe: float
    debt_ceiling: float
    asset_mix: dict

def load_investor_profiles() -> dict:
    return {
        "ROHAN": InvestorProfile(
            investor_name="Rohan Mehta (Risk-Averse)",
            risk_class="RISK_AVERSE",
            valuation_cap_pe=22.0,
            debt_ceiling=0.75, # Strict debt-to-equity limit!
            asset_mix={"TCS": 50, "HDFCBANK": 10, "LIQUID_CASH": 40}
        ),
        "ANANYA": InvestorProfile(
            investor_name="Ananya Sen (Growth-Seeking)",
            risk_class="GROWTH_SEEKING",
            valuation_cap_pe=65.0,
            debt_ceiling=1.80, # More tolerant of leverage
            asset_mix={"TCS": 20, "HDFCBANK": 40, "ITC": 40}
        )
    }
