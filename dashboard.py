import streamlit as st
import pandas as pd
import os
import time
import random
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

from log_parser import read_log_file, parse_log_lines
from analyzer import count_by_level, top_repeated_errors, errors_by_hour, keyword_search

# -----------------------------------------------------------
# STREAMLIT CONFIG
# -----------------------------------------------------------
st.set_page_config(page_title="Live Log Dashboard", layout="wide")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "logs", "sample.log")

# Detect Streamlit Cloud
RUNNING_IN_CLOUD = os.environ.get("STREAMLIT_RUNTIME") == "cloud"

# Make sure logs folder exists
os.makedirs(os.path.join(BASE_DIR, "logs"), exist_ok=True)

# -----------------------------------------------------------
# CLOUD AUTO-LOG GENERATOR
# -----------------------------------------------------------
def generate_fake_logs():
    """Generate logs automatically in Streamlit Cloud (so dashboard always works)."""
    messages = [
        "Starting system initialization",
        "Loading configuration file /etc/app/config.yaml",
        "Disk usage at 85% on /dev/sda1",
        "Database connection failed: timeout after 30s",
        "Unauthorized access attempt from IP 192.168.1.45",
        "Stack trace: File 'app.py', line 42, in <module>",
        "Memory usage crossed 90%",
        "Retrying database connection",
        "Failed to authenticate user: invalid token",
        "System crash detected in Module X"
    ]

    levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]

    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"{ts} | {random.choice(levels)} | {random.choice(messages)}\n"

    with open(LOG_PATH, "a") as f:
        f.write(entry)


# -----------------------------------------------------------
# LOAD LOG DATA
# -----------------------------------------------------------
def load_logs():
    if not os.path.exists(LOG_PATH):
        return pd.DataFrame()
    return pd.DataFrame(parse_log_lines(read_log_file(LOG_PATH)))


# -----------------------------------------------------------
# SIDEBAR
# -----------------------------------------------------------
st.sidebar.header("Settings")
auto_refresh = st.sidebar.checkbox("Auto refresh", True)
interval = st.sidebar.selectbox("Refresh interval (sec)", [1, 2, 3, 5, 10], 1)
keyword_filter = st.sidebar.text_input("Filter logs by keyword")

st.sidebar.markdown("---")
st.sidebar.write("Developed by Aanaya Verma 💙")

# -----------------------------------------------------------
# CLOUD LOG GENERATION
# -----------------------------------------------------------
if RUNNING_IN_CLOUD:
    generate_fake_logs()

# -----------------------------------------------------------
# LOAD LOGS FOR DISPLAY
# -----------------------------------------------------------
df = load_logs()

if df.empty:
    st.warning("No logs found yet…")
else:
    # Page title
    st.title("Real-Time Log Monitoring Dashboard")

    # Top metrics
    counts = count_by_level(df.to_dict(orient="records"))

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("INFO", counts.get("INFO", 0))
    col2.metric("WARNING", counts.get("WARNING", 0))
    col3.metric("ERROR", counts.get("ERROR", 0))
    col4.metric("CRITICAL", counts.get("CRITICAL", 0))

    st.divider()

    # Top repeated errors
    st.subheader("Top Repeated Errors")
    tops = top_repeated_errors(df.to_dict(orient="records"))
    error_df = pd.DataFrame(tops, columns=["message", "count"])

    if not error_df.empty:
        fig = px.bar(error_df, x="message", y="count", color="count")
        fig.update_layout(paper_bgcolor="#0f172a", font=dict(color="white"))
        st.plotly_chart(fig, width="stretch")

    # Errors over time
    st.subheader("Error Trends Over Time")
    hour_df = pd.DataFrame(errors_by_hour(df.to_dict(orient="records")).items(),
                           columns=["hour", "count"])
    if not hour_df.empty:
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=hour_df["hour"], y=hour_df["count"],
                                  mode="lines+markers", line=dict(color="#06b6d4")))
        fig2.update_layout(paper_bgcolor="#0f172a", font=dict(color="white"))
        st.plotly_chart(fig2, width="stretch")

    # Security alerts
    st.subheader("Security Alerts")
    sec = keyword_search(df.to_dict(orient="records"), "unauthorized")
    if sec:
        st.dataframe(pd.DataFrame(sec))
    else:
        st.success("No unauthorized attempts found.")

    # Raw logs
    st.subheader("Raw Logs")
    filtered_df = df.copy()

    if keyword_filter.strip():
        filtered_df = filtered_df[
            filtered_df["message"].str.contains(keyword_filter, case=False, na=False)
        ]

    st.dataframe(filtered_df.tail(50), width="stretch")

# -----------------------------------------------------------
# AUTO REFRESH
# -----------------------------------------------------------
if auto_refresh:
    st_autorefresh(interval=interval * 1000, key="refresh")
