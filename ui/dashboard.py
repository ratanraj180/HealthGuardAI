import streamlit as st
import json
import time
import pandas as pd
import os
import sys
import random
from datetime import datetime

# Add parent directory to path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.database import DatabaseManager

st.set_page_config(
    page_title="HealthGuard AI Monitor",
    page_icon="🛡️",
    layout="wide",
)

# Custom CSS for "High Quality" feel
st.markdown("""
<style>
    .metric-card {
        background-color: #1E1E1E;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333;
    }
    .stApp {
        background-color: #0E1117;
    }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ HealthGuard AI: Autonomous SRE")
st.markdown("### 🔴 Live System Telemetry")

# --- CLOUD DEPLOYMENT SUPPORT: SELF-DRIVING MODE ---
def ensure_live_data(db_manager):
    """Generates a new data point with SMOOTH random walk for realistic effect"""
    
    # Get last values to make it continuous
    last_metrics = db_manager.get_latest_metrics(limit=4)
    last_cpu = 0.3
    last_mem = 0.4
    
    if last_metrics:
        # Try to find last CPU/Mem values
        for m in last_metrics:
            if m[2] == "cpu" and m[3] == "usage": last_cpu = m[4]
            if m[2] == "memory" and m[3] == "usage": last_mem = m[4]

    # Random Walk: Change by a small amount (-0.05 to +0.05)
    cpu_change = (random.random() - 0.5) * 0.1
    mem_change = (random.random() - 0.5) * 0.05
    
    new_cpu = max(0.05, min(0.95, last_cpu + cpu_change))
    new_mem = max(0.1, min(0.90, last_mem + mem_change))
    
    # Occasional Spikes
    if random.random() > 0.95: new_cpu = random.uniform(0.8, 0.99)
    
    db_lat = random.randint(20, 60) if new_cpu < 0.8 else random.randint(100, 300)
    api_lat = random.randint(30, 150)

    db_manager.log_metric("cpu", "usage", new_cpu)
    db_manager.log_metric("memory", "usage", new_mem)
    db_manager.log_metric("database", "latency", db_lat)
    db_manager.log_metric("api", "latency", api_lat)
    
    return new_cpu, new_mem, db_lat, api_lat

# Connect to DB
try:
    db = DatabaseManager()
except Exception as e:
    st.error(f"Failed to connect to Database: {e}")
    st.stop()

# Layout: Metrics Row
col1, col2, col3, col4 = st.columns(4)

# Generate & Get Data
curr_cpu, curr_mem, curr_db, curr_api = ensure_live_data(db)

with col1:
    st.metric("CPU Load", f"{curr_cpu*100:.1f}%", f"{(curr_cpu-0.5)*10:.1f}%", delta_color="inverse")
with col2:
    st.metric("Memory Usage", f"{curr_mem*100:.1f}%", f"{(curr_mem-0.5)*5:.1f}%", delta_color="normal")
with col3:
    st.metric("DB Latency", f"{curr_db}ms", delta_color="inverse")
with col4:
    st.metric("API Latency", f"{curr_api}ms")

# --- VISUALIZATION: AREA CHARTS ---
st.markdown("### System Performance")
chart_col1, chart_col2 = st.columns(2)

# Fetch History
raw_metrics = db.get_latest_metrics(limit=200) # Get more data for smooth lines
metric_df = pd.DataFrame(raw_metrics, columns=["id", "timestamp", "Component", "Name", "Value"])
metric_df["Component"] = metric_df["Component"].str.upper()

with chart_col1:
    st.subheader("🔥 CPU Usage Trend")
    cpu_df = metric_df[metric_df["Name"] == "usage"]
    cpu_df = cpu_df[cpu_df["Component"] == "CPU"]
    
    if not cpu_df.empty:
        # Reverse to show chronological order (oldest -> newest)
        chart_data = cpu_df.sort_values("id")
        # Clean index for chart
        chart_data = chart_data.reset_index(drop=True)
        st.area_chart(chart_data["Value"], color="#ff4b4b") # Red for CPU
    else:
        st.info("Initializing CPU Stream...")

with chart_col2:
    st.subheader("💾 Memory Usage Trend")
    mem_df = metric_df[metric_df["Name"] == "usage"]
    mem_df = mem_df[mem_df["Component"] == "MEMORY"]
    
    if not mem_df.empty:
        chart_data = mem_df.sort_values("id")
        chart_data = chart_data.reset_index(drop=True)
        st.area_chart(chart_data["Value"], color="#0068c9") # Blue for Memory
    else:
        st.info("Initializing Memory Stream...")

# --- INCIDENTS ---
st.subheader("🚨 Detected Anomalies")
incidents = db.get_incidents(limit=3)
if incidents:
    for inc in incidents:
        st.error(f"**{inc[3]}** | {inc[1]} | Root Cause: {inc[4]}")
else:
    st.success("No active anomalies detected. System operating within normal parameters.")

# Auto-refresh
time.sleep(0.8) # Faster refresh for "video" feel
st.rerun()

