# web_app.py - Zero-Dependency Financial Web Dashboard for FIRA (Emerald, Gold & Onyx Theme)
import http.server
import socketserver
import json
import urllib.parse
import webbrowser
import threading
import time

# Core Multi-Agent imports
from knowledge_base import query_knowledge_base
from feed_handler import fetch_ticker_metrics
from investor_profile import load_investor_profiles
from consensus_engine import synthesize_consensus
from audit_logger import log_audit_metrics

# Port configuration (Port 8090 to avoid conflicts with AFIS 8080)
PORT = 8090

class FIRARequestHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        # Suppress logging to console to keep terminal clean
        return

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        path = parsed_url.path

        if path == "/":
            self.send_response(200)
            self.send_header("Content-type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(HTML_CONTENT.encode("utf-8"))
        elif path == "/api/analyze":
            query = urllib.parse.parse_qs(parsed_url.query)
            stock = query.get("stock", ["TCS"])[0]
            profile_key = query.get("profile", ["ROHAN"])[0]
            failure_mode = query.get("failure", ["None"])[0]
            if failure_mode == "None":
                failure_mode = None

            # 1. Fetch live market statistics
            feed = fetch_ticker_metrics(stock)

            # 2. Local semantic search context nodes
            contexts = query_knowledge_base(stock, f"leverage valuation future growth metrics for {stock}")

            # 3. Parallel consensus execution
            start_t = time.time()
            consensus = synthesize_consensus(stock, feed, contexts, load_investor_profiles()[profile_key], failure_mode)
            duration_ms = (time.time() - start_t) * 1000

            # 4. Record telemetry
            telemetry = log_audit_metrics(
                ticker=stock,
                verdict=consensus["verdict"],
                score=consensus["consensus_score"],
                profile_class=load_investor_profiles()[profile_key].risk_class,
                execution_time_ms=duration_ms,
                has_vol_anomaly=("CATALYTIC_MOMENTUM_BOOST" in consensus["overlays"]),
                portfolio_mix=load_investor_profiles()[profile_key].asset_mix
            )

            # Package combined output
            response_data = {
                "consensus": consensus,
                "feed": feed,
                "contexts": contexts,
                "telemetry": telemetry,
                "active_profile": {
                    "name": load_investor_profiles()[profile_key].investor_name,
                    "risk": load_investor_profiles()[profile_key].risk_class,
                    "leverage_threshold": load_investor_profiles()[profile_key].debt_ceiling,
                    "valuation_cap": load_investor_profiles()[profile_key].valuation_cap_pe,
                    "portfolio": load_investor_profiles()[profile_key].asset_mix
                }
            }

            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(response_data).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

# Embedded SaaS-grade Web HTML Interface with "Emerald Ledger" / "Nordic Mint" Styling
HTML_CONTENT = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FIRA: Emerald Ledger Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #040D12;
            --bg-secondary: #182C25;
            --border-color: #2D4A3E;
            --accent-mint: #5C8374;
            --accent-green: #93B1A6;
            --accent-gold: #CDC2AE;
            --accent-red: #E25E5E;
            --text-main: #ECE5C7;
            --text-muted: #94A3B8;
        }

        body {
            background-color: var(--bg-primary);
            color: var(--text-main);
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            padding-bottom: 3rem;
        }

        .navbar {
            background-color: var(--bg-secondary);
            border-bottom: 2px solid var(--accent-mint);
            padding: 1rem 2rem;
        }

        .dashboard-container {
            margin-top: 2rem;
            padding: 0 2rem;
        }

        .card-custom {
            background-color: var(--bg-secondary);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            padding: 1.5rem;
            margin-bottom: 1.5rem;
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .card-custom:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        }

        .metric-label {
            font-size: 0.85rem;
            color: var(--accent-green);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .metric-value {
            font-size: 1.75rem;
            font-weight: 700;
            margin-top: 0.25rem;
            color: var(--accent-gold);
        }

        .sidebar-title {
            font-size: 1rem;
            font-weight: 600;
            color: var(--accent-green);
            margin-bottom: 1rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .sidebar-select {
            background-color: var(--bg-primary);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            border-radius: 8px;
            padding: 0.6rem;
            width: 100%;
            margin-bottom: 1.25rem;
        }

        .sidebar-select:focus {
            outline: none;
            border-color: var(--accent-mint);
        }

        .btn-run {
            background: linear-gradient(135deg, #1A4D3B, #5C8374);
            color: white;
            border: 1px solid var(--accent-mint);
            border-radius: 8px;
            padding: 0.75rem;
            font-weight: 600;
            transition: background 0.2s;
            width: 100%;
        }

        .btn-run:hover {
            background: linear-gradient(135deg, #2D4A3E, #93B1A6);
        }

        .verdict-badge {
            display: inline-block;
            padding: 0.5rem 1rem;
            border-radius: 8px;
            font-weight: 700;
            font-size: 1.5rem;
            text-align: center;
        }

        .verdict-BUY {
            background-color: rgba(147, 177, 166, 0.15);
            color: var(--accent-green);
            border: 1px solid var(--accent-green);
        }

        .verdict-SELL {
            background-color: rgba(226, 94, 94, 0.15);
            color: var(--accent-red);
            border: 1px solid var(--accent-red);
        }

        .verdict-HOLD {
            background-color: rgba(205, 194, 174, 0.15);
            color: var(--accent-gold);
            border: 1px solid var(--accent-gold);
        }

        .table-custom {
            color: var(--text-main) !important;
        }

        .table-custom th {
            color: var(--accent-green);
            border-bottom-color: var(--border-color) !important;
        }

        .table-custom td {
            border-bottom-color: rgba(45, 74, 62, 0.5) !important;
            padding: 0.75rem 0.5rem;
        }

        .badge-applied {
            background-color: rgba(92, 131, 116, 0.1);
            color: var(--accent-green);
            border: 1px solid var(--accent-mint);
            padding: 0.25rem 0.5rem;
            border-radius: 4px;
            font-size: 0.75rem;
            font-weight: 600;
        }

        .citation-node {
            background-color: rgba(92, 131, 116, 0.05);
            border-left: 3px solid var(--accent-mint);
            padding: 0.75rem;
            border-radius: 0 6px 6px 0;
            margin-bottom: 0.75rem;
            font-size: 0.9rem;
        }

        .citation-title {
            color: var(--accent-green);
            font-weight: 600;
            margin-bottom: 0.25rem;
        }

        /* Donut graph */
        .donut-container {
            display: flex;
            justify-content: center;
            align-items: center;
            height: 180px;
        }

        .donut-wrapper {
            position: relative;
            width: 140px;
            height: 140px;
        }
    </style>
</head>
<body>

    <!-- Top Navigation -->
    <nav class="navbar navbar-expand-lg navbar-dark">
        <div class="container-fluid d-flex justify-content-between">
            <span class="navbar-brand d-flex align-items-center font-monospace" style="color: var(--accent-gold);">
                <span class="fs-4 me-2">⚖️</span> FIRA DECISION PORTAL (EMERALD LEDGER)
            </span>
            <span class="badge bg-success">SECURE ALTERNATIVE RUNTIME</span>
        </div>
    </nav>

    <!-- Main Workspace -->
    <div class="dashboard-container">
        <div class="row">
            
            <!-- Left Sidebar Controls -->
            <div class="col-md-3 col-lg-3">
                <div class="card-custom">
                    <div class="sidebar-title">⚡ Consolidated Controls</div>
                    
                    <label class="form-label text-muted small">Select Target Investor Profile</label>
                    <select id="profile-select" class="sidebar-select">
                        <option value="ROHAN">Rohan Mehta (Risk-Averse)</option>
                        <option value="ANANYA">Ananya Sen (Growth-Seeking)</option>
                    </select>

                    <label class="form-label text-muted small">Select Indian Equity Ticker</label>
                    <select id="stock-select" class="sidebar-select">
                        <option value="TCS">TCS - Tata Consultancy Services</option>
                        <option value="HDFCBANK">HDFCBANK - HDFC Bank Ltd</option>
                        <option value="ITC">ITC - ITC Industries Ltd</option>
                    </select>

                    <label class="form-label text-muted small">Inject System Fault</label>
                    <select id="failure-select" class="sidebar-select">
                        <option value="None">No Faults (Healthy)</option>
                        <option value="FUNDAMENTALS_DOWN">OUTAGE: Fundamentals Feed Crash</option>
                        <option value="TECHNICAL_DOWN">OUTAGE: Technical Feed Timeout</option>
                        <option value="SENTIMENT_DOWN">OUTAGE: Sentiment API Crash</option>
                    </select>

                    <button class="btn-run" onclick="triggerAnalysis()">
                        🚀 Execute FIRA Core Cycle
                    </button>
                </div>

                <!-- Active Profile Configuration Widget -->
                <div class="card-custom" id="profile-card">
                    <div class="sidebar-title">👤 Active Profile Attributes</div>
                    <div class="mb-2">
                        <span class="text-muted small">Leverage Threshold:</span>
                        <span class="float-end font-monospace" id="prof-leverage" style="color: var(--accent-gold);">0.75</span>
                    </div>
                    <div class="mb-3">
                        <span class="text-muted small">Valuation PE Cap:</span>
                        <span class="float-end font-monospace" id="prof-pe" style="color: var(--accent-gold);">22.0</span>
                    </div>
                    <div class="sidebar-title mt-4" style="font-size: 0.85rem;">💼 Active Portfolio Shares</div>
                    <div id="portfolio-list">
                        <!-- Filled dynamically -->
                    </div>
                </div>
            </div>

            <!-- Right Dashboard Content -->
            <div class="col-md-9 col-lg-9">
                
                <!-- Financial Tickers Metric Row -->
                <div class="row">
                    <div class="col-md-4">
                        <div class="card-custom">
                            <div class="metric-label">Live Price Feeds</div>
                            <div class="metric-value font-monospace" id="m-price">₹--</div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card-custom">
                            <div class="metric-label">14D Relative Strength (RSI)</div>
                            <div class="metric-value font-monospace text-warning" id="m-rsi">--</div>
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="card-custom">
                            <div class="metric-label">Balance Sheet Leverage (D/E)</div>
                            <div class="metric-value font-monospace" id="m-leverage">--</div>
                        </div>
                    </div>
                </div>

                <div class="row">
                    <!-- Main Consensus Verdict Column -->
                    <div class="col-lg-7">
                        <div class="card-custom h-100">
                            <div class="d-flex justify-content-between align-items-center mb-3">
                                <span class="sidebar-title mb-0">⚖️ Integrated Rating Output</span>
                                <span class="badge-applied" id="m-confidence">Reliability: --%</span>
                            </div>
                            
                            <div class="text-center my-4">
                                <div id="verdict-display" class="verdict-badge verdict-HOLD">HOLD</div>
                                <div class="mt-2 text-muted small">Consensus Scoring Scale: -1.00 (Strong Sell) to +1.00 (Strong Buy)</div>
                                <div class="fs-5 mt-1 font-monospace" id="m-score" style="color: var(--accent-gold);">Score: 0.00</div>
                            </div>

                            <hr style="border-color: var(--border-color)">
                            
                            <div class="mb-3">
                                <span class="text-muted small d-block mb-1">Mathematical Rationale:</span>
                                <p id="m-rationale" class="small" style="line-height: 1.5;">Consensus awaiting first analysis pass...</p>
                            </div>

                            <div class="mb-2">
                                <span class="text-muted small d-block mb-1">Applied Structural Overlays:</span>
                                <div id="overlays-list" class="d-flex gap-2 flex-wrap">
                                    <span class="badge-applied bg-secondary border-0">None</span>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- Asset Distribution Widget -->
                    <div class="col-lg-5">
                        <div class="card-custom h-100">
                            <span class="sidebar-title">📊 Asset Allocation Risk</span>
                            <div class="donut-container">
                                <div class="donut-wrapper">
                                    <svg viewBox="0 0 36 36" style="width: 100%; height: 100%;">
                                        <path class="circle-bg" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="#11221D" stroke-width="3"></path>
                                        <path id="pie-segment-1" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="var(--accent-mint)" stroke-width="4.5" stroke-dasharray="45, 100" stroke-dashoffset="0"></path>
                                        <path id="pie-segment-2" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="var(--accent-green)" stroke-width="4.5" stroke-dasharray="15, 100" stroke-dashoffset="-45"></path>
                                        <path id="pie-segment-3" d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831" fill="none" stroke="var(--accent-gold)" stroke-width="4.5" stroke-dasharray="40, 100" stroke-dashoffset="-60"></path>
                                        <text x="18" y="21.5" class="percentage" fill="var(--text-main)" font-size="6" font-family="monospace" font-weight="bold" text-anchor="middle" id="hhi-value">--</text>
                                    </svg>
                                </div>
                            </div>
                            <div class="text-center small text-muted">
                                Portfolio Herfindahl-Hirschman Concentration Index (HHI): <strong id="hhi-rating" class="text-white">--</strong>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Parallel Agent Executions Grid -->
                <div class="row mt-4">
                    <div class="col-col-12">
                        <div class="card-custom">
                            <span class="sidebar-title">🕵️ Parallel Analyst Voting Matrix</span>
                            <table class="table table-custom mb-0">
                                <thead>
                                    <tr>
                                        <th>Agent Specialist Node</th>
                                        <th>Recommendation Vote</th>
                                        <th>Raw Scoring</th>
                                        <th>Confidence Weight</th>
                                        <th class="text-end">Engine Speed</th>
                                    </tr>
                                </thead>
                                <tbody id="agent-table-body">
                                    <tr>
                                        <td colspan="5" class="text-center text-muted small py-4">Execute FIRA core cycle to boot parallel workflows...</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>

                <!-- Grounded Citations Row -->
                <div class="row mt-4">
                    <div class="col-col-12">
                        <div class="card-custom">
                            <span class="sidebar-title">📖 Verifiable SEBI Filing References</span>
                            <div id="citations-container" class="mt-2">
                                <div class="text-center text-muted small py-3">No references currently pulled from local semantic indexes.</div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Performance Metrics Log -->
                <div class="row mt-4">
                    <div class="col-md-6">
                        <div class="card-custom">
                            <span class="sidebar-title" style="font-size: 0.85rem;">⏱️ Real-time Telemetry Logs</span>
                            <div class="d-flex justify-content-between py-2 border-bottom border-secondary">
                                <span class="text-muted small">Total Execution Latency:</span>
                                <span id="tel-latency" class="font-monospace text-success">-- ms</span>
                            </div>
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="card-custom">
                            <span class="sidebar-title" style="font-size: 0.85rem;">🎯 Predictive Validation</span>
                            <div class="d-flex justify-content-between py-2 border-bottom border-secondary">
                                <span class="text-muted small">30D Return Trend Alignment:</span>
                                <span id="tel-accuracy" class="font-monospace text-success">--</span>
                            </div>
                        </div>
                    </div>
                </div>

            </div>
        </div>
    </div>

    <script>
        function triggerAnalysis() {
            const stock = document.getElementById("stock-select").value;
            const profile = document.getElementById("profile-select").value;
            const failure = document.getElementById("failure-select").value;

            // Update UI to Loading States
            document.getElementById("m-price").innerText = "₹...";
            document.getElementById("m-rsi").innerText = "...";
            document.getElementById("m-leverage").innerText = "...";
            document.getElementById("m-rationale").innerText = "Processing parallel expert threads...";
            
            fetch(`/api/analyze?stock=${stock}&profile=${profile}&failure=${failure}`)
                .then(res => res.json())
                .then(data => {
                    // Update metric cards
                    document.getElementById("m-price").innerText = "₹" + data.feed.price.toFixed(2);
                    document.getElementById("m-rsi").innerText = data.feed.rsi.toFixed(1);
                    document.getElementById("m-leverage").innerText = data.feed.debt_to_equity.toFixed(2);

                    // Update Verdict badge
                    const vDisp = document.getElementById("verdict-display");
                    vDisp.innerText = data.consensus.verdict;
                    vDisp.className = `verdict-badge verdict-${data.consensus.verdict}`;

                    // Update Score and confidence
                    document.getElementById("m-score").innerText = "Score: " + (data.consensus.consensus_score >= 0 ? "+" : "") + data.consensus.consensus_score.toFixed(2);
                    document.getElementById("m-confidence").innerText = "Reliability: " + Math.round(data.consensus.reliability * 100) + "%";
                    document.getElementById("m-rationale").innerText = data.consensus.logic;

                    // Update overlays
                    const ovList = document.getElementById("overlays-list");
                    ovList.innerHTML = "";
                    if (data.consensus.overlays.length === 0) {
                        ovList.innerHTML = '<span class="badge-applied bg-secondary border-0">None</span>';
                    } else {
                        data.consensus.overlays.forEach(ov => {
                            ovList.innerHTML += `<span class="badge-applied">${ov}</span> `;
                        });
                    }

                    // Update active profile configurations
                    document.getElementById("prof-leverage").innerText = data.active_profile.leverage_threshold.toFixed(2);
                    document.getElementById("prof-pe").innerText = data.active_profile.valuation_cap.toFixed(2);
                    
                    const portList = document.getElementById("portfolio-list");
                    portList.innerHTML = "";
                    const assetKeys = Object.keys(data.active_profile.portfolio);
                    assetKeys.forEach(asset => {
                        const val = data.active_profile.portfolio[asset];
                        portList.innerHTML += `
                            <div class="small d-flex justify-content-between mb-1 text-muted">
                                <span>• ${asset}</span>
                                <span class="font-monospace" style="color: var(--accent-gold);">${val}%</span>
                            </div>`;
                    });

                    // Update Donut Chart Segments
                    let val1 = data.active_profile.portfolio[assetKeys[0]] || 0;
                    let val2 = data.active_profile.portfolio[assetKeys[1]] || 0;
                    let val3 = data.active_profile.portfolio[assetKeys[2]] || 0;

                    const segment1 = document.getElementById("pie-segment-1");
                    const segment2 = document.getElementById("pie-segment-2");
                    const segment3 = document.getElementById("pie-segment-3");

                    segment1.setAttribute("stroke-dasharray", `${val1}, 100`);
                    segment2.setAttribute("stroke-dasharray", `${val2}, 100`);
                    segment2.setAttribute("stroke-dashoffset", `-${val1}`);
                    segment3.setAttribute("stroke-dasharray", `${val3}, 100`);
                    segment3.setAttribute("stroke-dashoffset", `-${val1 + val2}`);

                    document.getElementById("hhi-value").textContent = Math.round(data.telemetry.portfolio_hhi);
                    document.getElementById("hhi-rating").textContent = data.telemetry.portfolio_hhi < 1500 ? "Low Risk" : data.telemetry.portfolio_hhi < 2500 ? "Moderate" : "High Risk";

                    // Update Telemetry Row
                    document.getElementById("tel-latency").innerText = data.telemetry.latency_ms.toFixed(1) + " ms";
                    document.getElementById("tel-accuracy").innerText = data.telemetry.accuracy_score === 1.0 ? "100% Correct Alignment" : "Stable/Neutral Trend";

                    // Update Analyst Grid
                    const agentBody = document.getElementById("agent-table-body");
                    agentBody.innerHTML = "";
                    if (data.consensus.analysts.length === 0) {
                        agentBody.innerHTML = `<tr><td colspan="5" class="text-center text-danger small py-3">⚠️ Fault Alert: No active threads returned consensus results. Fallbacks engaged.</td></tr>`;
                    } else {
                        data.consensus.analysts.forEach(ag => {
                            const signalColor = ag.rating === "BUY" ? "text-success font-weight-bold" : ag.rating === "SELL" ? "text-danger" : "text-warning";
                            agentBody.innerHTML += `
                                <tr>
                                    <td><strong class="text-white">${ag.analyst_name}</strong></td>
                                    <td><span class="${signalColor}">${ag.rating}</span></td>
                                    <td class="font-monospace">${ag.score >= 0 ? "+" : ""}${ag.score.toFixed(2)}</td>
                                    <td class="font-monospace">${Math.round(ag.confidence * 100)}%</td>
                                    <td class="text-end text-success font-monospace">${ag.latency_ms.toFixed(1)} ms</td>
                                </tr>`;
                        });
                    }

                    // Update Grounding Citations
                    const citContainer = document.getElementById("citations-container");
                    citContainer.innerHTML = "";
                    if (data.contexts.length === 0) {
                        citContainer.innerHTML = `<div class="text-center text-muted small py-2">No documents currently pulled from local indexes.</div>`;
                    } else {
                        data.contexts.forEach(ctx => {
                            const spl = ctx.split("]", 2);
                            const nodeId = spl[0] + "]";
                            const body = spl[1].trim();
                            citContainer.innerHTML += `
                                <div class="citation-node">
                                    <div class="citation-title">${nodeId}</div>
                                    <div class="text-white">${body}</div>
                                </div>`;
                        });
                    }

                })
                .catch(err => {
                    console.error(err);
                    document.getElementById("m-rationale").innerText = "Outage: Error contacting local FIRA Consensus Engine. Verify app.py is hosting.";
                });
        }

        // Boot initial pass on window load
        window.onload = function() {
            triggerAnalysis();
        };
    </script>
</body>
</html>
"""

def start_server():
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), FIRARequestHandler) as httpd:
        print(f"📡 SUCCESS: Zero-Dependency FIRA Web Server launched on http://localhost:{PORT}")
        print("  ==============================================================")
        print("  Press Ctrl+C inside this terminal window to stop the server.")
        print("  ==============================================================")
        httpd.serve_forever()

def main():
    print("==============================================================")
    print("⚖️  Launching FIRA Consolidated Web Dashboard Server...")
    print("==============================================================")

    # Launch browser thread after 1.5 seconds delay
    threading.Thread(target=lambda: (time.sleep(1.5), webbrowser.open(f"http://localhost:{PORT}"))).start()
    
    # Run the HTTP server on the main thread
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n📡 Server stopped by user.")

if __name__ == "__main__":
    main()
