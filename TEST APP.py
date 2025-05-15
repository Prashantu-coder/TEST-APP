import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- Page Setup ---
st.set_page_config(page_title="Quantexo", layout="wide")

# Custom CSS
st.markdown("""
    <style>
    .stApp { background-color: #1a1a1a; }
    .stSelectbox, .stTextInput, .stButton>button {
        background-color: #2d2d2d !important;
        color: white !important;
        border-color: #444 !important;
    }
    </style>
    <div style='color:white;padding:1rem;background-color:#1a1a1a;border-bottom:1px solid #444'>
        <div style='font-size:2.5rem;font-weight:bold'>Quantexo🕵️</div>
        <div style='font-size:1.2rem;color:#aaa'>💰 Advanced Insights for Bold Trades</div>
    </div>
    """, unsafe_allow_html=True)

# --- Company Search ---
companies = {"HIDCL", "NIBL", "NICA", "NMB", "SCB"}  # Sample companies
company_symbol = st.selectbox("🔍 Select Company", [""] + sorted(list(companies)), index=0)

if not company_symbol:
    st.info("ℹ Select a company to analyze")
    st.stop()

@st.cache_data(ttl=3600)
def get_sheet_data(symbol):
    try:
        sheet_url = "https://docs.google.com/spreadsheets/d/1Q_En7VGGfifDmn5xuiF-t_02doPpwl4PLzxb4TBCW0Q/export?format=csv&gid=0"
        df = pd.read_csv(sheet_url).iloc[:, :7]
        df.columns = ['date', 'symbol', 'open', 'high', 'low', 'close', 'volume']
        df['symbol'] = df['symbol'].astype(str).str.strip().str.upper()
        return df[df['symbol'] == symbol.upper()]
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = get_sheet_data(company_symbol)
if df.empty:
    st.warning("No data available for this company")
    st.stop()

# Data Processing
df['date'] = pd.to_datetime(df['date'])
for col in ['open', 'high', 'low', 'close']:
    df[col] = pd.to_numeric(df[col], errors='coerce')
df['volume'] = df['volume'].astype(str).str.replace(',', '').astype(float)
df = df.dropna().sort_values('date')

# Signal Detection
df['point_change'] = df['close'].diff()
df['tag'] = ''
window_size = min(20, len(df)//2)
avg_volume = df['volume'].rolling(window=window_size).mean().fillna(df['volume'].mean())

for i in range(1, len(df)):
    row = df.iloc[i]
    prev = df.iloc[i-1]
    body = abs(row['close'] - row['open'])
    prev_body = abs(prev['close'] - prev['open'])
    
    # Bullish Signals
    if row['close'] > row['open']:
        if (row['close'] >= row['high'] - (row['high'] - row['low'])*0.1 and 
            row['volume'] > avg_volume[i] * 1.5 and 
            body > prev_body):
            df.at[i, 'tag'] = '🟢'
        elif body > (row['high'] - row['low'])*0.7 and row['volume'] > avg_volume[i]*2:
            df.at[i, 'tag'] = '🐂'
    
    # Bearish Signals
    elif row['open'] > row['close']:
        if (row['close'] <= row['low'] + (row['high'] - row['low'])*0.1 and 
            row['volume'] > avg_volume[i] * 1.5 and 
            body > prev_body):
            df.at[i, 'tag'] = '🔴'
        elif body > (row['high'] - row['low'])*0.7 and row['volume'] > avg_volume[i]*2:
            df.at[i, 'tag'] = '🐻'

# Visualization
fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df['date'], y=df['close'],
    mode='lines', name='Price',
    line=dict(color='#4CAF50', width=2),
    hovertemplate="Date: %{x|%Y-%m-%d}<br>Price: %{y:.2f}<extra></extra>"
))

signals = df[df['tag'] != '']
fig.add_trace(go.Scatter(
    x=signals['date'], y=signals['close'],
    mode='markers+text',
    name='Signals',
    text=signals['tag'],
    textposition='top center',
    marker=dict(size=14, color='white'),
    hovertemplate="Signal: %{text}<extra></extra>"
))

fig.update_layout(
    plot_bgcolor='#2d2d2d',
    paper_bgcolor='#1a1a1a',
    font_color='white',
    xaxis=dict(showgrid=False),
    yaxis=dict(showgrid=True, gridcolor='#444'),
    margin=dict(l=20, r=20, t=40, b=20)
)

st.plotly_chart(fig, use_container_width=True)