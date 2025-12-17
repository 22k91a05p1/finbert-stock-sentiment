import sys
import os
# 1. Fix the path first so imports work
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px
from src.database import get_db_engine

# -----------------------------------------------------------------------------
# 2. PAGE CONFIGURATION
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Market Sentiment AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------------------------------
# 3. LOAD DATA FROM DATABASE
# -----------------------------------------------------------------------------
def load_data():
    try:
        engine = get_db_engine()
        # Read the data you scraped from the database
        df = pd.read_sql("SELECT * FROM sentiment_data ORDER BY date DESC", engine)
        return df
    except Exception as e:
        st.error(f"Error connecting to database: {e}")
        return pd.DataFrame()

# -----------------------------------------------------------------------------
# 4. SIDEBAR
# -----------------------------------------------------------------------------
with st.sidebar:
    st.title("🎛️ Controls")
    
    if st.button("🔄 Refresh Data", use_container_width=True):
        st.cache_data.clear()
        st.rerun()
        
    st.divider()
    st.info("This dashboard tracks real-time stock sentiment using FinBERT.")

# -----------------------------------------------------------------------------
# 5. MAIN DASHBOARD
# -----------------------------------------------------------------------------
st.title("🤖 AI Stock Sentiment Tracker")
st.markdown("### Real-time analysis of r/WallStreetBets discussions")

# Load the data
df = load_data()

if not df.empty:
    # --- TOP ROW: METRICS ---
    with st.container():
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Total Posts Analyzed", len(df))
        
        pos_count = len(df[df['sentiment'] == 'positive'])
        col2.metric("Positive Signals", pos_count, delta="Bullish", delta_color="normal")
        
        neg_count = len(df[df['sentiment'] == 'negative'])
        col3.metric("Negative Signals", neg_count, delta="- Bearish", delta_color="inverse")
        
        avg_conf = df['confidence'].mean()
        col4.metric("AI Confidence Score", f"{avg_conf:.1%}")

    st.markdown("---")

    # --- MIDDLE ROW: CHARTS ---
    col_left, col_right = st.columns([2, 1])

    with col_left:
        st.subheader("📊 Sentiment Trend Over Time")
        # Line Chart
        color_map = {"positive": "#00CC96", "negative": "#EF553B", "neutral": "#636EFA"}
        fig_line = px.line(df, x='date', y='confidence', color='sentiment', 
                           color_discrete_map=color_map, markers=True)
        st.plotly_chart(fig_line, use_container_width=True)

    with col_right:
        st.subheader("🍩 Sentiment Split")
        # --- FIXED THIS LINE BELOW (px.pie instead of px.donut) ---
        fig_pie = px.pie(df, names='sentiment', color='sentiment', 
                         color_discrete_map=color_map, hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)

    # --- BOTTOM ROW: DATA TABLE ---
    st.subheader("📝 Live Feed")
    st.dataframe(
        df[['sentiment', 'confidence', 'title', 'date']],
        use_container_width=True,
        column_config={
            "sentiment": st.column_config.TextColumn("Sentiment", width="small"),
            "confidence": st.column_config.ProgressColumn("AI Confidence", format="%.2f", min_value=0, max_value=1),
            "title": st.column_config.TextColumn("Discussion Title", width="large"),
            "date": st.column_config.DatetimeColumn("Time", format="D MMM HH:mm"),
        },
        hide_index=True,
    )

else:
    st.warning("Waiting for data... Run your pipeline (`poetry run python -m src.main`) to fetch news.")