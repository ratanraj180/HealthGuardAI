# 🛡️ HealthGuard AI

**Autonomous Code & Infrastructure Sentinel**

HealthGuard AI is a multi-agent system that continuously monitors your system, detects anomalies, uses AI to diagnose root causes, performs safe autonomous fixes, and verifies recovery.

## 🚀 Features

*   **Multi-Agent Architecture**: Separate agents for Monitor, Detect, Diagnose, Fix, Verify, Report.
*   **AI Diagnosis**: Uses simulated LLM logic to explain root causes in plain English.
*   **Auto-Remediation**: Safely applies fixes like restarting services or clearing caches.
*   **Live Dashboard**: Real-time visualization of system health using Streamlit.
*   **Slack Alerts**: Instant notifications when incidents occur.

## 📁 Project Structure

*   `agents/`: The AI agents (Monitor, Detector, Fixer, etc.)
*   `core/`: Core logic and Orchestrator.
*   `config/`: Configuration settings.
*   `ui/`: The Streamlit dashboard.
*   `main.py`: The backend system entry point.

## 🛠️ How to Run

### Prerequisities
You need Python installed. Install dependencies:
```bash
pip install streamlit pandas requests
```

### 1. Start the Backend Brain 🧠
This runs the simulation and the agents.
```bash
python main.py
```

### 2. Start the Dashboard 📊
Open a **new terminal** and run:
```bash
streamlit run ui/dashboard.py
```

Now watch the dashboard as the system simulates traffic, detects anomalies, and automatically fixes them!

## ⚠️ Configuration
*   Edit `config/settings.py` to change thresholds or disable simulation.
*   Edit `integrations/slack_alert.py` to add your real Slack Webhook URL.

---
*Built for the Hackathon*
