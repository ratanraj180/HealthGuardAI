import streamlit as st
import json
import time
import pandas as pd
import os
import sys

# Add parent directory to path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import DatabaseManager

st.set_page_config(
    page_title="HealthGuard AI Monitor",
    page_icon="🛡️",
    layout="wide",
)

st.title("🛡️ HealthGuard AI: Autonomous SRE")
st.markdown("### Production Environment Simulation (With SQLite DB)")

# Refresh mechanism
if st.button("Refresh Data"):
    st.rerun()

# Connect to DB
try:
    db = DatabaseManager()
except Exception as e:
    st.error(f"Failed to connect to Database: {e}")
    st.stop()

# Layout
col1, col2, col3, col4 = st.columns(4)

# Get Metrics from DB
raw_metrics = db.get_latest_metrics()
# Metrics table: (id, timestamp, component, name, value)

if not raw_metrics:
    st.info("No metrics in database yet. Waiting for Orchestrator...")
    time.sleep(2)
    st.rerun()

# Parse metrics (simplified for display)
# We want the latest one for each component
latest_metrics = {}
for m in raw_metrics:
    # m = (id, timestamp, component, name, value)
    comp = m[2]
    name = m[3]
    val = m[4]
    key = f"{comp}_{name}"
    # Since we ordered internally by DESC, the first one we see is the latest? 
    # Actually get_latest_metrics does LIMIT 100 on DESC ID.
    # So iterating them, the first occurence of a key is the latest.
    if key not in latest_metrics:
        latest_metrics[key] = val

cpu_val = latest_metrics.get("cpu_usage", 0)
mem_val = latest_metrics.get("memory_usage", 0)
db_val = latest_metrics.get("database_latency", 0)
api_val = latest_metrics.get("api_latency", 0)

with col1:
    val = cpu_val * 100
    delta_color = "inverse" if val > 80 else "normal"
    st.metric("CPU Usage", f"{val:.1f}%", delta_color=delta_color)

with col2:
    val = mem_val * 100
    st.metric("Memory Usage", f"{val:.1f}%")

with col3:
    st.metric("DB Latency", f"{db_val:.0f}ms", delta_color="inverse")

with col4:
    st.metric("API Latency", f"{api_val:.0f}ms")

# Status Banner
if cpu_val > 0.85:
    st.error("🚨 CRITICAL: High CPU Usage Detected! Remediation Pipeline Active.")
elif db_val > 300:
    st.warning("⚠️ WARNING: Database Latency High.")
else:
    st.success("✅ SYSTEM HEALTHY: All systems operational.")

# Charts
st.subheader("Live System Telemetry")
chart_col1, chart_col2 = st.columns(2)

# Convert DB rows to DataFrame
metric_df = pd.DataFrame(raw_metrics, columns=["id", "timestamp", "Component", "Name", "Value"])
# Upper case component for display
metric_df["Component"] = metric_df["Component"].str.upper()

with chart_col1:
    # Filter for just usage metrics (CPU/Memory) for the bar chart or similar
    # Actually let's just show the latest 10 points
    st.bar_chart(metric_df.head(20).pivot_table(index="Component", values="Value", aggfunc='mean'))

with chart_col2:
    # Latest Incident Reports
    st.subheader("Incident History (SQLite)")
    incidents = db.get_incidents()
    # (id, timestamp, status, anomaly_component, root_cause, fix_action, full_report)
    
    if incidents:
        for inc in incidents:
            with st.expander(f"{inc[1]} - {inc[3]} ({inc[2]})"):
                st.write(f"**Root Cause:** {inc[4]}")
                st.write(f"**Fix Action:** {inc[5]}")
                st.code(inc[6])
    else:
        st.info("No incidents recorded in database.")

st.markdown("---")
st.caption("Powered by HealthGuard AI & SQLite")

# Auto-refresh at the END so everything renders first
time.sleep(1)
st.rerun()
