"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  NSE MARKET INTELLIGENCE TERMINAL — ULTIMATE EDITION v3.0                  ║
║  A production-grade, full-spectrum trading & analytics platform.           ║
║                                                                            ║
║  Modules:                                                                  ║
║    1.  Market Command Center (Movers, Breadth, FII/DII)                    ║
║    2.  Sectoral Rotation Engine                                            ║
║    3.  Advanced Seasonality (with statistical significance)                ║
║    4.  Multi-MA Crossover + Pattern Screener                               ║
║    5.  Portfolio Optimizer (Efficient Frontier + Risk Budgeting)           ║
║    6.  Correlation & Clustering Scanner                                    ║
║    7.  Probability, Volatility & Monte Carlo Engine                        ║
║    8.  Option Chain, Greeks & Strategy Builder                             ║
║    9.  IPO Intelligence Dashboard                                          ║
║   10.  Technical Analysis Workbench (Candlesticks, Indicators, S/R)        ║
║   11.  Risk Management Suite (VaR, Drawdown, Kelly, Position Sizing)       ║
║   12.  Watchlist & Alerts                                                  ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import stats
from scipy.optimize import minimize
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
from itertools import combinations
import datetime
import calendar
import math
import requests
import warnings
import json
import hashlib
from functools import lru_cache
from typing import Dict, List, Tuple, Optional

warnings.filterwarnings('ignore')

# ==============================================================================
# PAGE CONFIG & GLOBAL THEME
# ==============================================================================
st.set_page_config(
    page_title="NSE Intelligence Terminal v3.0",
    layout="wide",
    page_icon="📈",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional dark-theme terminal look
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@300;400;500;700&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    :root {
        --bg-primary: #0d1117;
        --bg-secondary: #161b22;
        --bg-tertiary: #21262d;
        --border-color: #30363d;
        --text-primary: #e6edf3;
        --text-secondary: #8b949e;
        --accent-green: #00c48c;
        --accent-red: #ff4d6d;
        --accent-blue: #58a6ff;
        --accent-gold: #e3b341;
        --accent-purple: #bc8cff;
    }

    .stApp {
        background-color: var(--bg-primary);
        font-family: 'Inter', sans-serif;
    }

    .main .block-container {
        padding-top: 1rem;
        padding-bottom: 2rem;
        max-width: 1600px;
    }

    h1, h2, h3, h4, h5, h6 {
        font-family: 'Inter', sans-serif;
        font-weight: 700;
        color: var(--text-primary);
    }

    h1 { font-size: 2.2rem; letter-spacing: -0.02em; }
    h2 { font-size: 1.6rem; }
    h3 { font-size: 1.3rem; }

    .stMetric {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 16px 20px;
        transition: all 0.3s ease;
    }
    .stMetric:hover {
        border-color: var(--accent-blue);
        box-shadow: 0 0 20px rgba(88,166,255,0.1);
    }

    [data-testid="stMetricValue"] {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.5rem;
        font-weight: 700;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.8rem;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: var(--text-secondary);
    }

    .stDataFrame {
        border: 1px solid var(--border-color);
        border-radius: 12px;
        overflow: hidden;
    }

    .stButton > button {
        background: linear-gradient(135deg, #238636, #2ea043);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 24px;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        box-shadow: 0 2px 8px rgba(46,160,67,0.3);
    }
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 16px rgba(46,160,67,0.4);
    }

    .stSelectbox > div > div {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 8px;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
        background: var(--bg-secondary);
        border-radius: 12px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background: var(--accent-blue) !important;
        color: white !important;
    }

    .terminal-header {
        background: linear-gradient(135deg, var(--bg-secondary), var(--bg-tertiary));
        border: 1px solid var(--border-color);
        border-radius: 16px;
        padding: 24px 32px;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }
    .terminal-header::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-green), var(--accent-blue), var(--accent-purple));
    }
    .terminal-header h1 {
        margin: 0;
        background: linear-gradient(135deg, #fff, #a0c4ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .terminal-header .subtitle {
        color: var(--text-secondary);
        font-size: 0.9rem;
        margin-top: 4px;
    }

    .signal-badge {
        display: inline-block;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .signal-bullish { background: rgba(0,196,140,0.15); color: var(--accent-green); border: 1px solid rgba(0,196,140,0.3); }
    .signal-bearish { background: rgba(255,77,109,0.15); color: var(--accent-red); border: 1px solid rgba(255,77,109,0.3); }
    .signal-neutral { background: rgba(227,179,65,0.15); color: var(--accent-gold); border: 1px solid rgba(227,179,65,0.3); }

    .card {
        background: var(--bg-secondary);
        border: 1px solid var(--border-color);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 16px;
    }

    .glow-green { text-shadow: 0 0 10px rgba(0,196,140,0.5); }
    .glow-red { text-shadow: 0 0 10px rgba(255,77,109,0.5); }

    div[data-testid="stSidebar"] {
        background: var(--bg-secondary);
        border-right: 1px solid var(--border-color);
    }

    .stProgress > div > div > div {
        background: linear-gradient(90deg, var(--accent-green), var(--accent-blue));
        border-radius: 4px;
    }

    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-track { background: var(--bg-primary); }
    ::-webkit-scrollbar-thumb { background: var(--border-color); border-radius: 4px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--text-secondary); }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# CONFIGURATION & UNIVERSE
# ==============================================================================
TICKER_LIST = [
    "BHARTIARTL.NS", "HDFCBANK.NS", "KAYNES.NS", "VEDL.NS", "ADANIENT.NS", "BSE.NS", "RELIANCE.NS", "ICICIBANK.NS", "INFY.NS",
    "SBIN.NS", "HAL.NS", "CIPLA.NS", "MCX.NS", "TCS.NS", "IDEA.NS", "LT.NS", "SAIL.NS", "DIXON.NS", "ADANIPOWER.NS", "BHEL.NS",
    "SHRIRAMFIN.NS", "OIL.NS", "TATASTEEL.NS", "AXISBANK.NS", "ETERNAL.NS", "ADANIGREEN.NS", "ONGC.NS", "M&M.NS", "ASHOKLEY.NS",
    "HCLTECH.NS", "TVSMOTOR.NS", "BAJFINANCE.NS", "HINDALCO.NS", "ADANIPORTS.NS", "COALINDIA.NS", "ADANIENSOL.NS", "SOLARINDS.NS",
    "GRASIM.NS", "TITAN.NS", "ZYDUSLIFE.NS", "SUNPHARMA.NS", "BAJAJ-AUTO.NS", "VMM.NS", "JSWSTEEL.NS", "HINDZINC.NS", "POWERINDIA.NS",
    "POWERGRID.NS", "BEL.NS", "KOTAKBANK.NS", "HINDPETRO.NS", "INDUSTOWER.NS", "JIOFIN.NS", "COFORGE.NS", "SUZLON.NS", "MARUTI.NS",
    "NATIONALUM.NS", "KALYANKJIL.NS", "NMDC.NS", "CANBK.NS", "BAJAJFINSV.NS", "CROMPTON.NS", "PERSISTENT.NS", "DLF.NS", "APOLLOHOSP.NS",
    "SWIGGY.NS", "BPCL.NS", "POLICYBZR.NS", "WIPRO.NS", "ITC.NS", "BIOCON.NS", "POLYCAB.NS", "LUPIN.NS", "CDSL.NS", "INDIGO.NS",
    "TECHM.NS", "EICHERMOT.NS", "HINDUNILVR.NS", "LAURUSLABS.NS", "DRREDDY.NS", "SAMMAANCAP.NS", "BANKBARODA.NS", "LTM.NS",
    "HEROMOTOCO.NS", "DIVISLAB.NS", "NTPC.NS", "LICHSGFIN.NS", "MAZDOCK.NS", "SIEMENS.NS", "PFC.NS", "TRENT.NS", "ASIANPAINT.NS",
    "TMPV.NS", "COCHINSHIP.NS", "ULTRACEMCO.NS", "ANGELONE.NS", "TIINDIA.NS", "FEDERALBNK.NS", "WAAREEENER.NS", "CGPOWER.NS",
    "LTF.NS", "TATAPOWER.NS", "IDFCFIRSTB.NS", "BHARATFORG.NS", "GODFRYPHLP.NS", "AMBER.NS", "PAYTM.NS", "GLENMARK.NS", "FORCEMOT.NS",
    "VBL.NS", "YESBANK.NS", "MUTHOOTFIN.NS", "UNIONBANK.NS", "INDHOTEL.NS", "ABB.NS", "CHOLAFIN.NS", "IOC.NS", "KEI.NS", "MAXHEALTH.NS",
    "HDFCLIFE.NS", "GODREJCP.NS", "IRFC.NS", "INDIANB.NS", "RECLTD.NS", "NESTLEIND.NS", "BRITANNIA.NS", "AUROPHARMA.NS", "PIDILITIND.NS",
    "MPHASIS.NS", "FORTIS.NS", "HDFCAMC.NS", "CUMMINSIND.NS", "TATACONSUM.NS", "INDUSINDBK.NS", "PNB.NS", "RBLBANK.NS", "BANDHANBNK.NS",
    "AMBUJACEM.NS", "PIIND.NS", "RVNL.NS", "OFSS.NS", "VOLTAS.NS", "ABCAPITAL.NS", "SBILIFE.NS", "NAM-INDIA.NS", "PGEL.NS", "KPITTECH.NS",
    "JINDALSTEL.NS", "NBCC.NS", "MFSL.NS", "BANKINDIA.NS", "DMART.NS", "SBICARD.NS", "BLUESTARCO.NS", "GODREJPROP.NS", "AUBANK.NS",
    "GAIL.NS", "NYKAA.NS", "MANKIND.NS", "LICI.NS", "KFINTECH.NS", "MOTHERSON.NS", "IREDA.NS", "TATAELXSI.NS", "BDL.NS", "TORNTPHARM.NS",
    "LODHA.NS", "NAUKRI.NS", "HYUNDAI.NS", "NUVAMA.NS", "UPL.NS", "JSWENERGY.NS", "MARICO.NS", "DABUR.NS", "DALBHARAT.NS", "INOXWIND.NS",
    "CAMS.NS", "UNOMINDA.NS", "MANAPPURAM.NS", "NHPC.NS", "BOSCHLTD.NS", "PAGEIND.NS", "GMRAIRPORT.NS", "UNITDSPR.NS", "SONACOMS.NS",
    "SRF.NS", "APLAPOLLO.NS", "PHOENIXLTD.NS", "PATANJALI.NS", "DELHIVERY.NS", "ICICIGI.NS", "HAVELLS.NS", "EXIDEIND.NS", "BAJAJHLDNG.NS",
    "PNBHOUSING.NS", "MOTILALOFS.NS", "IEX.NS", "PRESTIGE.NS", "JUBLFOOD.NS", "PREMIERENE.NS", "ASTRAL.NS", "360ONE.NS", "ALKEM.NS",
    "SUPREMEIND.NS", "OBEROIRLTY.NS", "ICICIPRULI.NS", "CONCOR.NS", "SHREECEM.NS", "COLPAL.NS", "PETRONET.NS"
]

SECTOR_MAP = {
    "HDFCBANK.NS":"Banking", "ICICIBANK.NS":"Banking", "SBIN.NS":"Banking", "AXISBANK.NS":"Banking",
    "KOTAKBANK.NS":"Banking", "BANKBARODA.NS":"Banking", "CANBK.NS":"Banking", "PNB.NS":"Banking",
    "UNIONBANK.NS":"Banking", "INDIANB.NS":"Banking", "BANKINDIA.NS":"Banking", "FEDERALBNK.NS":"Banking",
    "YESBANK.NS":"Banking", "RBLBANK.NS":"Banking", "IDFCFIRSTB.NS":"Banking", "INDUSINDBK.NS":"Banking",
    "BANDHANBNK.NS":"Banking", "AUBANK.NS":"Banking", "BAJFINANCE.NS":"NBFC", "BAJAJFINSV.NS":"NBFC",
    "SHRIRAMFIN.NS":"NBFC", "CHOLAFIN.NS":"NBFC", "MUTHOOTFIN.NS":"NBFC", "MANAPPURAM.NS":"NBFC",
    "ABCAPITAL.NS":"NBFC", "LTF.NS":"NBFC", "LICHSGFIN.NS":"NBFC", "PNBHOUSING.NS":"NBFC",
    "JIOFIN.NS":"NBFC", "SAMMAANCAP.NS":"NBFC", "HDFCLIFE.NS":"Insurance", "SBILIFE.NS":"Insurance",
    "LICI.NS":"Insurance", "ICICIGI.NS":"Insurance", "ICICIPRULI.NS":"Insurance", "MAXHEALTH.NS":"Insurance",
    "MFSL.NS":"Insurance", "POLICYBZR.NS":"Insurance", "BSE.NS":"Capital Mkts", "MCX.NS":"Capital Mkts",
    "CDSL.NS":"Capital Mkts", "ANGELONE.NS":"Capital Mkts", "HDFCAMC.NS":"Capital Mkts", "NAM-INDIA.NS":"Capital Mkts",
    "MOTILALOFS.NS":"Capital Mkts", "NUVAMA.NS":"Capital Mkts", "360ONE.NS":"Capital Mkts", "KFINTECH.NS":"Capital Mkts",
    "CAMS.NS":"Capital Mkts", "IEX.NS":"Capital Mkts", "BAJAJHLDNG.NS":"Capital Mkts", "INFY.NS":"IT", "TCS.NS":"IT",
    "HCLTECH.NS":"IT", "WIPRO.NS":"IT", "TECHM.NS":"IT", "COFORGE.NS":"IT", "PERSISTENT.NS":"IT", "MPHASIS.NS":"IT",
    "KPITTECH.NS":"IT", "TATAELXSI.NS":"IT", "OFSS.NS":"IT", "NAUKRI.NS":"IT", "PAYTM.NS":"IT", "NYKAA.NS":"IT",
    "DELHIVERY.NS":"IT", "SWIGGY.NS":"IT", "BHARTIARTL.NS":"Telecom", "IDEA.NS":"Telecom", "INDUSTOWER.NS":"Telecom",
    "RELIANCE.NS":"Oil & Gas", "ONGC.NS":"Oil & Gas", "OIL.NS":"Oil & Gas", "BPCL.NS":"Oil & Gas",
    "HINDPETRO.NS":"Oil & Gas", "IOC.NS":"Oil & Gas", "GAIL.NS":"Oil & Gas", "PETRONET.NS":"Oil & Gas",
    "TATASTEEL.NS":"Metals", "JSWSTEEL.NS":"Metals", "HINDALCO.NS":"Metals", "VEDL.NS":"Metals", "SAIL.NS":"Metals",
    "NMDC.NS":"Metals", "NATIONALUM.NS":"Metals", "HINDZINC.NS":"Metals", "COALINDIA.NS":"Metals",
    "APLAPOLLO.NS":"Metals", "JINDALSTEL.NS":"Metals", "ADANIPOWER.NS":"Power", "ADANIGREEN.NS":"Power",
    "ADANIENSOL.NS":"Power", "TATAPOWER.NS":"Power", "NTPC.NS":"Power", "POWERGRID.NS":"Power",
    "POWERINDIA.NS":"Power", "NHPC.NS":"Power", "JSWENERGY.NS":"Power", "IREDA.NS":"Power", "SUZLON.NS":"Power",
    "WAAREEENER.NS":"Power", "INOXWIND.NS":"Power", "PREMIERENE.NS":"Power", "SOLARINDS.NS":"Power",
    "LT.NS":"Infra", "ADANIPORTS.NS":"Infra", "ADANIENT.NS":"Infra", "RVNL.NS":"Infra", "NBCC.NS":"Infra",
    "IRFC.NS":"Infra", "PFC.NS":"Infra", "RECLTD.NS":"Infra", "GMRAIRPORT.NS":"Infra", "CONCOR.NS":"Infra",
    "HAL.NS":"Defence", "BEL.NS":"Defence", "BHEL.NS":"Defence", "MAZDOCK.NS":"Defence", "COCHINSHIP.NS":"Defence",
    "BDL.NS":"Defence", "TIINDIA.NS":"Defence", "CIPLA.NS":"Pharma", "SUNPHARMA.NS":"Pharma", "ZYDUSLIFE.NS":"Pharma",
    "DRREDDY.NS":"Pharma", "LUPIN.NS":"Pharma", "BIOCON.NS":"Pharma", "DIVISLAB.NS":"Pharma", "LAURUSLABS.NS":"Pharma",
    "AUROPHARMA.NS":"Pharma", "GLENMARK.NS":"Pharma", "ALKEM.NS":"Pharma", "TORNTPHARM.NS":"Pharma",
    "APOLLOHOSP.NS":"Pharma", "FORTIS.NS":"Pharma", "MANKIND.NS":"Pharma", "PIIND.NS":"Pharma",
    "MARUTI.NS":"Auto", "M&M.NS":"Auto", "BAJAJ-AUTO.NS":"Auto", "TVSMOTOR.NS":"Auto", "HEROMOTOCO.NS":"Auto",
    "ASHOKLEY.NS":"Auto", "EICHERMOT.NS":"Auto", "FORCEMOT.NS":"Auto", "HYUNDAI.NS":"Auto", "MOTHERSON.NS":"Auto",
    "BOSCHLTD.NS":"Auto", "BHARATFORG.NS":"Auto", "SONACOMS.NS":"Auto", "UNOMINDA.NS":"Auto", "EXIDEIND.NS":"Auto",
    "ITC.NS":"FMCG", "HINDUNILVR.NS":"FMCG", "NESTLEIND.NS":"FMCG", "BRITANNIA.NS":"FMCG", "DABUR.NS":"FMCG",
    "MARICO.NS":"FMCG", "GODREJCP.NS":"FMCG", "COLPAL.NS":"FMCG", "VBL.NS":"FMCG", "TATACONSUM.NS":"FMCG",
    "PATANJALI.NS":"FMCG", "UNITDSPR.NS":"FMCG", "GODFRYPHLP.NS":"FMCG", "PAGEIND.NS":"FMCG",
    "DLF.NS":"Real Estate", "GODREJPROP.NS":"Real Estate", "LODHA.NS":"Real Estate", "OBEROIRLTY.NS":"Real Estate",
    "PRESTIGE.NS":"Real Estate", "PHOENIXLTD.NS":"Real Estate", "ULTRACEMCO.NS":"Cement", "SHREECEM.NS":"Cement",
    "AMBUJACEM.NS":"Cement", "DALBHARAT.NS":"Cement", "GRASIM.NS":"Cement", "ASTRAL.NS":"Cement",
    "SUPREMEIND.NS":"Cement", "PIDILITIND.NS":"Cement", "SRF.NS":"Cement", "UPL.NS":"Cement",
    "TITAN.NS":"Durables", "TRENT.NS":"Durables", "ASIANPAINT.NS":"Durables", "HAVELLS.NS":"Durables",
    "POLYCAB.NS":"Durables", "CGPOWER.NS":"Durables", "VOLTAS.NS":"Durables", "CROMPTON.NS":"Durables",
    "BLUESTARCO.NS":"Durables", "AMBER.NS":"Durables", "DIXON.NS":"Durables", "KAYNES.NS":"Durables",
    "KALYANKJIL.NS":"Durables", "DMART.NS":"Durables", "KEI.NS":"Durables", "ABB.NS":"Durables",
    "SIEMENS.NS":"Durables", "CUMMINSIND.NS":"Durables", "INDIGO.NS":"Travel", "INDHOTEL.NS":"Travel",
    "JUBLFOOD.NS":"Travel", "VMM.NS":"Others", "TMPV.NS":"Others", "PGEL.NS":"Others", "LTM.NS":"Others",
    "SBICARD.NS":"Others", "ETERNAL.NS":"Others"
}

TRADING_DAYS = 252
RISK_FREE_RATE = 0.065

# ==============================================================================
# DATA LAYER — Caching & Fetching
# ==============================================================================
@st.cache_data(ttl=3600, show_spinner=False)
def fetch_data(tickers, period, interval="1d"):
    """Fetch OHLCV data with automatic retry and error handling."""
    try:
        data = yf.download(tickers, period=period, interval=interval, progress=False, auto_adjust=True)
        return data
    except Exception as e:
        st.error(f"Data fetch error: {e}")
        return pd.DataFrame()


@st.cache_data(ttl=3600, show_spinner=False)
def fetch_single_ticker(ticker, period="2y", interval="1d"):
    """Fetch single ticker with full OHLCV."""
    try:
        t = yf.Ticker(ticker)
        df = t.history(period=period, interval=interval)
        return df
    except Exception:
        return pd.DataFrame()


# ==============================================================================
# TECHNICAL INDICATORS ENGINE
# ==============================================================================
def calc_rsi(series, period=14):
    delta = series.diff()
    gain = delta.where(delta > 0, 0.0)
    loss = -delta.where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period, min_periods=period).mean()
    avg_loss = loss.rolling(window=period, min_periods=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100 - (100 / (1 + rs))
    return rsi


def calc_macd(series, fast=12, slow=26, signal=9):
    ema_fast = series.ewm(span=fast, adjust=False).mean()
    ema_slow = series.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line
    return macd_line, signal_line, histogram


def calc_bollinger(series, period=20, std_dev=2):
    sma = series.rolling(window=period).mean()
    std = series.rolling(window=period).std()
    upper = sma + std_dev * std
    lower = sma - std_dev * std
    return upper, sma, lower


def calc_atr(high, low, close, period=14):
    tr1 = high - low
    tr2 = abs(high - close.shift(1))
    tr3 = abs(low - close.shift(1))
    tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    return atr


def calc_vwap(df):
    """Volume Weighted Average Price."""
    if 'Volume' not in df.columns:
        return pd.Series(np.nan, index=df.index)
    typical_price = (df['High'] + df['Low'] + df['Close']) / 3
    cum_vol = df['Volume'].cumsum()
    cum_tp_vol = (typical_price * df['Volume']).cumsum()
    vwap = cum_tp_vol / cum_vol.replace(0, np.nan)
    return vwap


def calc_obv(df):
    """On-Balance Volume."""
    obv = [0]
    for i in range(1, len(df)):
        if df['Close'].iloc[i] > df['Close'].iloc[i-1]:
            obv.append(obv[-1] + df['Volume'].iloc[i])
        elif df['Close'].iloc[i] < df['Close'].iloc[i-1]:
            obv.append(obv[-1] - df['Volume'].iloc[i])
        else:
            obv.append(obv[-1])
    return pd.Series(obv, index=df.index)


def calc_stochastic(high, low, close, k_period=14, d_period=3):
    lowest_low = low.rolling(window=k_period).min()
    highest_high = high.rolling(window=k_period).max()
    k = 100 * (close - lowest_low) / (highest_high - lowest_low).replace(0, np.nan)
    d = k.rolling(window=d_period).mean()
    return k, d


def calc_adx(high, low, close, period=14):
    """Average Directional Index."""
    plus_dm = high.diff()
    minus_dm = -low.diff()
    plus_dm[plus_dm < 0] = 0
    minus_dm[minus_dm < 0] = 0
    plus_dm[(plus_dm - minus_dm) <= 0] = 0
    minus_dm[(minus_dm - plus_dm) <= 0] = 0
    
    tr = pd.concat([high - low, abs(high - close.shift(1)), abs(low - close.shift(1))], axis=1).max(axis=1)
    atr = tr.rolling(window=period).mean()
    
    plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr.replace(0, np.nan))
    minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr.replace(0, np.nan))
    
    dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di).replace(0, np.nan)
    adx = dx.rolling(window=period).mean()
    return adx, plus_di, minus_di


def calc_fibonacci_levels(high, low):
    """Calculate Fibonacci retracement levels."""
    diff = high - low
    levels = {
        '0.0% (High)': high,
        '23.6%': high - 0.236 * diff,
        '38.2%': high - 0.382 * diff,
        '50.0%': high - 0.500 * diff,
        '61.8%': high - 0.618 * diff,
        '78.6%': high - 0.786 * diff,
        '100.0% (Low)': low,
    }
    return levels


def calc_pivot_points(high, low, close):
    """Classic Pivot Points."""
    pp = (high + low + close) / 3
    r1 = 2 * pp - low
    s1 = 2 * pp - high
    r2 = pp + (high - low)
    s2 = pp - (high - low)
    r3 = high + 2 * (pp - low)
    s3 = low - 2 * (high - pp)
    return {'PP': pp, 'R1': r1, 'R2': r2, 'R3': r3, 'S1': s1, 'S2': s2, 'S3': s3}


def detect_support_resistance(df, window=20, num_levels=5):
    """Detect support/resistance using local minima/maxima."""
    highs = df['High'].values
    lows = df['Low'].values
    
    resistance_levels = []
    support_levels = []
    
    for i in range(window, len(df) - window):
        if highs[i] == max(highs[i-window:i+window+1]):
            resistance_levels.append(highs[i])
        if lows[i] == min(lows[i-window:i+window+1]):
            support_levels.append(lows[i])
    
    # Cluster nearby levels
    def cluster_levels(levels, tolerance=0.02):
        if not levels:
            return []
        levels = sorted(levels)
        clusters = [[levels[0]]]
        for l in levels[1:]:
            if abs(l - clusters[-1][-1]) / clusters[-1][-1] < tolerance:
                clusters[-1].append(l)
            else:
                clusters.append([l])
        return [np.mean(c) for c in clusters]
    
    resistances = cluster_levels(resistance_levels)[-num_levels:]
    supports = cluster_levels(support_levels)[-num_levels:]
    return supports, resistances


# ==============================================================================
# RISK METRICS ENGINE
# ==============================================================================
def calc_var(returns, confidence=0.95, method='historical'):
    """Value at Risk."""
    if method == 'historical':
        return np.percentile(returns, (1 - confidence) * 100)
    elif method == 'parametric':
        mu = returns.mean()
        sigma = returns.std()
        z = stats.norm.ppf(1 - confidence)
        return mu + z * sigma
    return 0


def calc_cvar(returns, confidence=0.95):
    """Conditional VaR (Expected Shortfall)."""
    var = calc_var(returns, confidence)
    return returns[returns <= var].mean()


def calc_max_drawdown(series):
    """Maximum Drawdown."""
    peak = series.cummax()
    drawdown = (series - peak) / peak
    return drawdown.min()


def calc_calmar_ratio(returns, series):
    """Calmar Ratio = Annualized Return / Max Drawdown."""
    ann_ret = returns.mean() * TRADING_DAYS
    mdd = abs(calc_max_drawdown(series))
    return ann_ret / mdd if mdd != 0 else 0


def calc_sortino_ratio(returns, rf=RISK_FREE_RATE):
    """Sortino Ratio (downside deviation only)."""
    excess = returns - rf / TRADING_DAYS
    downside = excess[excess < 0]
    downside_std = downside.std() * np.sqrt(TRADING_DAYS)
    ann_ret = excess.mean() * TRADING_DAYS
    return ann_ret / downside_std if downside_std > 0 else 0


def calc_kelly_fraction(win_rate, avg_win, avg_loss):
    """Kelly Criterion for optimal position sizing."""
    if avg_loss == 0:
        return 0
    b = avg_win / abs(avg_loss)
    kelly = (win_rate * b - (1 - win_rate)) / b
    return max(0, min(kelly, 0.25))  # Cap at 25%


def monte_carlo_simulation(returns, initial_value=100000, days=252, simulations=10000):
    """Monte Carlo simulation for portfolio projection."""
    mu = returns.mean()
    sigma = returns.std()
    
    results = np.zeros((simulations, days))
    results[:, 0] = initial_value
    
    for t in range(1, days):
        shock = np.random.normal(mu, sigma, simulations)
        results[:, t] = results[:, t-1] * (1 + shock)
    
    return results


# ==============================================================================
# BLACK-SCHOLES & OPTIONS ENGINE
# ==============================================================================
def _norm_cdf(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def _norm_pdf(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def calc_greeks(S, K, T_days, sigma_pct, opt_type='CE', r=0.065):
    """Full Black-Scholes Greeks + pricing."""
    T = max(T_days, 1) / 365.0
    sigma = max(sigma_pct, 0.01) / 100.0
    if S <= 0 or K <= 0:
        return dict(delta=0, gamma=0, theta=0, vega=0, rho=0, theo_price=0,
                     intrinsic=0, time_value=0, moneyness='—')
    try:
        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        nd1, nd2 = _norm_cdf(d1), _norm_cdf(d2)
        nnd1, nnd2 = _norm_cdf(-d1), _norm_cdf(-d2)
        npd1 = _norm_pdf(d1)
        disc = math.exp(-r * T)
        
        if opt_type == 'CE':
            theo = S * nd1 - K * disc * nd2
            delta = nd1
            rho = K * T * disc * nd2 / 100.0
            intrinsic = max(S - K, 0.0)
            money = 'ITM' if S > K else ('ATM' if abs(S - K) / K < 0.005 else 'OTM')
        else:
            theo = K * disc * nnd2 - S * nnd1
            delta = nd1 - 1.0
            rho = -K * T * disc * nnd2 / 100.0
            intrinsic = max(K - S, 0.0)
            money = 'ITM' if S < K else ('ATM' if abs(S - K) / K < 0.005 else 'OTM')
        
        gamma = npd1 / (S * sigma * math.sqrt(T))
        vega = S * npd1 * math.sqrt(T) / 100.0
        theta = (-(S * npd1 * sigma) / (2.0 * math.sqrt(T))
                 - r * K * disc * (nd2 if opt_type == 'CE' else nnd2)) / 365.0
        time_val = max(theo - intrinsic, 0.0)
        
        return dict(delta=delta, gamma=gamma, theta=theta, vega=vega, rho=rho,
                     theo_price=theo, intrinsic=intrinsic, time_value=time_val, moneyness=money)
    except Exception:
        return dict(delta=0, gamma=0, theta=0, vega=0, rho=0, theo_price=0,
                     intrinsic=0, time_value=0, moneyness='—')


def option_payoff(strategy, strikes, premiums, spot_range):
    """Calculate option strategy payoff at expiry."""
    payoffs = np.zeros(len(spot_range))
    for i, s in enumerate(spot_range):
        total = 0
        for strike, premium, opt_type, action in zip(strikes, premiums, strategy['types'], strategy['actions']):
            if opt_type == 'CE':
                intrinsic = max(s - strike, 0)
            else:
                intrinsic = max(strike - s, 0)
            if action == 'BUY':
                total += intrinsic - premium
            else:
                total += premium - intrinsic
        payoffs[i] = total
    return payoffs


# ==============================================================================
# NSE DATA LAYER
# ==============================================================================
def get_nse_headers():
    return {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'accept-language': 'en,gu;q=0.9,hi;q=0.8',
        'accept-encoding': 'gzip, deflate',
    }

def get_nse_session():
    if 'nse_session' not in st.session_state:
        st.session_state.nse_session = requests.Session()
        try:
            st.session_state.nse_session.get('https://www.nseindia.com/option-chain', headers=get_nse_headers(), timeout=8)
        except Exception:
            pass
    return st.session_state.nse_session

def nse_get(url, retry=True):
    session = get_nse_session()
    try:
        r = session.get(url, headers=get_nse_headers(), timeout=10)
        if r.status_code == 401 and retry:
            session.get('https://www.nseindia.com/option-chain', headers=get_nse_headers(), timeout=8)
            r = session.get(url, headers=get_nse_headers(), timeout=10)
        return r
    except Exception:
        return None

@st.cache_data(ttl=300, show_spinner=False)
def fetch_nse_symbols():
    try:
        r = nse_get('https://www.nseindia.com/api/underlying-information')
        if r is not None and r.status_code == 200:
            d = r.json()
            return [x['symbol'] for x in d['data']['IndexList']], [x['symbol'] for x in d['data']['UnderlyingList']]
    except Exception:
        pass
    return ["NIFTY", "BANKNIFTY", "FINNIFTY"], [t.replace(".NS", "") for t in TICKER_LIST]

@st.cache_data(ttl=180, show_spinner=False)
def fetch_nse_expiries(symbol):
    try:
        r = nse_get(f'https://www.nseindia.com/api/option-chain-contract-info?symbol={symbol}')
        if r is not None and r.status_code == 200:
            jd = r.json()
            if 'expiryDates' in jd:
                return jd['expiryDates']
            if 'records' in jd and 'expiryDates' in jd['records']:
                return jd['records']['expiryDates']
    except Exception:
        pass
    return []

def fetch_option_chain_raw(symbol, expiry, mode):
    t_str = 'Indices' if mode == 'Index' else 'Equity'
    url = f'https://www.nseindia.com/api/option-chain-v3?type={t_str}&symbol={symbol}&expiry={expiry}'
    r = nse_get(url)
    if r is None or r.status_code != 200:
        return None, None, None, f"HTTP {r.status_code if r is not None else 'no response'} from NSE."
    try:
        jd = r.json()
    except Exception:
        return None, None, None, "NSE response was not valid JSON."

    ce_vals = [d['CE'] for d in jd.get('records', {}).get('data', [])
               if 'CE' in d and d.get('expiryDate', '').lower() == expiry.lower()]
    pe_vals = [d['PE'] for d in jd.get('records', {}).get('data', [])
               if 'PE' in d and d.get('expiryDate', '').lower() == expiry.lower()]
    if not ce_vals or not pe_vals:
        return None, None, None, "Empty chain for this expiry."

    points = next((x['underlyingValue'] for x in pe_vals if x['underlyingValue'] != 0), 0.0)
    ts = jd.get('records', {}).get('timestamp', datetime.datetime.now().strftime('%d-%b-%Y %H:%M:%S'))

    cols_ce = ['openInterest', 'changeinOpenInterest', 'totalTradedVolume', 'impliedVolatility',
               'lastPrice', 'change', 'buyQuantity1', 'buyPrice1', 'sellPrice1', 'sellQuantity1', 'strikePrice']
    cols_pe = ['strikePrice', 'buyQuantity1', 'buyPrice1', 'sellPrice1', 'sellQuantity1',
               'change', 'lastPrice', 'impliedVolatility', 'totalTradedVolume', 'changeinOpenInterest', 'openInterest']

    ce_df = pd.DataFrame(ce_vals)[cols_ce]
    pe_df = pd.DataFrame(pe_vals)[cols_pe]
    merged = pd.merge(ce_df, pe_df, on='strikePrice')
    merged.columns = ['CE OI', 'CE Chg OI', 'CE Volume', 'CE IV', 'CE LTP', 'CE Net Chg',
                       'CE Bid Qty', 'CE Bid Price', 'CE Ask Price', 'CE Ask Qty', 'Strike Price',
                       'PE Bid Qty', 'PE Bid Price', 'PE Ask Price', 'PE Ask Qty',
                       'PE Net Chg', 'PE LTP', 'PE IV', 'PE Volume', 'PE Chg OI', 'PE OI']
    return merged, ts, points, None


def analyse_oc(df, sp, rf, points):
    """Full option-chain analytics engine."""
    try:
        matched = df[df['Strike Price'] == sp].index.tolist()
        if not matched:
            return None
        idx = int(matched[0])
        c_oi = [int(df.iloc[i, 0]) for i in range(len(df))]
        p_oi = [int(df.iloc[i, 20]) for i in range(len(df))]
        ci = c_oi.index(max(c_oi))
        pi = p_oi.index(max(p_oi))
        mc_sp = float(df.iloc[ci]['Strike Price'])
        mp_sp = float(df.iloc[pi]['Strike Price'])
        mc = round(max(c_oi) / rf, 1)
        mp = round(max(p_oi) / rf, 1)

        if mc_sp == mp_sp:
            mc2, mc_sp2, mp2, mp_sp2 = mc, mc_sp, mp, mp_sp
        elif abs(ci - pi) == 1:
            mc2 = round(df[df['Strike Price'] == mp_sp].iloc[0, 0] / rf, 1)
            mc_sp2 = mp_sp
            mp2 = round(df[df['Strike Price'] == mc_sp].iloc[0, 20] / rf, 1)
            mp_sp2 = mc_sp
        else:
            lo, hi = min(pi, ci), max(pi, ci)
            ic = [int(df.iloc[i, 0]) for i in range(lo, hi)] or [0]
            ip = [int(df.iloc[i, 20]) for i in range(lo + 1, hi + 1)] or [0]
            mc2 = round(max(ic) / rf, 1)
            mc_sp2 = float(df.iloc[lo + ic.index(max(ic))]['Strike Price'])
            mp2 = round(max(ip) / rf, 1)
            mp_sp2 = float(df.iloc[lo + 1 + ip.index(max(ip))]['Strike Price'])

        tot_c = sum(c_oi)
        tot_p = sum(p_oi)
        pcr = round(tot_p / tot_c, 2) if tot_c else 0.0

        def sv(s_series, i):
            v = s_series.get(i, 'x')
            return 0 if isinstance(v, str) else int(v)

        cc = df.iloc[:, 1]
        pc = df.iloc[:, 19]
        c1 = int(df.iloc[idx, 1])
        c2, c3 = sv(cc, idx + 1), sv(cc, idx + 2)
        p1 = int(df.iloc[idx, 19])
        p2, p3 = sv(pc, idx + 1), sv(pc, idx + 2)
        p4, p5 = sv(pc, idx + 4), sv(cc, idx + 4)
        p6, p7 = sv(cc, idx - 2), sv(pc, idx - 2)

        cs = round((c1 + c2 + c3) / rf, 1)
        cb = round(c3 / rf, 1)
        ps = round((p1 + p2 + p3) / rf, 1)
        pb = round(p1 / rf, 1)
        diff = round(cs - ps, 1)
        citm = 0.0 if p5 == 0 else round(p4 / p5, 1)
        pitm = 0.0 if p7 == 0 else round(p6 / p7, 1)

        def itm_lbl(ca, pa):
            lbl = 'No'
            if pa > ca:
                if pa >= 0:
                    if ca <= 0 or pa / (ca or 1) > 1.5:
                        lbl = 'Yes'
                elif pa / (ca or 1) < 0.5:
                    lbl = 'Yes'
            if ca <= 0:
                lbl = 'Yes'
            return lbl

        ce_iv = float(df.iloc[idx]['CE IV'])
        pe_iv = float(df.iloc[idx]['PE IV'])
        tot_cv = int(df['CE Volume'].sum())
        tot_pv = int(df['PE Volume'].sum())
        vr = round(tot_pv / tot_cv, 2) if tot_cv else 0.0
        ce_wiv = round((df['CE IV'] * df['CE OI']).sum() / max(df['CE OI'].sum(), 1), 2)
        pe_wiv = round((df['PE IV'] * df['PE OI']).sum() / max(df['PE OI'].sum(), 1), 2)

        strikes = df['Strike Price'].tolist()
        def pain(k):
            return (sum(c_oi[i] * (k - s) for i, s in enumerate(strikes) if k > s)
                    + sum(p_oi[i] * (s - k) for i, s in enumerate(strikes) if k < s))
        max_pain = min(strikes, key=pain)

        return dict(
            cs=cs, ps=ps, diff=diff, cb=cb, pb=pb, citm=citm, pitm=pitm,
            mc=mc, mc_sp=mc_sp, mc2=mc2, mc_sp2=mc_sp2,
            mp=mp, mp_sp=mp_sp, mp2=mp2, mp_sp2=mp_sp2,
            pcr=pcr, sentiment='Bearish' if cs >= ps else 'Bullish',
            call_itm_lbl=itm_lbl(p5, p4), put_itm_lbl=itm_lbl(p7, p6),
            ce_exits='Yes' if cb <= 0 or cs <= 0 else 'No',
            pe_exits='Yes' if pb <= 0 or ps <= 0 else 'No',
            ce_iv=ce_iv, pe_iv=pe_iv, iv_skew=round(pe_iv - ce_iv, 2),
            tot_c=tot_c, tot_p=tot_p, tot_cv=tot_cv, tot_pv=tot_pv,
            vr=vr, ce_wiv=ce_wiv, pe_wiv=pe_wiv, max_pain=max_pain,
        )
    except Exception:
        return None


def calc_suggestion(m, points):
    """7-factor scoring engine."""
    score = 0
    reasons = []
    pcr = m['pcr']
    if pcr >= 1.3:
        score += 3; reasons.append(('BULLISH', f'PCR {pcr} ≥ 1.3 — heavy put writing signals floor support'))
    elif pcr >= 1.1:
        score += 2; reasons.append(('BULLISH', f'PCR {pcr} ∈ [1.1,1.3) — put OI dominance'))
    elif pcr >= 0.9:
        reasons.append(('NEUTRAL', f'PCR {pcr} ∈ [0.9,1.1) — balanced OI'))
    elif pcr >= 0.7:
        score -= 2; reasons.append(('BEARISH', f'PCR {pcr} ∈ [0.7,0.9) — call OI dominance'))
    else:
        score -= 3; reasons.append(('BEARISH', f'PCR {pcr} < 0.7 — aggressive call writing'))

    if m['sentiment'] == 'Bullish':
        score += 2; reasons.append(('BULLISH', f'OI Diff {m["diff"]:+.1f} — PE writers dominant'))
    else:
        score -= 2; reasons.append(('BEARISH', f'OI Diff {m["diff"]:+.1f} — CE writers dominant'))

    pain_diff = m['max_pain'] - points
    if abs(pain_diff) < 50:
        reasons.append(('NEUTRAL', f'Price ≈ Max Pain ({int(m["max_pain"])})'))
    elif pain_diff > 200:
        score += 2; reasons.append(('BULLISH', f'Max Pain {int(m["max_pain"])} is {pain_diff:+.0f} pts above CMP'))
    elif pain_diff > 0:
        score += 1; reasons.append(('BULLISH', f'Max Pain {int(m["max_pain"])} mildly above CMP'))
    elif pain_diff < -200:
        score -= 2; reasons.append(('BEARISH', f'Max Pain {int(m["max_pain"])} is {pain_diff:+.0f} pts below CMP'))
    else:
        score -= 1; reasons.append(('BEARISH', f'Max Pain mildly below CMP'))

    sk = m['iv_skew']
    if sk > 4: score -= 3; reasons.append(('BEARISH', f'IV Skew +{sk}% — extreme put premium'))
    elif sk > 2: score -= 2; reasons.append(('BEARISH', f'IV Skew +{sk}% — elevated put premium'))
    elif sk > 0.5: score -= 1; reasons.append(('MILD BEAR', f'IV Skew +{sk}%'))
    elif sk < -4: score += 3; reasons.append(('BULLISH', f'IV Skew {sk}% — extreme call premium'))
    elif sk < -2: score += 2; reasons.append(('BULLISH', f'IV Skew {sk}% — elevated call premium'))
    elif sk < -0.5: score += 1; reasons.append(('MILD BULL', f'IV Skew {sk}%'))
    else: reasons.append(('NEUTRAL', f'IV Skew {sk}% — balanced'))

    vr = m['vr']
    if vr > 1.5: score += 2; reasons.append(('BULLISH', f'Vol Ratio {vr} — PE volume dominant'))
    elif vr > 1.2: score += 1; reasons.append(('BULLISH', f'Vol Ratio {vr}'))
    elif vr < 0.6: score -= 2; reasons.append(('BEARISH', f'Vol Ratio {vr} — CE volume dominant'))
    elif vr < 0.8: score -= 1; reasons.append(('BEARISH', f'Vol Ratio {vr}'))
    else: reasons.append(('NEUTRAL', f'Vol Ratio {vr} — balanced'))

    if m['ce_exits'] == 'Yes' and m['pe_exits'] == 'Yes':
        reasons.append(('CAUTION', 'Both CE & PE unwinding — avoid new entries'))
    elif m['ce_exits'] == 'Yes':
        score += 1; reasons.append(('MILD BULL', 'CE OI unwinding — call shorts covering'))
    elif m['pe_exits'] == 'Yes':
        score -= 1; reasons.append(('MILD BEAR', 'PE OI unwinding — put shorts covering'))

    ratio = m['ps'] / max(m['cs'], 0.01)
    if ratio > 1.5: score += 1; reasons.append(('BULLISH', f'ATM PE OI >> CE OI — support'))
    elif ratio < 0.67: score -= 1; reasons.append(('BEARISH', f'ATM CE OI >> PE OI — resistance'))

    if score >= 7: action, confidence, conf_pct = 'STRONG BUY CE 🚀', 'Very High', 90
    elif score >= 4: action, confidence, conf_pct = 'BUY CE 📈', 'High', 75
    elif score >= 2: action, confidence, conf_pct = 'MILD CE BIAS ↗', 'Moderate', 60
    elif score >= 1: action, confidence, conf_pct = 'SLIGHT CE LEAN ↗', 'Low', 52
    elif score <= -7: action, confidence, conf_pct = 'STRONG BUY PE 🔻', 'Very High', 90
    elif score <= -4: action, confidence, conf_pct = 'BUY PE 📉', 'High', 75
    elif score <= -2: action, confidence, conf_pct = 'MILD PE BIAS ↘', 'Moderate', 60
    elif score <= -1: action, confidence, conf_pct = 'SLIGHT PE LEAN ↘', 'Low', 52
    else: action, confidence, conf_pct = 'NEUTRAL / WAIT ⏸', 'Low', 50

    return dict(action=action, score=score, confidence=confidence, conf_pct=conf_pct, reasons=reasons)


# ==============================================================================
# IPO DATA (from Knowledge Base)
# ==============================================================================
IPO_BELOW_PRICE = [
    {"Name": "Shlokka Dyes", "Listing Date": "17 Oct 2025", "IPO MCap": 195, "IPO Price": 91, "Current Price": 69.66, "% Change": -23},
    {"Name": "Sihora Indust.", "Listing Date": "17 Oct 2025", "IPO MCap": 35, "IPO Price": 66, "Current Price": 54.18, "% Change": -18},
    {"Name": "Mittal Sections", "Listing Date": "14 Oct 2025", "IPO MCap": 165, "IPO Price": 143, "Current Price": 76.00, "% Change": -47},
    {"Name": "Tata Capital", "Listing Date": "13 Oct 2025", "IPO MCap": 138383, "IPO Price": 326, "Current Price": 324.15, "% Change": -1},
    {"Name": "NSB BPO", "Listing Date": "10 Oct 2025", "IPO MCap": 280, "IPO Price": 140, "Current Price": 119.00, "% Change": -15},
    {"Name": "Wework India", "Listing Date": "10 Oct 2025", "IPO MCap": 8685, "IPO Price": 648, "Current Price": 634.80, "% Change": -2},
    {"Name": "Greenleaf Envi.", "Listing Date": "09 Oct 2025", "IPO MCap": 81, "IPO Price": 136, "Current Price": 133.10, "% Change": -2},
    {"Name": "Om Freight Forwa", "Listing Date": "08 Oct 2025", "IPO MCap": 455, "IPO Price": 135, "Current Price": 93.36, "% Change": -31},
    {"Name": "Chiraharit", "Listing Date": "08 Oct 2025", "IPO MCap": 115, "IPO Price": 21, "Current Price": 14.55, "% Change": -31},
    {"Name": "Glottis", "Listing Date": "07 Oct 2025", "IPO MCap": 1192, "IPO Price": 129, "Current Price": 74.53, "% Change": -42},
    {"Name": "Om Metallogic", "Listing Date": "07 Oct 2025", "IPO MCap": 66, "IPO Price": 83, "Current Price": 44.32, "% Change": -47},
    {"Name": "Dhillon Freight", "Listing Date": "07 Oct 2025", "IPO MCap": 28, "IPO Price": 72, "Current Price": 40.20, "% Change": -44},
    {"Name": "Rukmani Devi Gar", "Listing Date": "06 Oct 2025", "IPO MCap": 88, "IPO Price": 99, "Current Price": 69.50, "% Change": -30},
    {"Name": "Jinkushal Indus.", "Listing Date": "03 Oct 2025", "IPO MCap": 464, "IPO Price": 122, "Current Price": 120.71, "% Change": -1},
    {"Name": "TruAlt Bioenergy", "Listing Date": "03 Oct 2025", "IPO MCap": 4253, "IPO Price": 496, "Current Price": 456.80, "% Change": -8},
    {"Name": "Solvex Edibles", "Listing Date": "01 Oct 2025", "IPO MCap": 64, "IPO Price": 72, "Current Price": 28.90, "% Change": -60},
    {"Name": "BMW Ventures", "Listing Date": "01 Oct 2025", "IPO MCap": 858, "IPO Price": 99, "Current Price": 60.75, "% Change": -39},
    {"Name": "Gurunanak Agri.", "Listing Date": "01 Oct 2025", "IPO MCap": 90, "IPO Price": 75, "Current Price": 34.90, "% Change": -53},
    {"Name": "Solarworld Ene.", "Listing Date": "30 Sep 2025", "IPO MCap": 3042, "IPO Price": 351, "Current Price": 310.40, "% Change": -12},
    {"Name": "Jaro Institute", "Listing Date": "30 Sep 2025", "IPO MCap": 1972, "IPO Price": 890, "Current Price": 666.30, "% Change": -25},
]

IPO_RECENT = [
    {"Name": "Midwest", "Listing Date": "24 Oct 2025", "IPO MCap": 3851, "IPO Price": 1065, "Current Price": 1141.10, "% Change": 7},
    {"Name": "Canara HSBC", "Listing Date": "17 Oct 2025", "IPO MCap": 10070, "IPO Price": 106, "Current Price": 118.14, "% Change": 11},
    {"Name": "SK Minerals", "Listing Date": "17 Oct 2025", "IPO MCap": 155, "IPO Price": 127, "Current Price": 195.00, "% Change": 54},
    {"Name": "Rubicon Research", "Listing Date": "16 Oct 2025", "IPO MCap": 7990, "IPO Price": 485, "Current Price": 609.80, "% Change": 26},
    {"Name": "Canara Robeco", "Listing Date": "16 Oct 2025", "IPO MCap": 5304, "IPO Price": 266, "Current Price": 323.75, "% Change": 22},
    {"Name": "LG Electronics", "Listing Date": "14 Oct 2025", "IPO MCap": 77380, "IPO Price": 1140, "Current Price": 1657.70, "% Change": 45},
    {"Name": "Tata Capital", "Listing Date": "13 Oct 2025", "IPO MCap": 138383, "IPO Price": 326, "Current Price": 326.95, "% Change": 0},
    {"Name": "DSM Fresh", "Listing Date": "09 Oct 2025", "IPO MCap": 223, "IPO Price": 100, "Current Price": 186.57, "% Change": 87},
    {"Name": "Infinity Infoway", "Listing Date": "08 Oct 2025", "IPO MCap": 85, "IPO Price": 155, "Current Price": 365.25, "% Change": 136},
    {"Name": "Zelio E-Mobility", "Listing Date": "08 Oct 2025", "IPO MCap": 288, "IPO Price": 136, "Current Price": 327.25, "% Change": 141},
    {"Name": "Advance Agrolife", "Listing Date": "08 Oct 2025", "IPO MCap": 643, "IPO Price": 100, "Current Price": 136.26, "% Change": 36},
    {"Name": "B.A.G. Converge.", "Listing Date": "08 Oct 2025", "IPO MCap": 185, "IPO Price": 87, "Current Price": 129.90, "% Change": 49},
    {"Name": "Sunsky Logistics", "Listing Date": "08 Oct 2025", "IPO MCap": 57, "IPO Price": 46, "Current Price": 79.55, "% Change": 73},
]

IPO_UPCOMING = [
    {"Name": "Jayesh Logistics", "Subscription": "3rd Nov", "M.Cap Cr": 106, "Subscription %": "33.6x"},
    {"Name": "Shreeji Global", "Subscription": "12th Nov", "M.Cap Cr": 284, "Subscription %": "52.0x"},
]


# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS"]
if 'alerts' not in st.session_state:
    st.session_state.alerts = []


# ==============================================================================
# SIDEBAR NAVIGATION
# ==============================================================================
st.sidebar.markdown("## 📈 NSE Terminal <span style='color:#58a6ff'>v3.0</span>", unsafe_allow_html=True)
st.sidebar.markdown("---")

app_mode = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Market Command Center",
        "🔄 Sectoral Rotation",
        "📅 Seasonality Lab",
        "📐 Multi-MA Screener",
        "💼 Portfolio Optimizer",
        "🔗 Correlation & Clustering",
        "🎲 Probability & Monte Carlo",
        "⚡ Option Chain & Strategy",
        "🚀 IPO Intelligence",
        "📊 Technical Workbench",
        "🛡️ Risk Management Suite",
        "⭐ Watchlist & Alerts",
    ],
    label_visibility="collapsed"
)

st.sidebar.markdown("---")
st.sidebar.markdown(f"""
<div style="font-size:0.75rem;color:#8b949e;padding:8px 0">
    <b>Session:</b> {datetime.datetime.now().strftime('%d %b %Y, %H:%M')}<br>
    <b>Universe:</b> {len(TICKER_LIST)} stocks<br>
    <b>Sectors:</b> {len(set(SECTOR_MAP.values()))} tracked<br>
    <b>Data Cache:</b> 1hr TTL
</div>
""", unsafe_allow_html=True)

# Watchlist quick-access in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### ⭐ Quick Watchlist")
for t in st.session_state.watchlist[:5]:
    st.sidebar.markdown(f"• `{t.replace('.NS','')}`")


# ==============================================================================
# 1. MARKET COMMAND CENTER
# ==============================================================================
if app_mode == "🏠 Market Command Center":
    st.markdown("""
    <div class="terminal-header">
        <h1>🏠 Market Command Center</h1>
        <div class="subtitle">Real-time movers, breadth indicators, and market pulse across 200+ NSE equities</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("⚡ Fetching market data..."):
        data = fetch_data(TICKER_LIST, "2mo")

    if not data.empty and 'Close' in data.columns:
        close_prices = data['Close'].ffill().bfill()
        
        # Calculate returns
        results = []
        for ticker in TICKER_LIST:
            if ticker in close_prices.columns:
                s = close_prices[ticker].dropna()
                if len(s) >= 22:
                    current = s.iloc[-1]
                    results.append({
                        "Ticker": ticker.replace(".NS", ""),
                        "Full Ticker": ticker,
                        "Sector": SECTOR_MAP.get(ticker, "Others"),
                        "LTP": round(current, 2),
                        "1D %": round(((current - s.iloc[-2]) / s.iloc[-2]) * 100, 2),
                        "1W %": round(((current - s.iloc[-6]) / s.iloc[-6]) * 100, 2),
                        "1M %": round(((current - s.iloc[-22]) / s.iloc[-22]) * 100, 2),
                    })

        df = pd.DataFrame(results)
        
        # Market Breadth
        advancers = len(df[df['1D %'] > 0])
        decliners = len(df[df['1D %'] < 0])
        unchanged = len(df[df['1D %'] == 0])
        breadth_ratio = advancers / max(decliners, 1)
        
        avg_1d = df['1D %'].mean()
        median_1d = df['1D %'].median()
        
        # Top metrics row
        mc1, mc2, mc3, mc4, mc5, mc6 = st.columns(6)
        mc1.metric("Advancers", f"🟢 {advancers}", delta=f"{advancers}/{len(df)}")
        mc2.metric("Decliners", f"🔴 {decliners}", delta=f"-{decliners}", delta_color="inverse")
        mc3.metric("Breadth Ratio", f"{breadth_ratio:.2f}", delta="Bullish" if breadth_ratio > 1 else "Bearish")
        mc4.metric("Avg 1D Return", f"{avg_1d:+.2f}%")
        mc5.metric("Median 1D", f"{median_1d:+.2f}%")
        mc6.metric("Universe Size", f"{len(df)}")
        
        st.markdown("---")
        
        tab1, tab2, tab3, tab4 = st.tabs(["🚀 Top Movers", "📊 Distribution", "🏆 Sector Leaders", "📋 Full Table"])
        
        with tab1:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.subheader("1-Day")
                top_1d = df.nlargest(10, "1D %")
                st.dataframe(top_1d[['Ticker', 'LTP', '1D %']].style.background_gradient(subset=['1D %'], cmap="Greens"), use_container_width=True)
                bot_1d = df.nsmallest(10, "1D %")
                st.dataframe(bot_1d[['Ticker', 'LTP', '1D %']].style.background_gradient(subset=['1D %'], cmap="Reds_r"), use_container_width=True)
            with c2:
                st.subheader("1-Week")
                top_1w = df.nlargest(10, "1W %")
                st.dataframe(top_1w[['Ticker', 'LTP', '1W %']].style.background_gradient(subset=['1W %'], cmap="Greens"), use_container_width=True)
                bot_1w = df.nsmallest(10, "1W %")
                st.dataframe(bot_1w[['Ticker', 'LTP', '1W %']].style.background_gradient(subset=['1W %'], cmap="Reds_r"), use_container_width=True)
            with c3:
                st.subheader("1-Month")
                top_1m = df.nlargest(10, "1M %")
                st.dataframe(top_1m[['Ticker', 'LTP', '1M %']].style.background_gradient(subset=['1M %'], cmap="Greens"), use_container_width=True)
                bot_1m = df.nsmallest(10, "1M %")
                st.dataframe(bot_1m[['Ticker', 'LTP', '1M %']].style.background_gradient(subset=['1M %'], cmap="Reds_r"), use_container_width=True)
        
        with tab2:
            fig_hist = go.Figure()
            fig_hist.add_trace(go.Histogram(x=df['1D %'], nbinsx=50, marker_color='#58a6ff', opacity=0.7, name='1D'))
            fig_hist.add_vline(x=0, line_color="#ff4d6d", line_width=2, line_dash="dash")
            fig_hist.add_vline(x=avg_1d, line_color="#00c48c", line_width=2, annotation_text=f"Avg: {avg_1d:.2f}%")
            fig_hist.update_layout(title="1-Day Return Distribution", xaxis_title="Return %", yaxis_title="Count",
                                   template="plotly_dark", height=400)
            st.plotly_chart(fig_hist, use_container_width=True)
            
            # Sector-wise breadth
            sector_breadth = df.groupby('Sector').apply(lambda x: (x['1D %'] > 0).sum() / len(x) * 100).reset_index()
            sector_breadth.columns = ['Sector', 'Bullish %']
            fig_breadth = px.bar(sector_breadth.sort_values('Bullish %'), x='Bullish %', y='Sector',
                                orientation='h', color='Bullish %', color_continuous_scale='RdYlGn',
                                title="Sector Breadth (% Stocks Positive Today)")
            fig_breadth.update_layout(template="plotly_dark", height=500)
            st.plotly_chart(fig_breadth, use_container_width=True)
        
        with tab3:
            sector_perf = df.groupby('Sector')[['1D %', '1W %', '1M %']].mean().round(2).reset_index()
            sector_perf = sector_perf.sort_values('1M %', ascending=False)
            st.dataframe(sector_perf.style.background_gradient(subset=['1M %'], cmap="RdYlGn"), use_container_width=True)
        
        with tab4:
            st.dataframe(df.sort_values('1D %', ascending=False), use_container_width=True, height=600)


# ==============================================================================
# 2. SECTORAL ROTATION
# ==============================================================================
elif app_mode == "🔄 Sectoral Rotation":
    st.markdown("""
    <div class="terminal-header">
        <h1>🔄 Sectoral Rotation Engine</h1>
        <div class="subtitle">Track capital flows across sectors with multi-timeframe analysis</div>
    </div>
    """, unsafe_allow_html=True)

    with st.spinner("⚡ Fetching sectoral data..."):
        raw = fetch_data(TICKER_LIST, "6mo")

    if not raw.empty and 'Close' in raw.columns:
        close = raw['Close'].ffill().bfill()
        
        def safe_ret(series, n):
            c = series.dropna()
            if len(c) < n + 1: return np.nan
            return round(((c.iloc[-1] / c.iloc[-1 - n]) - 1) * 100, 2)

        records = []
        for t in close.columns:
            s = close[t]
            if len(s.dropna()) >= 22:
                records.append({
                    "Ticker": t.replace(".NS", ""),
                    "Full": t,
                    "Sector": SECTOR_MAP.get(t, "Others"),
                    "1D %": safe_ret(s, 1), "1W %": safe_ret(s, 5),
                    "1M %": safe_ret(s, 21), "3M %": safe_ret(s, 63),
                })
        df = pd.DataFrame(records).dropna()

        tab1, tab2, tab3, tab4 = st.tabs(["🔥 Heatmap", "📊 Rotation Chart", "🌳 Treemap", "📈 Momentum"])
        
        with tab1:
            sector_agg = df.groupby("Sector")[["1D %", "1W %", "1M %", "3M %"]].mean().round(2).reset_index()
            sector_agg = sector_agg.sort_values("1M %", ascending=False)
            heat_data = sector_agg.set_index("Sector")[["1D %", "1W %", "1M %", "3M %"]]
            fig = px.imshow(heat_data, text_auto=True, color_continuous_scale="RdYlGn",
                           color_continuous_midpoint=0, aspect="auto", title="Sector Performance Matrix")
            fig.update_layout(template="plotly_dark", height=600)
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            fig2 = make_subplots(rows=2, cols=2, subplot_titles=("1D Returns", "1W Returns", "1M Returns", "3M Returns"))
            for i, col in enumerate(["1D %", "1W %", "1M %", "3M %"]):
                data_sorted = sector_agg.sort_values(col)
                colors = ['#00c48c' if x >= 0 else '#ff4d6d' for x in data_sorted[col]]
                fig2.add_trace(go.Bar(x=data_sorted[col], y=data_sorted["Sector"], orientation='h',
                                      marker_color=colors, name=col, showlegend=False),
                              row=i//2+1, col=i%2+1)
            fig2.update_layout(height=800, template="plotly_dark", title_text="Multi-Timeframe Sector Returns")
            st.plotly_chart(fig2, use_container_width=True)
        
        with tab3:
            df["Size"] = df["1M %"].abs().clip(lower=0.1)
            fig3 = px.treemap(df, path=['Sector', 'Ticker'], values='Size', color='1M %',
                             color_continuous_scale='RdYlGn', color_continuous_midpoint=0,
                             title="Market Treemap (Size=|1M Return|, Color=Return)")
            fig3.update_layout(template="plotly_dark", height=600)
            st.plotly_chart(fig3, use_container_width=True)
        
        with tab4:
            # Sector momentum: 1M vs 3M to identify accelerating/decelerating sectors
            sector_agg['Momentum'] = sector_agg['1M %'] - sector_agg['3M %'] / 3
            sector_agg['Status'] = sector_agg['Momentum'].apply(
                lambda x: '🟢 Accelerating' if x > 1 else ('🔴 Decelerating' if x < -1 else '🟡 Stable'))
            st.dataframe(sector_agg.sort_values('Momentum', ascending=False), use_container_width=True)


# ==============================================================================
# 3. SEASONALITY LAB
# ==============================================================================
elif app_mode == "📅 Seasonality Lab":
    st.markdown("""
    <div class="terminal-header">
        <h1>📅 Seasonality Laboratory</h1>
        <div class="subtitle">Statistical analysis of monthly return patterns with significance testing</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        months = list(calendar.month_name)[1:]
        target_month_name = st.selectbox("Target Month", options=months, index=(datetime.datetime.now().month % 12))
        target_month = list(calendar.month_name).index(target_month_name)
        years_history = st.slider("Years of History", 5, 15, 10)
        min_years = st.slider("Min Years Traded", 3, 10, 5)
        run_seasonality = st.button("🔬 Run Analysis", type="primary")

    if run_seasonality:
        with st.spinner(f"📊 Fetching {years_history} years of data..."):
            raw = fetch_data(TICKER_LIST, f"{years_history}y", interval="1mo")
            daily_raw = fetch_data(TICKER_LIST, "5d", interval="1d")

        if not raw.empty and 'Close' in raw.columns:
            close = raw["Close"]
            returns = close.pct_change() * 100
            daily_close = daily_raw["Close"]
            ltp_map = {t: round(daily_close[t].dropna().iloc[-1], 2) for t in daily_close.columns if len(daily_close[t].dropna()) > 0}

            records = []
            for ticker in close.columns:
                monthly = returns[ticker][returns.index.month == target_month].dropna()
                if len(monthly) >= min_years:
                    avg = monthly.mean()
                    std = monthly.std()
                    win_rate = (monthly > 0).mean() * 100
                    sharpe = avg / std if std > 0 else np.nan
                    # T-test: is the mean significantly different from 0?
                    if len(monthly) > 2:
                        t_stat, p_value = stats.ttest_1samp(monthly, 0)
                    else:
                        t_stat, p_value = 0, 1.0
                    
                    records.append({
                        "Ticker": ticker.replace(".NS", ""),
                        "LTP": ltp_map.get(ticker, np.nan),
                        "Win Rate (%)": round(win_rate, 1),
                        "Avg Return (%)": round(avg, 2),
                        "Std Dev (%)": round(std, 2),
                        "Sharpe": round(sharpe, 3) if not np.isnan(sharpe) else np.nan,
                        "t-stat": round(t_stat, 2),
                        "p-value": round(p_value, 4),
                        "Significant": "✅" if p_value < 0.05 else "❌",
                        "Years": len(monthly)
                    })

            df = pd.DataFrame(records).dropna(subset=["Sharpe"]).sort_values("Sharpe", ascending=False).reset_index(drop=True)
            df.index += 1

            st.success(f"✅ Analyzed {len(df)} stocks with ≥{min_years} years of {target_month_name} data")
            
            # Summary stats
            sig_count = len(df[df['p-value'] < 0.05])
            st.info(f"📈 **{sig_count}/{len(df)}** stocks show statistically significant {target_month_name} seasonality (p < 0.05)")
            
            st.dataframe(df.head(30).style.background_gradient(subset=["Sharpe"], cmap="Blues"), use_container_width=True)

            top = df.head(15)
            fig = make_subplots(rows=1, cols=3, subplot_titles=("Avg Return", "Win Rate", "Statistical Significance"))
            colors = ["#00C853" if v > 0 else "#D50000" for v in top["Avg Return (%)"]]
            fig.add_trace(go.Bar(x=top["Ticker"], y=top["Avg Return (%)"], marker_color=colors, showlegend=False), row=1, col=1)
            fig.add_trace(go.Bar(x=top["Ticker"], y=top["Win Rate (%)"], marker_color='#58a6ff', showlegend=False), row=1, col=2)
            fig.add_trace(go.Bar(x=top["Ticker"], y=-np.log10(top["p-value"].clip(lower=1e-10)),
                                marker_color='#bc8cff', showlegend=False, name="-log10(p)"), row=1, col=3)
            fig.add_hline(y=-np.log10(0.05), line_dash="dash", line_color="#e3b341", row=1, col=3,
                         annotation_text="p=0.05 threshold")
            fig.update_layout(height=450, template="plotly_dark", showlegend=False)
            st.plotly_chart(fig, use_container_width=True)


# ==============================================================================
# 4. MULTI-MA SCREENER
# ==============================================================================
elif app_mode == "📐 Multi-MA Screener":
    st.markdown("""
    <div class="terminal-header">
        <h1>📐 Multi-MA Crossover & Pattern Screener</h1>
        <div class="subtitle">Golden/Death Cross detection with RSI, MACD confirmation filters</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("Scans for SMA/EMA crossovers with multi-indicator confirmation.")
    
    col1, col2, col3 = st.columns(3)
    fast_ma = col1.selectbox("Fast MA Period", [9, 13, 20, 21, 50], index=4)
    slow_ma = col2.selectbox("Slow MA Period", [50, 100, 150, 200], index=3)
    ma_type = col3.selectbox("MA Type", ["SMA", "EMA"])
    use_rsi_filter = st.checkbox("Require RSI confirmation (30-70 for buy, avoid overbought/oversold)", value=True)
    
    if st.button("🔍 Run Screener", type="primary"):
        with st.spinner("⚡ Fetching 2 years of data..."):
            raw = fetch_data(TICKER_LIST, "2y", "1d")

        if not raw.empty and 'Close' in raw.columns:
            close_df = raw['Close']
            results = []

            progress = st.progress(0)
            for i, ticker in enumerate(close_df.columns):
                progress.progress((i + 1) / len(close_df.columns))
                s = close_df[ticker].dropna()
                if len(s) < slow_ma + 10:
                    continue

                if ma_type == "SMA":
                    fast_series = s.rolling(window=fast_ma).mean()
                    slow_series = s.rolling(window=slow_ma).mean()
                else:
                    fast_series = s.ewm(span=fast_ma, adjust=False).mean()
                    slow_series = s.ewm(span=slow_ma, adjust=False).mean()

                valid = pd.DataFrame({'Close': s, 'Fast': fast_series, 'Slow': slow_series}).dropna()
                if valid.empty:
                    continue

                last_close = valid['Close'].iloc[-1]
                last_fast = valid['Fast'].iloc[-1]
                last_slow = valid['Slow'].iloc[-1]
                diff_pct = ((last_fast - last_slow) / last_slow) * 100

                bullish = valid['Fast'] > valid['Slow']
                cross_points = bullish.ne(bullish.shift())
                cross_points.iloc[0] = False
                cross_dates = valid.index[cross_points]

                days_since_cross = None
                if len(cross_dates) > 0:
                    days_since_cross = len(valid) - 1 - valid.index.get_loc(cross_dates[-1])

                # RSI
                rsi_val = calc_rsi(s, 14).iloc[-1] if len(s) > 14 else 50
                
                # MACD
                macd_line, signal_line, hist = calc_macd(s)
                macd_bullish = macd_line.iloc[-1] > signal_line.iloc[-1] if len(macd_line.dropna()) > 0 else False

                status = "No Signal"
                signal = "Neutral"
                strength = 0

                if days_since_cross is not None:
                    if days_since_cross <= 3:
                        status = "⚡ FRESH CROSS"
                        signal = "Bullish" if last_fast > last_slow else "Bearish"
                        strength = 3
                    elif days_since_cross <= 20:
                        status = "Post Cross"
                        signal = "Bullish" if last_fast > last_slow else "Bearish"
                        strength = 2

                if status == "No Signal" and abs(diff_pct) <= 2.0:
                    if last_fast < last_slow:
                        status = "🔜 Approaching Golden"
                        signal = "Bullish"
                        strength = 1
                    else:
                        status = "🔜 Approaching Death"
                        signal = "Bearish"
                        strength = 1

                # Confirmation filters
                confirmed = True
                if use_rsi_filter and signal == "Bullish" and rsi_val > 70:
                    confirmed = False
                if use_rsi_filter and signal == "Bearish" and rsi_val < 30:
                    confirmed = False
                if signal == "Bullish" and not macd_bullish:
                    strength -= 1
                if signal == "Bearish" and macd_bullish:
                    strength -= 1

                if status != "No Signal" and confirmed and strength > 0:
                    results.append({
                        "Ticker": ticker.replace(".NS", ""),
                        "Close": round(last_close, 2),
                        f"{ma_type}{fast_ma}": round(last_fast, 2),
                        f"{ma_type}{slow_ma}": round(last_slow, 2),
                        "Diff %": round(diff_pct, 2),
                        "RSI": round(rsi_val, 1),
                        "MACD": "🟢" if macd_bullish else "🔴",
                        "Status": status,
                        "Signal": signal,
                        "Strength": "⭐" * strength,
                        "Days Since": days_since_cross if days_since_cross else "—"
                    })

            progress.empty()
            
            if results:
                df_results = pd.DataFrame(results).sort_values(['Signal', 'Diff %'])
                st.success(f"🎯 Found **{len(df_results)}** actionable signals!")
                
                bull = df_results[df_results['Signal'] == 'Bullish']
                bear = df_results[df_results['Signal'] == 'Bearish']
                
                c1, c2 = st.columns(2)
                with c1:
                    st.markdown("### 🟢 Bullish Signals")
                    st.dataframe(bull.style.map(lambda v: 'color: #00c48c; font-weight: bold' if v == 'Bullish' else '', subset=['Signal']), use_container_width=True)
                with c2:
                    st.markdown("### 🔴 Bearish Signals")
                    st.dataframe(bear.style.map(lambda v: 'color: #ff4d6d; font-weight: bold' if v == 'Bearish' else '', subset=['Signal']), use_container_width=True)
            else:
                st.info("No actionable signals found with current filters.")


# ==============================================================================
# 5. PORTFOLIO OPTIMIZER
# ==============================================================================
elif app_mode == "💼 Portfolio Optimizer":
    st.markdown("""
    <div class="terminal-header">
        <h1>💼 Portfolio Optimizer</h1>
        <div class="subtitle">Efficient Frontier, Risk Budgeting, and Roy's Safety-First optimization</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 3])
    with col1:
        inv_amt = st.number_input("Investment (₹)", min_value=10000, value=500000, step=50000)
        port_size = st.slider("Stocks per Portfolio", 3, 15, 8)
        threshold_ret = st.slider("Min Return (%)", 1.0, 20.0, 8.0) / 100
        opt_method = st.selectbox("Optimization", ["Max Sharpe", "Min Variance", "Max Sortino", "Risk Parity"])
        run_opt = st.button("🚀 Optimize", type="primary")

    if run_opt:
        with st.spinner("⚡ Fetching 2Y data & running optimization..."):
            raw = fetch_data(TICKER_LIST + ["^NSEI"], "2y")

        if not raw.empty and 'Close' in raw.columns:
            cleaned = raw['Close'].dropna(thresh=int(len(raw)*0.8), axis=1).ffill().bfill()
            benchmark = cleaned.pop("^NSEI") if "^NSEI" in cleaned.columns else None
            daily_ret = cleaned.pct_change().dropna()

            exp_ret = daily_ret.mean() * TRADING_DAYS
            ann_vol = daily_ret.std() * np.sqrt(TRADING_DAYS)
            sharpe = (exp_ret - RISK_FREE_RATE) / ann_vol
            
            def _mdd(series):
                peak = series.cummax()
                return ((series - peak) / peak).min()
            mdd = cleaned.apply(_mdd)
            
            p_1y = cleaned.iloc[-TRADING_DAYS] if len(cleaned) >= TRADING_DAYS else cleaned.iloc[0]
            actual_ret = (cleaned.iloc[-1] - p_1y) / p_1y

            score = (0.25 * exp_ret.rank(pct=True) + 0.2 * actual_ret.rank(pct=True) +
                     0.3 * sharpe.rank(pct=True) + 0.15 * (-mdd).rank(pct=True) +
                     0.1 * (daily_ret.std() * np.sqrt(TRADING_DAYS)).rank(pct=True, ascending=False))

            hard_pass = (actual_ret > 0) & (exp_ret >= threshold_ret)
            elite = score[hard_pass].nlargest(25).index.tolist()

            if len(elite) < port_size:
                st.error(f"Only {len(elite)} stocks passed. Lower the threshold.")
            else:
                cov_mat = (daily_ret[elite].cov() * TRADING_DAYS).values
                exp_arr = exp_ret[elite].values
                n = len(elite)

                # Find best combination
                combos = list(combinations(range(n), port_size))
                best_combos = []
                for combo in combos:
                    p_exp = exp_arr[list(combo)].mean()
                    if p_exp >= threshold_ret:
                        sub_cov = cov_mat[np.ix_(combo, combo)]
                        p_var = np.ones(port_size).T @ sub_cov @ np.ones(port_size) / (port_size**2)
                        p_std = np.sqrt(p_var)
                        p_sharpe = (p_exp - RISK_FREE_RATE) / p_std
                        best_combos.append((combo, p_sharpe))

                best_combos.sort(key=lambda x: x[1], reverse=True)
                top_combo_idx = best_combos[0][0]
                top_tickers = [elite[i] for i in top_combo_idx]

                port_mu = exp_ret[top_tickers].values
                port_cov = (daily_ret[top_tickers].cov() * TRADING_DAYS).values

                def objective(weights):
                    p_ret = np.sum(port_mu * weights)
                    p_vol = np.sqrt(np.dot(weights.T, np.dot(port_cov, weights)))
                    if opt_method == "Max Sharpe":
                        return -(p_ret - RISK_FREE_RATE) / p_vol
                    elif opt_method == "Min Variance":
                        return p_vol
                    elif opt_method == "Max Sortino":
                        downside = np.sqrt(np.dot(weights.T, np.dot(port_cov * (port_cov < 0), weights)))
                        return -(p_ret - RISK_FREE_RATE) / max(downside, 1e-8)
                    else:  # Risk Parity
                        contrib = weights * (port_cov @ weights)
                        target = np.sum(contrib) / port_size
                        return np.sum((contrib - target) ** 2)

                cons = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
                bounds = tuple((0.03, 0.30) for _ in range(port_size))
                init = np.array([1/port_size] * port_size)
                opt_result = minimize(objective, init, method='SLSQP', bounds=bounds, constraints=cons)
                opt_weights = opt_result.x

                opt_ret = np.sum(port_mu * opt_weights)
                opt_vol = np.sqrt(np.dot(opt_weights.T, np.dot(port_cov, opt_weights)))
                opt_sharpe = (opt_ret - RISK_FREE_RATE) / opt_vol

                st.success(f"✅ Optimization Complete | Sharpe: **{opt_sharpe:.3f}** | Return: **{opt_ret*100:.1f}%** | Vol: **{opt_vol*100:.1f}%**")

                c1, c2, c3 = st.columns(3)
                with c1:
                    st.markdown("### Allocations")
                    alloc_df = pd.DataFrame({
                        "Stock": [t.replace('.NS', '') for t in top_tickers],
                        "Weight %": (opt_weights * 100).round(1),
                        "Amount ₹": (opt_weights * inv_amt).astype(int),
                        "Sector": [SECTOR_MAP.get(t, 'Others') for t in top_tickers]
                    })
                    st.dataframe(alloc_df, use_container_width=True, hide_index=True)
                with c2:
                    fig_pie = px.pie(alloc_df, values='Weight %', names='Stock', hole=0.5,
                                    title="Capital Allocation", color_discrete_sequence=px.colors.qualitative.Set3)
                    fig_pie.update_layout(template="plotly_dark")
                    st.plotly_chart(fig_pie, use_container_width=True)
                with c3:
                    fig_sector = px.pie(alloc_df, values='Weight %', names='Sector', hole=0.5,
                                       title="Sector Exposure")
                    fig_sector.update_layout(template="plotly_dark")
                    st.plotly_chart(fig_sector, use_container_width=True)

                # Backtest
                st.markdown("### 📈 2-Year Backtest")
                port_hist = (daily_ret[top_tickers] * opt_weights).sum(axis=1)
                port_cum = (1 + port_hist).cumprod()
                
                fig_bt = go.Figure()
                fig_bt.add_trace(go.Scatter(x=port_cum.index, y=port_cum.values, name="Portfolio",
                                           line=dict(color='#00c48c', width=2.5)))
                if benchmark is not None:
                    bm_ret = benchmark.pct_change().dropna()
                    bm_cum = (1 + bm_ret).cumprod().reindex(port_cum.index).ffill()
                    fig_bt.add_trace(go.Scatter(x=bm_cum.index, y=bm_cum.values, name="Nifty 50",
                                               line=dict(color='#8b949e', width=1.5, dash='dash')))
                
                # Drawdown subplot
                port_dd = (port_cum - port_cum.cummax()) / port_cum.cummax() * 100
                fig_bt.add_trace(go.Scatter(x=port_dd.index, y=port_dd.values, name="Drawdown %",
                                           fill='tozeroy', line=dict(color='#ff4d6d', width=1),
                                           yaxis='y2'))
                fig_bt.update_layout(
                    template="plotly_dark", height=500,
                    yaxis=dict(title="Growth (1.0 = Start)"),
                    yaxis2=dict(title="Drawdown %", overlaying='y', side='right', showgrid=False),
                    legend=dict(orientation="h", yanchor="bottom", y=1.02)
                )
                st.plotly_chart(fig_bt, use_container_width=True)
                
                # Risk metrics
                rm1, rm2, rm3, rm4, rm5 = st.columns(5)
                rm1.metric("Ann. Return", f"{opt_ret*100:.1f}%")
                rm2.metric("Ann. Volatility", f"{opt_vol*100:.1f}%")
                rm3.metric("Sharpe Ratio", f"{opt_sharpe:.2f}")
                rm4.metric("Max Drawdown", f"{calc_max_drawdown(port_cum)*100:.1f}%")
                rm5.metric("Sortino", f"{calc_sortino_ratio(port_hist):.2f}")


# ==============================================================================
# 6. CORRELATION & CLUSTERING
# ==============================================================================
elif app_mode == "🔗 Correlation & Clustering":
    st.markdown("""
    <div class="terminal-header">
        <h1>🔗 Correlation & Clustering Scanner</h1>
        <div class="subtitle">Hierarchical clustering, pair trading candidates, and diversification analysis</div>
    </div>
    """, unsafe_allow_html=True)

    target = st.text_input("Target Ticker (blank for full analysis)", "RELIANCE.NS").strip().upper()
    
    if st.button("🔍 Analyze", type="primary"):
        with st.spinner("⚡ Computing correlations..."):
            raw = fetch_data(TICKER_LIST, "1y")

        if not raw.empty and 'Close' in raw.columns:
            returns = raw['Close'].pct_change().dropna()
            returns = returns.loc[:, returns.isna().sum() < len(returns) * 0.05].ffill().bfill()
            corr_matrix = returns.corr()

            tab1, tab2, tab3 = st.tabs(["🗺️ Heatmap", "🌳 Dendrogram", "📊 Pairs"])
            
            with tab1:
                # Sector-ordered heatmap
                sectors_ordered = sorted(set(SECTOR_MAP.values()))
                ticker_order = []
                for sec in sectors_ordered:
                    sec_tickers = [t for t in corr_matrix.columns if SECTOR_MAP.get(t, 'Others') == sec]
                    ticker_order.extend(sec_tickers)
                ticker_order = [t for t in ticker_order if t in corr_matrix.columns]
                
                fig_heat = go.Figure(data=go.Heatmap(
                    z=corr_matrix.loc[ticker_order, ticker_order].values,
                    x=[t.replace('.NS','') for t in ticker_order],
                    y=[t.replace('.NS','') for t in ticker_order],
                    colorscale='RdBu_r', zmid=0, zmin=-1, zmax=1
                ))
                fig_heat.update_layout(title="Correlation Matrix (Sector-Ordered)", template="plotly_dark",
                                      height=800, width=900)
                st.plotly_chart(fig_heat, use_container_width=True)
            
            with tab2:
                # Hierarchical clustering
                dist_matrix = 1 - corr_matrix.values
                np.fill_diagonal(dist_matrix, 0)
                dist_matrix = np.clip(dist_matrix, 0, 2)
                condensed = dist_matrix[np.triu_indices_from(dist_matrix, k=1)]
                Z = linkage(condensed, method='ward')
                
                fig_dend = go.Figure()
                fig_dend.add_trace(go.Scatter(
                    x=list(range(len(corr_matrix))),
                    y=[0]*len(corr_matrix),
                    mode='markers',
                    marker=dict(size=1, color='transparent'),
                    showlegend=False
                ))
                # Use scipy dendrogram data
                from scipy.cluster.hierarchy import dendrogram as scipy_dendrogram
                dn = scipy_dendrogram(Z, labels=[t.replace('.NS','') for t in corr_matrix.columns], no_plot=True)
                
                fig_dend = go.Figure()
                for i, (icoord, dcoord) in enumerate(zip(dn['icoord'], dn['dcoord'])):
                    fig_dend.add_trace(go.Scatter(x=icoord, y=dcoord, mode='lines',
                                                  line=dict(color='#58a6ff', width=1), showlegend=False))
                fig_dend.update_layout(title="Hierarchical Clustering Dendrogram", template="plotly_dark",
                                      height=500, xaxis_title="Stocks", yaxis_title="Distance")
                st.plotly_chart(fig_dend, use_container_width=True)
                
                # Cluster assignments
                n_clusters = st.slider("Number of Clusters", 3, 15, 8)
                clusters = fcluster(Z, n_clusters, criterion='maxclust')
                cluster_df = pd.DataFrame({'Ticker': corr_matrix.columns.str.replace('.NS',''), 'Cluster': clusters})
                st.dataframe(cluster_df.sort_values('Cluster'), use_container_width=True)
            
            with tab3:
                if target and target in corr_matrix.columns:
                    st.subheader(f"Inverse Correlations for {target.replace('.NS','')}")
                    target_corr = corr_matrix[target].drop(target).sort_values()
                    top_inv = target_corr.head(15).reset_index()
                    top_inv.columns = ['Ticker', 'Correlation']
                    top_inv['Ticker'] = top_inv['Ticker'].str.replace('.NS', '')
                    st.dataframe(top_inv.style.background_gradient(subset=['Correlation'], cmap="Reds_r"), use_container_width=True)
                else:
                    st.subheader("Top Negatively Correlated Pairs")
                    mask = np.tril(np.ones_like(corr_matrix, dtype=bool), k=-1)
                    pairs = corr_matrix.where(mask).stack().reset_index()
                    pairs.columns = ["T1", "T2", "Corr"]
                    pairs = pairs.sort_values("Corr").head(20)
                    pairs['T1'] = pairs['T1'].str.replace('.NS', '')
                    pairs['T2'] = pairs['T2'].str.replace('.NS', '')
                    st.dataframe(pairs.style.background_gradient(subset=['Corr'], cmap="Reds_r"), use_container_width=True)


# ==============================================================================
# 7. PROBABILITY & MONTE CARLO
# ==============================================================================
elif app_mode == "🎲 Probability & Monte Carlo":
    st.markdown("""
    <div class="terminal-header">
        <h1>🎲 Probability & Monte Carlo Engine</h1>
        <div class="subtitle">Multi-timeframe analysis, conditional probabilities, and 10,000-path simulation</div>
    </div>
    """, unsafe_allow_html=True)

    ticker = st.text_input("Ticker", "RELIANCE.NS").strip().upper()
    if st.button("🎯 Analyze", type="primary") and ticker:
        with st.spinner(f"⚡ Analyzing {ticker}..."):
            df = fetch_single_ticker(ticker, "5y")

        if not df.empty and len(df) > 30:
            df = df.dropna(subset=['Close'])
            ltp = df['Close'].iloc[-1]
            
            st.markdown(f"### {ticker.replace('.NS','')} — LTP: **₹{ltp:,.2f}**")
            
            tab1, tab2, tab3, tab4 = st.tabs(["📊 Probability", "🎰 Monte Carlo", "📐 Timeframes", "📉 Volatility"])
            
            with tab1:
                df['Return'] = df['Close'].pct_change()
                df['Direction'] = df['Return'].apply(lambda x: 'Up' if x > 0 else 'Down')
                df['Prev_Dir'] = df['Direction'].shift(1)
                
                last_dir = df['Direction'].iloc[-1]
                sim = df[df['Prev_Dir'] == last_dir]
                up_prob = (sim['Direction'] == 'Up').mean() * 100 if len(sim) > 0 else 50
                
                c1, c2, c3 = st.columns(3)
                c1.metric("After UP Day → UP", f"{up_prob:.1f}%")
                c2.metric("After UP Day → DOWN", f"{100-up_prob:.1f}%")
                c3.metric("Sample Size", f"{len(sim)} days")
                
                # Day-of-week analysis
                df['DOW'] = df.index.day_name()
                dow_stats = df.groupby('DOW')['Return'].agg(['mean', 'std', 'count']) * 100
                dow_stats = dow_stats.reindex(['Monday','Tuesday','Wednesday','Thursday','Friday'])
                st.markdown("#### Day-of-Week Returns")
                st.dataframe(dow_stats.style.background_gradient(subset=['mean'], cmap="RdYlGn"))
            
            with tab2:
                st.markdown("#### 10,000-Path Monte Carlo Simulation (252 days)")
                returns = df['Return'].dropna()
                mc_results = monte_carlo_simulation(returns, ltp, 252, 10000)
                
                fig_mc = go.Figure()
                # Plot percentile bands
                p5 = np.percentile(mc_results, 5, axis=0)
                p25 = np.percentile(mc_results, 25, axis=0)
                p50 = np.percentile(mc_results, 50, axis=0)
                p75 = np.percentile(mc_results, 75, axis=0)
                p95 = np.percentile(mc_results, 95, axis=0)
                
                days_range = list(range(252))
                fig_mc.add_trace(go.Scatter(x=days_range, y=p95, line=dict(width=0), showlegend=False))
                fig_mc.add_trace(go.Scatter(x=days_range, y=p5, fill='tonexty', fillcolor='rgba(88,166,255,0.1)',
                                           line=dict(width=0), name='5-95% Range'))
                fig_mc.add_trace(go.Scatter(x=days_range, y=p75, line=dict(width=0), showlegend=False))
                fig_mc.add_trace(go.Scatter(x=days_range, y=p25, fill='tonexty', fillcolor='rgba(0,196,140,0.2)',
                                           line=dict(width=0), name='25-75% Range'))
                fig_mc.add_trace(go.Scatter(x=days_range, y=p50, line=dict(color='#e3b341', width=2), name='Median'))
                fig_mc.add_hline(y=ltp, line_dash="dash", line_color="#8b949e", annotation_text="Current")
                
                fig_mc.update_layout(title="Monte Carlo Price Projection", template="plotly_dark",
                                    xaxis_title="Trading Days", yaxis_title="Price (₹)", height=500)
                st.plotly_chart(fig_mc, use_container_width=True)
                
                # Terminal distribution
                terminal = mc_results[:, -1]
                mc1, mc2, mc3, mc4 = st.columns(4)
                mc1.metric("Median (1Y)", f"₹{np.median(terminal):,.0f}")
                mc2.metric("5th Percentile", f"₹{np.percentile(terminal, 5):,.0f}")
                mc3.metric("95th Percentile", f"₹{np.percentile(terminal, 95):,.0f}")
                mc4.metric("P(Loss)", f"{(terminal < ltp).mean()*100:.1f}%")
            
            with tab3:
                def analyze_tf(data, windows, label):
                    results = []
                    temp = data.copy()
                    temp['Ret'] = temp['Close'].pct_change() * 100
                    temp['Swing'] = ((temp['High'] - temp['Low']) / temp['Low']) * 100
                    for w in windows:
                        if len(temp) >= w:
                            subset = temp.tail(w)
                            results.append({
                                "Window": f"Last {w} {label}",
                                "Avg Swing %": f"{subset['Swing'].mean():.2f}",
                                "Avg Up %": f"{subset['Ret'][subset['Ret']>0].mean():.2f}",
                                "Avg Down %": f"{subset['Ret'][subset['Ret']<0].mean():.2f}",
                                "Proj Low": f"₹{ltp * (1 - abs(subset['Ret'][subset['Ret']<0].mean())/100):,.0f}",
                                "Proj High": f"₹{ltp * (1 + subset['Ret'][subset['Ret']>0].mean()/100):,.0f}",
                            })
                    return pd.DataFrame(results) if results else None
                
                t1, t2, t3 = st.columns(3)
                with t1:
                    st.markdown("**Daily**")
                    r = analyze_tf(df, [20, 60, 120, 250], "days")
                    if r is not None: st.dataframe(r, use_container_width=True, hide_index=True)
                with t2:
                    st.markdown("**Weekly**")
                    df_w = df.resample('W-FRI').agg({'Open':'first','High':'max','Low':'min','Close':'last'}).dropna()
                    r = analyze_tf(df_w, [12, 26, 52], "weeks")
                    if r is not None: st.dataframe(r, use_container_width=True, hide_index=True)
                with t3:
                    st.markdown("**Monthly**")
                    df_m = df.resample('ME').agg({'Open':'first','High':'max','Low':'min','Close':'last'}).dropna()
                    r = analyze_tf(df_m, [3, 6, 12], "months")
                    if r is not None: st.dataframe(r, use_container_width=True, hide_index=True)
            
            with tab4:
                # Rolling volatility
                df['Vol_20'] = df['Return'].rolling(20).std() * np.sqrt(TRADING_DAYS) * 100
                df['Vol_60'] = df['Return'].rolling(60).std() * np.sqrt(TRADING_DAYS) * 100
                
                fig_vol = go.Figure()
                fig_vol.add_trace(go.Scatter(x=df.index, y=df['Vol_20'], name='20D Vol', line=dict(color='#58a6ff')))
                fig_vol.add_trace(go.Scatter(x=df.index, y=df['Vol_60'], name='60D Vol', line=dict(color='#e3b341')))
                fig_vol.update_layout(title="Rolling Annualized Volatility", template="plotly_dark",
                                     yaxis_title="Volatility %", height=400)
                st.plotly_chart(fig_vol, use_container_width=True)


# ==============================================================================
# 8. OPTION CHAIN & STRATEGY
# ==============================================================================
elif app_mode == "⚡ Option Chain & Strategy":
    st.markdown("""
    <div class="terminal-header">
        <h1>⚡ Option Chain, Greeks & Strategy Builder</h1>
        <div class="subtitle">Live NSE data + Black-Scholes Greeks + Multi-leg strategy payoff diagrams</div>
    </div>
    """, unsafe_allow_html=True)

    main_tab1, main_tab2 = st.tabs(["📊 Live Option Chain", "🏗️ Strategy Builder"])
    
    with main_tab1:
        c1, c2, c3 = st.columns(3)
        mode = c1.selectbox("Mode", ["Index", "Stock"])
        idx_list, stk_list = fetch_nse_symbols()
        symbol = c2.selectbox("Symbol", idx_list if mode == "Index" else stk_list)
        expiries = fetch_nse_expiries(symbol)
        
        if not expiries:
            st.warning("⚠️ Cannot load expiries from NSE (rate-limited). Try locally.")
        else:
            expiry = c3.selectbox("Expiry", expiries)
            
            if st.button("📡 Fetch Chain", type="primary"):
                with st.spinner("Fetching..."):
                    merged, ts, points, err = fetch_option_chain_raw(symbol, expiry, mode)
                if err:
                    st.error(f"Error: {err}")
                else:
                    st.session_state['oc_data'] = {"df": merged, "ts": ts, "points": points, "symbol": symbol}
            
            if 'oc_data' in st.session_state:
                cached = st.session_state['oc_data']
                merged, ts, points = cached['df'], cached['ts'], cached['points']
                strikes = merged['Strike Price'].tolist()
                atm_sp = min(strikes, key=lambda x: abs(x - points))
                rf = 1000 if mode == 'Index' else 10
                
                st.markdown(f"**{symbol} @ ₹{points:,.2f}** · Updated: `{ts}`")
                sp = st.selectbox("Analysis Strike", sorted(strikes), index=sorted(strikes).index(atm_sp))
                
                m = analyse_oc(merged, sp, rf, points)
                
                if m:
                    sug = calc_suggestion(m, points)
                    
                    # Metrics row
                    mc1, mc2, mc3, mc4, mc5 = st.columns(5)
                    mc1.metric("PCR", m['pcr'])
                    mc2.metric("Max Pain", int(m['max_pain']), f"{int(m['max_pain']-points)} pts")
                    mc3.metric("CE IV", f"{m['ce_iv']}%")
                    mc4.metric("PE IV", f"{m['pe_iv']}%")
                    mc5.metric("IV Skew", f"{m['iv_skew']:+.2f}%")
                    
                    st.markdown(f"### Verdict: {sug['action']}")
                    st.markdown(f"Score: **{sug['score']:+d}/±10** | Confidence: **{sug['confidence']}** ({sug['conf_pct']}%)")
                    
                    for lbl, txt in sug['reasons']:
                        badge = {'BULLISH':'🟢','MILD BULL':'🟢','BEARISH':'🔴','MILD BEAR':'🔴',
                                'NEUTRAL':'🟡','CAUTION':'🟠'}.get(lbl, '⚪')
                        st.markdown(f"- {badge} **{lbl}:** {txt}")
                    
                    # Greeks
                    st.markdown("---")
                    st.markdown("### 📐 Greeks")
                    try:
                        exp_date = datetime.datetime.strptime(expiry, '%d-%b-%Y')
                        t_days = max((exp_date - datetime.datetime.now()).days, 1)
                    except: t_days = 7
                    
                    row = merged[merged['Strike Price'] == sp].iloc[0]
                    ce_g = calc_greeks(points, sp, t_days, row['CE IV'], 'CE')
                    pe_g = calc_greeks(points, sp, t_days, row['PE IV'], 'PE')
                    
                    g_df = pd.DataFrame([
                        {"Greek": "Delta (Δ)", "CE": f"{ce_g['delta']:+.4f}", "PE": f"{pe_g['delta']:+.4f}"},
                        {"Greek": "Gamma (Γ)", "CE": f"{ce_g['gamma']:.6f}", "PE": f"{pe_g['gamma']:.6f}"},
                        {"Greek": "Theta (Θ)", "CE": f"{ce_g['theta']:+.4f}", "PE": f"{pe_g['theta']:+.4f}"},
                        {"Greek": "Vega (ν)", "CE": f"{ce_g['vega']:+.4f}", "PE": f"{pe_g['vega']:+.4f}"},
                        {"Greek": "Rho (ρ)", "CE": f"{ce_g['rho']:+.4f}", "PE": f"{pe_g['rho']:+.4f}"},
                    ])
                    st.dataframe(g_df, use_container_width=True, hide_index=True)
                    
                    # OI Chart
                    fig_oi = go.Figure()
                    fig_oi.add_trace(go.Bar(x=merged['Strike Price'], y=merged['CE OI'], name='CE OI', marker_color='#f85149', opacity=0.8))
                    fig_oi.add_trace(go.Bar(x=merged['Strike Price'], y=-merged['PE OI'], name='PE OI', marker_color='#3fb950', opacity=0.8))
                    fig_oi.add_vline(x=points, line_color="#58a6ff", line_width=2, line_dash="dot", annotation_text="LTP")
                    fig_oi.update_layout(title="OI Distribution", barmode='overlay', template="plotly_dark", height=400)
                    st.plotly_chart(fig_oi, use_container_width=True)
    
    with main_tab2:
        st.markdown("### 🏗️ Options Strategy Payoff Builder")
        st.markdown("Build multi-leg strategies and visualize payoff at expiry.")
        
        spot_input = st.number_input("Underlying Price (₹)", min_value=1.0, value=24000.0, step=100.0)
        num_legs = st.slider("Number of Legs", 1, 4, 2)
        
        legs = []
        for i in range(num_legs):
            st.markdown(f"**Leg {i+1}**")
            lc1, lc2, lc3, lc4 = st.columns(4)
            action = lc1.selectbox("Action", ["BUY", "SELL"], key=f"action_{i}")
            opt_type = lc2.selectbox("Type", ["CE", "PE"], key=f"type_{i}")
            strike = lc3.number_input("Strike", min_value=1.0, value=spot_input, step=50.0, key=f"strike_{i}")
            premium = lc4.number_input("Premium (₹)", min_value=0.01, value=200.0, step=10.0, key=f"prem_{i}")
            legs.append((action, opt_type, strike, premium))
        
        if st.button("📈 Calculate Payoff"):
            spot_range = np.linspace(spot_input * 0.7, spot_input * 1.3, 500)
            payoffs = np.zeros(len(spot_range))
            
            for action, opt_type, strike, premium in legs:
                for j, s in enumerate(spot_range):
                    if opt_type == 'CE':
                        intrinsic = max(s - strike, 0)
                    else:
                        intrinsic = max(strike - s, 0)
                    if action == 'BUY':
                        payoffs[j] += intrinsic - premium
                    else:
                        payoffs[j] += premium - intrinsic
            
            fig_payoff = go.Figure()
            fig_payoff.add_trace(go.Scatter(x=spot_range, y=payoffs, mode='lines',
                                           line=dict(color='#58a6ff', width=2.5), name='Payoff'))
            fig_payoff.add_hline(y=0, line_color="#8b949e", line_width=1, line_dash="dash")
            fig_payoff.add_vline(x=spot_input, line_color="#e3b341", line_width=1.5, line_dash="dot", annotation_text="Spot")
            
            # Fill profit/loss zones
            fig_payoff.add_trace(go.Scatter(x=spot_range, y=np.maximum(payoffs, 0),
                                           fill='tozeroy', fillcolor='rgba(0,196,140,0.15)',
                                           line=dict(width=0), name='Profit Zone'))
            fig_payoff.add_trace(go.Scatter(x=spot_range, y=np.minimum(payoffs, 0),
                                           fill='tozeroy', fillcolor='rgba(255,77,109,0.15)',
                                           line=dict(width=0), name='Loss Zone'))
            
            max_profit = payoffs.max()
            max_loss = payoffs.min()
            breakevens = spot_range[np.where(np.diff(np.sign(payoffs)))[0]] if len(np.where(np.diff(np.sign(payoffs)))[0]) > 0 else []
            
            fig_payoff.update_layout(title="Strategy Payoff at Expiry", template="plotly_dark",
                                    xaxis_title="Underlying Price", yaxis_title="P&L (₹)", height=450)
            st.plotly_chart(fig_payoff, use_container_width=True)
            
            m1, m2, m3 = st.columns(3)
            m1.metric("Max Profit", f"₹{max_profit:,.0f}" if max_profit < 1e6 else "Unlimited")
            m2.metric("Max Loss", f"₹{max_loss:,.0f}" if max_loss > -1e6 else "Unlimited")
            m3.metric("Breakeven(s)", ", ".join([f"₹{b:,.0f}" for b in breakevens]) if len(breakevens) > 0 else "N/A")


# ==============================================================================
# 9. IPO INTELLIGENCE
# ==============================================================================
elif app_mode == "🚀 IPO Intelligence":
    st.markdown("""
    <div class="terminal-header">
        <h1>🚀 IPO Intelligence Dashboard</h1>
        <div class="subtitle">Track upcoming, recent, and below-price IPOs with analytics</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["📅 Upcoming", "🆕 Recent Listings", "📉 Below IPO Price", "📊 Analytics"])
    
    with tab1:
        st.markdown("### Upcoming IPOs")
        ipo_up_df = pd.DataFrame(IPO_UPCOMING)
        st.dataframe(ipo_up_df, use_container_width=True, hide_index=True)
        st.info("💡 **Jayesh Logistics** (₹106 Cr) and **Shreeji Global** (₹284 Cr) are in the pipeline.")
    
    with tab2:
        st.markdown("### Recently Listed (Last 30 Days)")
        ipo_rec_df = pd.DataFrame(IPO_RECENT)
        st.dataframe(ipo_rec_df.style.background_gradient(subset=['% Change'], cmap="RdYlGn"), use_container_width=True, hide_index=True)
        
        # Top gainers chart
        fig_ipo = px.bar(ipo_rec_df.sort_values('% Change'), x='% Change', y='Name', orientation='h',
                        color='% Change', color_continuous_scale='RdYlGn', title="Recent IPO Performance")
        fig_ipo.update_layout(template="plotly_dark", height=500)
        st.plotly_chart(fig_ipo, use_container_width=True)
    
    with tab3:
        st.markdown("### Trading Below IPO Price")
        ipo_bel_df = pd.DataFrame(IPO_BELOW_PRICE)
        st.dataframe(ipo_bel_df.style.background_gradient(subset=['% Change'], cmap="Reds_r"), use_container_width=True, hide_index=True)
        
        # Worst performers
        fig_bel = px.bar(ipo_bel_df.sort_values('% Change'), x='% Change', y='Name', orientation='h',
                        color='% Change', color_continuous_scale='Reds_r', title="Biggest IPO Losers")
        fig_bel.update_layout(template="plotly_dark", height=500)
        st.plotly_chart(fig_bel, use_container_width=True)
    
    with tab4:
        st.markdown("### 📊 IPO Market Analytics")
        all_ipos = IPO_RECENT + IPO_BELOW_PRICE
        all_df = pd.DataFrame(all_ipos)
        
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Tracked", len(all_df))
        c2.metric("Above IPO Price", len(all_df[all_df['% Change'] > 0]))
        c3.metric("Below IPO Price", len(all_df[all_df['% Change'] < 0]))
        c4.metric("Avg Return", f"{all_df['% Change'].mean():.1f}%")
        
        # MCap vs Performance scatter
        fig_scatter = px.scatter(all_df, x='IPO MCap', y='% Change', size='IPO MCap',
                                color='% Change', color_continuous_scale='RdYlGn',
                                hover_name='Name', title="IPO MCap vs Listing Performance",
                                log_x=True)
        fig_scatter.add_hline(y=0, line_dash="dash", line_color="#8b949e")
        fig_scatter.update_layout(template="plotly_dark", height=450)
        st.plotly_chart(fig_scatter, use_container_width=True)


# ==============================================================================
# 10. TECHNICAL WORKBENCH
# ==============================================================================
elif app_mode == "📊 Technical Workbench":
    st.markdown("""
    <div class="terminal-header">
        <h1>📊 Technical Analysis Workbench</h1>
        <div class="subtitle">Candlestick charts, 15+ indicators, S/R levels, Fibonacci, and pivot points</div>
    </div>
    """, unsafe_allow_html=True)

    ticker = st.text_input("Ticker Symbol", "RELIANCE.NS").strip().upper()
    period = st.selectbox("Period", ["3mo", "6mo", "1y", "2y", "5y"], index=2)
    
    if st.button("📈 Load Chart", type="primary"):
        with st.spinner(f"Loading {ticker}..."):
            df = fetch_single_ticker(ticker, period)
        
        if not df.empty and len(df) > 20:
            df = df.dropna(subset=['Close'])
            ltp = df['Close'].iloc[-1]
            
            # Calculate all indicators
            df['SMA_20'] = df['Close'].rolling(20).mean()
            df['SMA_50'] = df['Close'].rolling(50).mean()
            df['SMA_200'] = df['Close'].rolling(200).mean()
            df['EMA_12'] = df['Close'].ewm(span=12).mean()
            df['EMA_26'] = df['Close'].ewm(span=26).mean()
            df['RSI'] = calc_rsi(df['Close'])
            df['MACD'], df['Signal'], df['Hist'] = calc_macd(df['Close'])
            df['BB_Upper'], df['BB_Mid'], df['BB_Lower'] = calc_bollinger(df['Close'])
            df['ATR'] = calc_atr(df['High'], df['Low'], df['Close'])
            df['VWAP'] = calc_vwap(df)
            df['OBV'] = calc_obv(df)
            df['Stoch_K'], df['Stoch_D'] = calc_stochastic(df['High'], df['Low'], df['Close'])
            df['ADX'], df['Plus_DI'], df['Minus_DI'] = calc_adx(df['High'], df['Low'], df['Close'])
            
            # S/R Levels
            supports, resistances = detect_support_resistance(df)
            fib_levels = calc_fibonacci_levels(df['High'].max(), df['Low'].min())
            pivots = calc_pivot_points(df['High'].iloc[-1], df['Low'].iloc[-1], df['Close'].iloc[-1])
            
            # Main candlestick chart with overlays
            fig = make_subplots(
                rows=4, cols=1, shared_xaxes=True,
                vertical_spacing=0.03,
                row_heights=[0.5, 0.15, 0.15, 0.2],
                subplot_titles=("Price & Indicators", "Volume", "RSI / Stochastic", "MACD")
            )
            
            # Candlestick
            fig.add_trace(go.Candlestick(x=df.index, open=df['Open'], high=df['High'],
                                        low=df['Low'], close=df['Close'], name='OHLC',
                                        increasing_line_color='#00c48c', decreasing_line_color='#ff4d6d'), row=1, col=1)
            
            # MAs
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_20'], name='SMA 20',
                                    line=dict(color='#e3b341', width=1)), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['SMA_50'], name='SMA 50',
                                    line=dict(color='#58a6ff', width=1.5)), row=1, col=1)
            if df['SMA_200'].notna().any():
                fig.add_trace(go.Scatter(x=df.index, y=df['SMA_200'], name='SMA 200',
                                        line=dict(color='#bc8cff', width=2)), row=1, col=1)
            
            # Bollinger Bands
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_Upper'], name='BB Upper',
                                    line=dict(color='rgba(88,166,255,0.3)', width=1, dash='dot')), row=1, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['BB_Lower'], name='BB Lower',
                                    line=dict(color='rgba(88,166,255,0.3)', width=1, dash='dot'),
                                    fill='tonexty', fillcolor='rgba(88,166,255,0.05)'), row=1, col=1)
            
            # VWAP
            fig.add_trace(go.Scatter(x=df.index, y=df['VWAP'], name='VWAP',
                                    line=dict(color='#ff9800', width=1, dash='dash')), row=1, col=1)
            
            # S/R levels
            for s in supports[-3:]:
                fig.add_hline(y=s, line_color="rgba(0,196,140,0.4)", line_width=1, line_dash="dash", row=1, col=1)
            for r in resistances[-3:]:
                fig.add_hline(y=r, line_color="rgba(255,77,109,0.4)", line_width=1, line_dash="dash", row=1, col=1)
            
            # Volume
            colors = ['#00c48c' if c >= o else '#ff4d6d' for c, o in zip(df['Close'], df['Open'])]
            fig.add_trace(go.Bar(x=df.index, y=df['Volume'], marker_color=colors, name='Volume', opacity=0.6), row=2, col=1)
            
            # RSI
            fig.add_trace(go.Scatter(x=df.index, y=df['RSI'], name='RSI(14)',
                                    line=dict(color='#bc8cff', width=1.5)), row=3, col=1)
            fig.add_hline(y=70, line_color="#ff4d6d", line_width=1, line_dash="dash", row=3, col=1)
            fig.add_hline(y=30, line_color="#00c48c", line_width=1, line_dash="dash", row=3, col=1)
            
            # MACD
            fig.add_trace(go.Scatter(x=df.index, y=df['MACD'], name='MACD',
                                    line=dict(color='#58a6ff', width=1.5)), row=4, col=1)
            fig.add_trace(go.Scatter(x=df.index, y=df['Signal'], name='Signal',
                                    line=dict(color='#e3b341', width=1)), row=4, col=1)
            hist_colors = ['#00c48c' if h >= 0 else '#ff4d6d' for h in df['Hist'].fillna(0)]
            fig.add_trace(go.Bar(x=df.index, y=df['Hist'], marker_color=hist_colors, name='Histogram', opacity=0.5), row=4, col=1)
            
            fig.update_layout(height=900, template="plotly_dark", xaxis_rangeslider_visible=False,
                             legend=dict(orientation="h", yanchor="bottom", y=1.02),
                             title=f"{ticker.replace('.NS','')} — Technical Analysis")
            st.plotly_chart(fig, use_container_width=True)
            
            # Indicator summary
            st.markdown("### 📋 Indicator Summary")
            rsi_val = df['RSI'].iloc[-1]
            macd_val = df['MACD'].iloc[-1]
            sig_val = df['Signal'].iloc[-1]
            adx_val = df['ADX'].iloc[-1] if df['ADX'].notna().any() else 0
            
            ic1, ic2, ic3, ic4, ic5, ic6 = st.columns(6)
            ic1.metric("RSI(14)", f"{rsi_val:.1f}", "Overbought" if rsi_val > 70 else ("Oversold" if rsi_val < 30 else "Neutral"))
            ic2.metric("MACD", f"{macd_val:.2f}", "Bullish" if macd_val > sig_val else "Bearish")
            ic3.metric("ADX", f"{adx_val:.1f}", "Strong" if adx_val > 25 else "Weak")
            ic4.metric("ATR(14)", f"₹{df['ATR'].iloc[-1]:.1f}")
            ic5.metric("Stoch %K", f"{df['Stoch_K'].iloc[-1]:.1f}")
            ic6.metric("Price vs VWAP", "Above ✅" if ltp > df['VWAP'].iloc[-1] else "Below ❌")
            
            # Fibonacci & Pivots
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("#### Fibonacci Levels")
                fib_df = pd.DataFrame(list(fib_levels.items()), columns=['Level', 'Price'])
                st.dataframe(fib_df, use_container_width=True, hide_index=True)
            with c2:
                st.markdown("#### Pivot Points")
                piv_df = pd.DataFrame(list(pivots.items()), columns=['Level', 'Price'])
                st.dataframe(piv_df, use_container_width=True, hide_index=True)


# ==============================================================================
# 11. RISK MANAGEMENT SUITE
# ==============================================================================
elif app_mode == "🛡️ Risk Management Suite":
    st.markdown("""
    <div class="terminal-header">
        <h1>🛡️ Risk Management Suite</h1>
        <div class="subtitle">VaR, CVaR, Drawdown analysis, Kelly Criterion, and position sizing</div>
    </div>
    """, unsafe_allow_html=True)

    ticker = st.text_input("Ticker", "RELIANCE.NS").strip().upper()
    capital = st.number_input("Capital (₹)", min_value=10000, value=100000, step=10000)
    
    if st.button("🛡️ Run Risk Analysis", type="primary"):
        with st.spinner("Computing risk metrics..."):
            df = fetch_single_ticker(ticker, "3y")
        
        if not df.empty and len(df) > 50:
            df = df.dropna(subset=['Close'])
            returns = df['Close'].pct_change().dropna()
            ltp = df['Close'].iloc[-1]
            
            tab1, tab2, tab3, tab4 = st.tabs(["📉 VaR & CVaR", "📊 Drawdown", "🎯 Position Sizing", "📈 Distribution"])
            
            with tab1:
                var_95_h = calc_var(returns, 0.95, 'historical')
                var_99_h = calc_var(returns, 0.99, 'historical')
                var_95_p = calc_var(returns, 0.95, 'parametric')
                cvar_95 = calc_cvar(returns, 0.95)
                
                vc1, vc2, vc3, vc4 = st.columns(4)
                vc1.metric("VaR 95% (Hist)", f"{var_95_h*100:.2f}%", f"₹{var_95_h*capital:,.0f}")
                vc2.metric("VaR 99% (Hist)", f"{var_99_h*100:.2f}%", f"₹{var_99_h*capital:,.0f}")
                vc3.metric("VaR 95% (Param)", f"{var_95_p*100:.2f}%")
                vc4.metric("CVaR 95%", f"{cvar_95*100:.2f}%", f"₹{cvar_95*capital:,.0f}")
                
                st.markdown(f"""
                **Interpretation:** With 95% confidence, your ₹{capital:,.0f} position in {ticker.replace('.NS','')} 
                will NOT lose more than **₹{abs(var_95_h*capital):,.0f}** in a single day.
                In the worst 5% of cases, expected loss is **₹{abs(cvar_95*capital):,.0f}**.
                """)
            
            with tab2:
                cum_returns = (1 + returns).cumprod()
                drawdown = (cum_returns - cum_returns.cummax()) / cum_returns.cummax() * 100
                mdd = drawdown.min()
                
                fig_dd = go.Figure()
                fig_dd.add_trace(go.Scatter(x=drawdown.index, y=drawdown.values,
                                           fill='tozeroy', fillcolor='rgba(255,77,109,0.2)',
                                           line=dict(color='#ff4d6d', width=1.5), name='Drawdown'))
                fig_dd.add_hline(y=mdd, line_dash="dash", line_color="#e3b341",
                                annotation_text=f"Max DD: {mdd:.1f}%")
                fig_dd.update_layout(title="Drawdown Analysis", template="plotly_dark",
                                    yaxis_title="Drawdown %", height=400)
                st.plotly_chart(fig_dd, use_container_width=True)
                
                # Drawdown statistics
                dd_stats = pd.DataFrame({
                    'Metric': ['Max Drawdown', 'Avg Drawdown', 'Max DD Duration (days)', 'Recovery Time'],
                    'Value': [f"{mdd:.1f}%", f"{drawdown[drawdown<0].mean():.1f}%",
                             "—", "—"]
                })
                st.dataframe(dd_stats, use_container_width=True, hide_index=True)
            
            with tab3:
                st.markdown("#### 🎯 Kelly Criterion Position Sizing")
                wins = returns[returns > 0]
                losses = returns[returns < 0]
                win_rate = len(wins) / len(returns)
                avg_win = wins.mean()
                avg_loss = losses.mean()
                
                kelly = calc_kelly_fraction(win_rate, avg_win, avg_loss)
                half_kelly = kelly / 2
                quarter_kelly = kelly / 4
                
                shares_full = int((capital * kelly) / ltp)
                shares_half = int((capital * half_kelly) / ltp)
                
                kc1, kc2, kc3, kc4 = st.columns(4)
                kc1.metric("Win Rate", f"{win_rate*100:.1f}%")
                kc2.metric("Avg Win/Loss", f"{abs(avg_win/avg_loss):.2f}")
                kc3.metric("Kelly %", f"{kelly*100:.1f}%")
                kc4.metric("Optimal Shares", f"{shares_full}")
                
                st.markdown(f"""
                | Strategy | Allocation | Shares | Amount |
                |----------|-----------|--------|--------|
                | Full Kelly | {kelly*100:.1f}% | {shares_full} | ₹{shares_full*ltp:,.0f} |
                | Half Kelly (Recommended) | {half_kelly*100:.1f}% | {shares_half} | ₹{shares_half*ltp:,.0f} |
                | Quarter Kelly (Conservative) | {quarter_kelly*100:.1f}% | {int(quarter_kelly*capital/ltp)} | ₹{int(quarter_kelly*capital/ltp)*ltp:,.0f} |
                """)
                
                # Risk-reward calculator
                st.markdown("#### 📐 Risk-Reward Calculator")
                entry = st.number_input("Entry Price", value=ltp, step=1.0)
                stop_loss = st.number_input("Stop Loss", value=ltp * 0.97, step=1.0)
                target = st.number_input("Target", value=ltp * 1.06, step=1.0)
                
                risk = abs(entry - stop_loss)
                reward = abs(target - entry)
                rr_ratio = reward / risk if risk > 0 else 0
                
                st.metric("Risk:Reward", f"1:{rr_ratio:.2f}",
                         "✅ Good" if rr_ratio >= 2 else "⚠️ Marginal" if rr_ratio >= 1 else "❌ Poor")
            
            with tab4:
                fig_dist = go.Figure()
                fig_dist.add_trace(go.Histogram(x=returns*100, nbinsx=80, marker_color='#58a6ff',
                                               opacity=0.7, name='Daily Returns'))
                fig_dist.add_vline(x=var_95_h*100, line_color="#ff4d6d", line_width=2,
                                  annotation_text=f"VaR 95%: {var_95_h*100:.2f}%")
                fig_dist.add_vline(x=0, line_color="#8b949e", line_width=1, line_dash="dash")
                
                # Normal overlay
                x_range = np.linspace(returns.min()*100, returns.max()*100, 100)
                normal_pdf = stats.norm.pdf(x_range, returns.mean()*100, returns.std()*100)
                fig_dist.add_trace(go.Scatter(x=x_range, y=normal_pdf * len(returns) * (returns.std()*100*80/5),
                                            line=dict(color='#e3b341', width=2, dash='dash'), name='Normal Fit'))
                
                fig_dist.update_layout(title="Return Distribution vs Normal", template="plotly_dark",
                                      xaxis_title="Daily Return %", yaxis_title="Frequency", height=400)
                st.plotly_chart(fig_dist, use_container_width=True)
                
                # Tail risk metrics
                skew = returns.skew()
                kurt = returns.kurtosis()
                st.markdown(f"**Skewness:** {skew:.3f} {'(Left-tailed risk ⚠️)' if skew < -0.5 else '(Approx. symmetric ✅)'}")
                st.markdown(f"**Kurtosis:** {kurt:.3f} {'(Fat tails — extreme events more likely ⚠️)' if kurt > 3 else '(Near-normal tails ✅)'}")


# ==============================================================================
# 12. WATCHLIST & ALERTS
# ==============================================================================
elif app_mode == "⭐ Watchlist & Alerts":
    st.markdown("""
    <div class="terminal-header">
        <h1>⭐ Watchlist & Price Alerts</h1>
        <div class="subtitle">Track your favorites and set threshold-based alerts</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["⭐ Watchlist", "🔔 Alerts"])
    
    with tab1:
        st.markdown("### Manage Watchlist")
        new_ticker = st.text_input("Add Ticker (e.g., TCS.NS)", "").strip().upper()
        if st.button("➕ Add") and new_ticker:
            if new_ticker not in st.session_state.watchlist:
                st.session_state.watchlist.append(new_ticker)
                st.success(f"Added {new_ticker}")
            else:
                st.warning("Already in watchlist")
        
        if st.session_state.watchlist:
            st.markdown("### 📊 Watchlist Performance")
            with st.spinner("Fetching watchlist data..."):
                wl_data = fetch_data(st.session_state.watchlist, "1mo")
            
            if not wl_data.empty and 'Close' in wl_data.columns:
                wl_close = wl_data['Close'].ffill().bfill()
                wl_records = []
                for t in st.session_state.watchlist:
                    if t in wl_close.columns:
                        s = wl_close[t].dropna()
                        if len(s) >= 2:
                            wl_records.append({
                                "Ticker": t.replace(".NS", ""),
                                "LTP": round(s.iloc[-1], 2),
                                "1D %": round((s.iloc[-1]/s.iloc[-2]-1)*100, 2),
                                "1W %": round((s.iloc[-1]/s.iloc[-6]-1)*100, 2) if len(s) >= 6 else "—",
                                "1M %": round((s.iloc[-1]/s.iloc[0]-1)*100, 2),
                                "Sector": SECTOR_MAP.get(t, "—"),
                            })
                
                if wl_records:
                    wl_df = pd.DataFrame(wl_records)
                    st.dataframe(wl_df.style.background_gradient(subset=['1D %', '1M %'], cmap="RdYlGn"),
                                use_container_width=True, hide_index=True)
                    
                    # Mini sparklines
                    fig_wl = make_subplots(rows=len(st.session_state.watchlist), cols=1,
                                          subplot_titles=[t.replace('.NS','') for t in st.session_state.watchlist],
                                          vertical_spacing=0.05)
                    for i, t in enumerate(st.session_state.watchlist):
                        if t in wl_close.columns:
                            s = wl_close[t].dropna()
                            color = '#00c48c' if s.iloc[-1] >= s.iloc[0] else '#ff4d6d'
                            fig_wl.add_trace(go.Scatter(x=s.index, y=s.values, mode='lines',
                                                       line=dict(color=color, width=1.5), showlegend=False),
                                           row=i+1, col=1)
                    fig_wl.update_layout(height=200*len(st.session_state.watchlist), template="plotly_dark")
                    st.plotly_chart(fig_wl, use_container_width=True)
            
            # Remove from watchlist
            remove_ticker = st.selectbox("Remove from watchlist", st.session_state.watchlist)
            if st.button("🗑️ Remove"):
                st.session_state.watchlist.remove(remove_ticker)
                st.rerun()
        else:
            st.info("Watchlist is empty. Add tickers above.")
    
    with tab2:
        st.markdown("### 🔔 Price Alerts")
        st.markdown("*Alerts are checked against latest available data (session-based).*")
        
        ac1, ac2, ac3, ac4 = st.columns(4)
        alert_ticker = ac1.text_input("Ticker", "RELIANCE.NS").strip().upper()
        alert_type = ac2.selectbox("Condition", ["Above", "Below"])
        alert_price = ac3.number_input("Price (₹)", min_value=0.01, value=2500.0, step=10.0)
        
        if ac4.button("🔔 Set Alert"):
            st.session_state.alerts.append({
                'ticker': alert_ticker, 'type': alert_type, 'price': alert_price,
                'time': datetime.datetime.now().strftime('%H:%M:%S')
            })
            st.success(f"Alert set: {alert_ticker} {alert_type} ₹{alert_price}")
        
        if st.session_state.alerts:
            st.markdown("#### Active Alerts")
            alerts_df = pd.DataFrame(st.session_state.alerts)
            st.dataframe(alerts_df, use_container_width=True, hide_index=True)
            
            # Check alerts against current data
            if st.button("🔄 Check Alerts"):
                for alert in st.session_state.alerts:
                    try:
                        t = yf.Ticker(alert['ticker'])
                        hist = t.history(period="1d")
                        if not hist.empty:
                            current = hist['Close'].iloc[-1]
                            triggered = (current >= alert['price'] if alert['type'] == 'Above'
                                        else current <= alert['price'])
                            if triggered:
                                st.error(f"🚨 **ALERT TRIGGERED:** {alert['ticker']} is {alert['type']} ₹{alert['price']} "
                                        f"(Current: ₹{current:.2f})")
                            else:
                                st.info(f"⏳ {alert['ticker']}: ₹{current:.2f} (target: {alert['type']} ₹{alert['price']})")
                    except Exception as e:
                        st.warning(f"Could not check {alert['ticker']}: {e}")
            
            if st.button("🗑️ Clear All Alerts"):
                st.session_state.alerts = []
                st.rerun()


# ==============================================================================
# FOOTER
# ==============================================================================
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style="font-size:0.7rem;color:#484f58;text-align:center;padding:12px">
    ⚠️ For educational purposes only.<br>
    Not financial advice. Consult a SEBI-registered advisor.<br>
    <br>
    Built with 🐍 Python + 📊 Plotly + 🚀 Streamlit
</div>
""", unsafe_allow_html=True)
