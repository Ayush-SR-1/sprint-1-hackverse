# FIRA (Financial Intelligence & Risk Advisor)

A clean, orchestrated parallel multi-agent AI consensus framework with SEBI filing RAG grounding, customized specifically to address the retail investor infrastructure gap.

## 🛠️ System Design & Files
This project consists of 10 fully modular Python scripts:
*   **`knowledge_base.py`**: The local RAG data node executing context lookups over SEBI financial filings and corporate records (TCS, HDFC Bank, ITC).
*   **`feed_handler.py`**: Simulated real-time market quantitative statistics (price, RSI, moving averages, daily trading volume ratios).
*   **`analysts.py`**: The parallel execution layer managing individual analyst threads (Fundamentals Auditor, Quantitative Modeler, Sentiment Scraper) with strict Pydantic output contracts.
*   **`investor_profile.py`**: The dynamic database management module configuring Rohan Mehta (Risk-Averse) and Ananya Sen (Growth-Seeking) parameters.
*   **`consensus_engine.py`**: The core consensus orchestrator executing weighted decision matrix aggregates, re-normalizations on dependency outages, and behavioral overlays.
*   **`audit_logger.py`**: Telemetry metrics tracker, auditing execution latency, accuracy flags, and portfolio Herfindahl concentration indexes (HHI).
*   **`cli_dashboard.py`**: Visual command-line interface tracking automated simulation walkthroughs.
*   **`web_app.py`**: The definitive zero-dependency local web dashboard server (built on standard library `http.server` on Port 8090) utilizing pure CSS layouts and SVG vectors.

## 🚀 Getting Started (Unpacking and Running)

1. Unpack the files using the safe self-extractor script:
   ```bash
   python fira_installer.py
   ```
2. Launch your web app instantly (zero dependencies or third-party libraries required!):
   ```bash
   python web_app.py
   ```
   *Your web browser will automatically load your beautiful Emerald & Gold Executive dashboard at http://localhost:8090!*

3. (Optional) Run the command line terminal dashboard:
   ```bash
   pip install -r requirements.txt
   python cli_dashboard.py
   ```
