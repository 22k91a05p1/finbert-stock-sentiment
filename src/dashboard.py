import sys
import os
import random
from datetime import datetime, timedelta

# 1. Fix path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import streamlit as st
import pandas as pd
import plotly.express as px

# Try importing DB, but handle failure gracefully
try:
    from src.database import get_db_engine
    DB_AVAILABLE = True
except:
    DB_AVAILABLE = False

# -----------------------------------------------------------------------------
# 2. PAGE CONFIG
# -----------------------------------------------------------------------------
st.set_page_config(page_title="Market Sentiment AI", page_icon="🤖", layout="wide")

# -----------------------------------------------------------------------------
# 3. DATA LOADING (Smart Fallback)
# -----------------------------------------------------------------------------
def generate_mock_data():
    """Generates fake data for Demo Mode so the app looks good on Cloud."""
    titles = [
        "NVIDIA creates new AI chip, stock soars",
        "Fed announces interest rate hike fears",
        "Tesla releases new model, mixed reviews",
        "Google cloud revenue jumps 20%",
        "Market crash incoming? Experts warn of bubble",
        "Apple vision pro sales exceed expectations",
        "Amazon lays off 500 employees in Alexa division"
    ]
    sentiments = ['positive', 'negative', 'neutral']
    
    data = []
    now = datetime.now()
    for i in range(20):
        data.append({
            'date': now - timedelta(hours=i),
            'title': random.choice(titles),
            'sentiment': random.choice(sentiments),
            'confidence': random.uniform(0.7, 0.99)
        })
    return pd.DataFrame(data)

def load_data():
    """Tries to load from DB; falls back to Mock Data if DB fails."""
    if DB_AVAILABLE:
        try:
            engine = get_db_engine()
            df = pd.read_sql("SELECT * FROM sentiment_data ORDER BY date DESC", engine)
            if not df.empty:
                return df
        except Exception:
            pass  # Fall through to mock data
    
    # If we reach here, DB failed or is empty. Return Mock Data.
    st.toast("⚠️ Database unreachable. Switched to DEMO MODE.", icon="⚠️")
    return generate_mock_data()

# -----------------------------------------------------------------------------
# 4. DASHBOARD UI
# -----------------------------------------------------------------------------
st.title("🤖 AI Stock Sentiment Tracker")

# Load Data
df = load_data()

# --- METRICS ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Posts Analyzed", len(df))
col2.metric("Positive Signals", len(df[df['sentiment'] == 'positive']), delta="Bullish")
col3.metric("Negative Signals", len(df[df['sentiment'] == 'negative']), delta="- Bearish", delta_color="inverse")
col4.metric("Avg Confidence", f"{df['confidence'].mean():.1%}")

st.markdown("---")

# --- CHARTS ---
col_left, col_right = st.columns([2, 1])
color_map = {"positive": "#00CC96", "negative": "#EF553B", "neutral": "#636EFA"}

with col_left:
    st.subheader("📊 Sentiment Trend")
    fig_line = px.line(df, x='date', y='confidence', color='sentiment', 
                       color_discrete_map=color_map, markers=True)
    st.plotly_chart(fig_line, use_container_width=True)

with col_right:
    st.subheader("🍩 Sentiment Split")
    fig_pie = px.pie(df, names='sentiment', color='sentiment', 
                     color_discrete_map=color_map, hole=0.4)
    st.plotly_chart(fig_pie, use_container_width=True)

# --- TABLE ---
st.subheader("📝 Live Feed")
st.dataframe(df[['sentiment', 'confidence', 'title', 'date']], use_container_width=True, hide_index=True)