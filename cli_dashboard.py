# FIRA Local Terminal Interface
import time

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

from knowledge_base import query_knowledge_base
from feed_handler import fetch_ticker_metrics
from investor_profile import load_investor_profiles
from consensus_engine import synthesize_consensus
from audit_logger import log_audit_metrics

def run_fira_scenario(scenario_idx: int, ticker: str, profile_key: str, fault_mode: str = None):
    profiles = load_investor_profiles()
    profile = profiles[profile_key]
    
    if HAS_RICH:
        console = Console()
        console.print(f"\n[bold green]⚡ SCENARIO {scenario_idx}: Processing {ticker} for {profile.investor_name}...[/bold green]")
        if fault_mode:
            console.print(f"[bold yellow]⚠️ INJECTING FAULT STATE: {fault_mode}[/bold yellow]")
    else:
        print(f"\n=== SCENARIO {scenario_idx}: Processing {ticker} for {profile.investor_name} ===")
        if fault_mode:
            print(f"!!! FAULT STATE: {fault_mode} !!!")
            
    start_t = time.time()
    
    # 1. Fetch live metrics
    metrics = fetch_ticker_metrics(ticker)
    
    # 2. Local semantic context query
    contexts = query_knowledge_base(ticker, f"leverage valuation capital structures for {ticker}")
    
    # 3. Process consensus engine
    consensus = synthesize_consensus(ticker, metrics, contexts, profile, fault_mode)
    
    # 4. Telemetry audit
    latency_ms = (time.time() - start_t) * 1000
    telemetry = log_audit_metrics(
        ticker=ticker,
        verdict=consensus["verdict"],
        score=consensus["consensus_score"],
        profile_class=profile.risk_class,
        execution_time_ms=latency_ms,
        has_vol_anomaly=("CATALYTIC_MOMENTUM_BOOST" in consensus["overlays"]),
        portfolio_mix=profile.asset_mix
    )

    if HAS_RICH:
        # Grounding table
        rag_table = Table(title="📖 SEBI Grounding Reference Nodes", border_style="dim")
        rag_table.add_column("Citation Reference", style="cyan")
        rag_table.add_column("Verified Filing Segment", style="italic")
        for ctx in contexts:
            node_id, text = ctx.split("]", 1)
            rag_table.add_row(node_id + "]", text.strip()[:100] + "...")
        console.print(rag_table)

        # Analyst results
        analyst_table = Table(title="🕵️ Analyst Thread Voting Status", border_style="green")
        analyst_table.add_column("Expert Thread", style="bold green")
        analyst_table.add_column("Vote", style="bold")
        analyst_table.add_column("Raw Score", justify="right")
        analyst_table.add_column("Internal Speed", justify="right")
        for analyst in consensus["analysts"]:
            v_col = "green" if analyst["rating"] == "BUY" else "red" if analyst["rating"] == "SELL" else "yellow"
            analyst_table.add_row(
                analyst["analyst_name"],
                f"[{v_col}]{analyst['rating']}[/{v_col}]",
                f"{analyst['score']:.2f}",
                f"{analyst['latency_ms']} ms"
            )
        console.print(analyst_table)

        # Consensus Synthesis
        v_col = "bold green" if consensus["verdict"] == "BUY" else "bold red" if consensus["verdict"] == "SELL" else "bold yellow"
        summary_panel = Panel(
            f"[bold]Consensus Verdict:[/bold] [{v_col}]{consensus['verdict']}[/{v_col}] (Weighted Score: {consensus['consensus_score']:.2f})\n"
            f"[bold]Consensus Reliability:[/bold] {consensus['reliability']*100:.0f}%\n"
            f"[bold]Active Structural Overlays:[/bold] {', '.join(consensus['overlays']) if consensus['overlays'] else 'None'}\n\n"
            f"[bold]Justification Details:[/bold] {consensus['logic']}",
            title="Consensus Synthesis Output",
            border_style="green" if consensus["verdict"] == "BUY" else "red" if consensus["verdict"] == "SELL" else "yellow"
        )
        console.print(summary_panel)
    else:
        print("\n--- SEBI Grounding Reference Nodes ---")
        for ctx in contexts:
            print("  " + ctx[:120] + "...")
        print("\n--- Analyst Thread Voting Status ---")
        for analyst in consensus["analysts"]:
            print(f"  * {analyst['analyst_name']}: Vote={analyst['rating']}, Score={analyst['score']:.2f}, Speed={analyst['latency_ms']} ms")
        print("\n--- Consensus Synthesis Output ---")
        print(f"  Verdict: {consensus['verdict']} (Score: {consensus['consensus_score']:.2f})")
        print(f"  Reliability: {consensus['reliability']*100:.0f}%")
        print(f"  Overlays Applied: {', '.join(consensus['overlays']) if consensus['overlays'] else 'None'}")
        print(f"  Rational justification: {consensus['logic']}")
        print(f"\nTelemetry Latency: {latency_ms:.2f} ms | Accuracy: {telemetry['accuracy_score']*100:.0f}%")
        print("="*80)

def main():
    if HAS_RICH:
        Console().print(Panel("[bold]FIRA (FINANCIAL INTELLIGENCE & RISK ADVISOR)[/bold]\nMulti-Agent Retail Investor Decision Infrastructure Demo", border_style="green"))
    else:
        print("="*80)
        print("          FIRA (FINANCIAL INTELLIGENCE & RISK ADVISOR) TERMINAL")
        print("="*80)
        
    # Scenario 1: Rohan Mehta (Risk-Averse) checking high leverage HDFC Bank
    run_fira_scenario(1, "HDFCBANK", "ROHAN")
    
    # Scenario 2: Ananya Sen (Growth-Seeking) checking high leverage HDFC Bank (volume booster trips)
    run_fira_scenario(2, "HDFCBANK", "ANANYA")
    
    # Scenario 3: Rohan Mehta (Risk-Averse) checking low leverage, high-margin TCS
    run_fira_scenario(3, "TCS", "ROHAN")
    
    # Scenario 4: Ananya Sen (Growth-Seeking) evaluating ITC with a simulated Sentiment API crash
    run_fira_scenario(4, "ITC", "ANANYA", "SENTIMENT_DOWN")

if __name__ == "__main__":
    main()
