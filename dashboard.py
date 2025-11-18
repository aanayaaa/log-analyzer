# dashboard.py
import streamlit as st
import pandas as pd
import os
import plotly.express as px
import plotly.graph_objects as go
from streamlit_autorefresh import st_autorefresh

from log_parser import read_log_file, parse_log_lines
from analyzer import count_by_level, top_repeated_errors, errors_by_hour, keyword_search

# -------------------------
st.set_page_config(page_title="Live Log Monitoring Dashboard", layout="wide")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_PATH = os.path.join(BASE_DIR, "logs", "sample.log")

# CSS (dark theme tweaks)
st.markdown(
    """
    <style>
    .block-container {padding-top: 1.0rem;}
    .metric-card {background-color: #0b1220;padding:26px;border-radius:12px;border:1px solid #111827;text-align:center;}
    [data-testid="stSidebar"] {background-color:#0f172a;}
    .stSelectbox div, select, .stNumberInput input {background-color:#111827;color:white;}
    </style>
    """,
    unsafe_allow_html=True,
)

# Sidebar controls
st.sidebar.header("Settings")
auto_refresh = st.sidebar.checkbox("Auto refresh", value=True)
interval = st.sidebar.selectbox("Refresh interval (seconds)", [1, 2, 3, 5, 7, 10], index=2)
keyword_filter = st.sidebar.text_input("Filter keyword OPTIONAL")
st.sidebar.markdown("---")
st.sidebar.write("Developed by Aanaya Verma")

# Autorefresh (doesn't block — placed early so UI controls show)
if auto_refresh:
    st_autorefresh(interval=interval * 1000, key="logrefresh")

# Load logs
def load_df():
    lines = read_log_file(LOG_PATH)
    parsed = parse_log_lines(lines)
    return pd.DataFrame(parsed)

df = load_df()

if df.empty:
    st.warning("No logs found yet... (run log_simulator.py in another terminal)")
    st.stop()

# Page title and metrics
st.title("Log Monitoring Dashboard")
st.write("Enterprise-grade real-time monitoring")

counts = count_by_level(df.to_dict(orient="records"))
c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"<div class='metric-card'><h4>INFO</h4><h2 style='color:#60a5fa'>{counts.get('INFO',0)}</h2></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='metric-card'><h4>WARNING</h4><h2 style='color:#fbbf24'>{counts.get('WARNING',0)}</h2></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='metric-card'><h4>ERROR</h4><h2 style='color:#f87171'>{counts.get('ERROR',0)}</h2></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='metric-card'><h4>CRITICAL</h4><h2 style='color:#ef4444'>{counts.get('CRITICAL',0)}</h2></div>", unsafe_allow_html=True)

st.markdown("---")

# Top repeated errors
st.subheader("Top Repeated Errors")
tops = top_repeated_errors(df.to_dict(orient="records"), top_n=8)
error_df = pd.DataFrame(tops, columns=["message", "count"]) if tops else pd.DataFrame(columns=["message","count"])

fig1 = px.bar(error_df, x="message", y="count", color="count", color_continuous_scale="Plasma")
fig1.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#0f172a", font=dict(color="white"))
st.plotly_chart(fig1, use_container_width=True)

# Error trends
st.subheader("Error Trends Over Time")
hour_counts = errors_by_hour(df.to_dict(orient="records"))
hour_df = pd.DataFrame(list(hour_counts.items()), columns=["hour", "count"]) if hour_counts else pd.DataFrame(columns=["hour","count"])
if not hour_df.empty:
    fig2 = go.Figure()
    fig2.add_trace(go.Bar(x=hour_df["hour"], y=hour_df["count"], marker_color="#06b6d4"))
    fig2.update_layout(paper_bgcolor="#0f172a", plot_bgcolor="#0f172a", font=dict(color="white"), title="Errors by Hour")
    st.plotly_chart(fig2, use_container_width=True)
else:
    st.info("Not enough timestamped entries to plot hourly trend.")

# Security Alerts
st.subheader("Security Alerts (Unauthorized Attempts)")
security_logs = keyword_search(df.to_dict(orient="records"), "unauthorized")
if security_logs:
    sec_df = pd.DataFrame(security_logs).drop(columns=["stacktrace"], errors="ignore")
    st.dataframe(sec_df, use_container_width=True)
else:
    st.success("No unauthorized attempts detected.")

# Raw logs (with filter + highlight)
# ---------------------------------------------------------
# RAW LOGS TABLE
# ---------------------------------------------------------
st.subheader("Raw Logs")

# Better row choices for real-time logs
row_count = st.selectbox(
    "Rows to show",
    ["All", 100, 500, 1000, 5000],
    index=1
)

filtered_df = df.copy()

# Apply keyword filter
if keyword_filter.strip():
    k = keyword_filter.lower()

    mask = filtered_df["message"].fillna("").str.contains(k, case=False, na=False) | \
           filtered_df["stacktrace"].fillna("").str.contains(k, case=False, na=False)

    filtered_df = filtered_df[mask]

    if filtered_df.empty:
        st.warning("No matching logs found.")
    else:
        # Highlight
        display_df = filtered_df.copy()
        display_df["message"] = display_df["message"].astype(str).str.replace(
            k, f"<mark style='background:#38bdf8;color:#000'>{k}</mark>",
            case=False, regex=True
        )
        display_df["stacktrace"] = display_df["stacktrace"].astype(str).str.replace(
            k, f"<mark style='background:#38bdf8;color:#000'>{k}</mark>",
            case=False, regex=True
        )

        # Select rows
        shown_df = display_df if row_count == "All" else display_df.tail(int(row_count))

        st.markdown(shown_df.to_html(escape=False, index=False), unsafe_allow_html=True)

else:
    # no keyword filtering
    shown_df = filtered_df if row_count == "All" else filtered_df.tail(int(row_count))
    st.dataframe(shown_df, use_container_width=True)
