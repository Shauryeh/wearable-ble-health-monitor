import streamlit as st
import pandas as pd
from src.config import CSV_FILE

st.set_page_config(page_title="JCVital Live Dashboard", layout="wide")

st.title("JCVital Live Health Dashboard")
st.caption("Live Bluetooth data from JCVital 2208A band")

@st.fragment(run_every=2)
def render_live_dashboard():
    if not CSV_FILE.exists():
        st.warning("Waiting for data file. Start live_logger.py first.")
        return

    try:
        df = pd.read_csv(CSV_FILE)

        if df.empty or len(df) < 2:
            st.warning("Waiting for live band data...")
            return

        df["timestamp"] = pd.to_datetime(df["timestamp"], errors="coerce")
        df["heart_rate"] = pd.to_numeric(df["heart_rate"], errors="coerce")
        df["spo2"] = pd.to_numeric(df["spo2"], errors="coerce")
        df["raw_hr"] = pd.to_numeric(df["raw_hr"], errors="coerce")
        df["raw_spo2"] = pd.to_numeric(df["raw_spo2"], errors="coerce")

        df = df.dropna(subset=["timestamp"])

        hr_df = df.dropna(subset=["heart_rate"])
        spo2_df = df.dropna(subset=["spo2"])

        col1, col2, col3, col4 = st.columns(4)

        if not hr_df.empty:
            latest_hr = int(hr_df["heart_rate"].iloc[-1])
            col1.metric("Heart Rate", f"{latest_hr} bpm")
        else:
            col1.metric("Heart Rate", "Waiting...")

        if not spo2_df.empty:
            latest_spo2 = int(spo2_df["spo2"].iloc[-1])
            col2.metric("SpO₂", f"{latest_spo2}%")
        else:
            col2.metric("SpO₂", "Waiting...")

        col3.metric("Rows Logged", len(df))
        col4.metric("Valid HR Rows", len(hr_df))

        st.subheader("Heart Rate Trend")
        if not hr_df.empty:
            st.line_chart(hr_df.set_index("timestamp")["heart_rate"])
        else:
            st.info("Waiting for valid heart rate data.")

        st.subheader("SpO₂ Trend")
        if not spo2_df.empty:
            st.line_chart(spo2_df.set_index("timestamp")["spo2"])
        else:
            st.info("Waiting for valid SpO₂ data.")

        st.subheader("Raw Bluetooth Packets")
        st.dataframe(df.tail(25), width="stretch")

    except Exception as e:
        st.warning(f"Waiting for data or fixing file read issue: {e}")


render_live_dashboard()
