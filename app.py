import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from scipy import stats
from scipy.optimize import minimize
from itertools import combinations
import datetime
import calendar
import math
import requests
import warnings

warnings.filterwarnings('ignore')

# ==============================================================================
# CONFIGURATION & UNIVERSE
# ==============================================================================
st.set_page_config(page_title="NSE Market Intelligence Terminal", layout="wide", page_icon="📈")

# Using the Top ~200 Nifty options universe to prevent Streamlit Cloud timeout/memory limits
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


@st.cache_data(ttl=3600)
def fetch_data(tickers, period, interval="1d"):
    return yf.download(tickers, period=period, interval=interval, progress=False, auto_adjust=True)


# ==============================================================================
# SHARED BLACK-SCHOLES HELPERS (used by both the classic screener and the
# full Option Chain & Greeks module below)
# ==============================================================================
def _norm_cdf(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0


def _norm_pdf(x):
    return math.exp(-0.5 * x * x) / math.sqrt(2.0 * math.pi)


def calc_greeks(S, K, T_days, sigma_pct, opt_type='CE', r=0.065):
    """Black-Scholes greeks + theoretical price / intrinsic / time value / moneyness."""
    T = max(T_days, 1) / 365.0
    sigma = max(sigma_pct, 0.01) / 100.0
    if S <= 0 or K <= 0:
        return dict(delta=0, gamma=0, theta=0, vega=0, rho=0, theo_price=0,
                     intrinsic=0, time_value=0, moneyness='—')
    try:
        d1 = (math.log(S / K) + (r + 0.5 * sigma ** 2) * T) / (sigma * math.sqrt(T))
        d2 = d1 - sigma * math.sqrt(T)
        nd1 = _norm_cdf(d1)
        nd2 = _norm_cdf(d2)
        nnd1 = _norm_cdf(-d1)
        nnd2 = _norm_cdf(-d2)
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


def analyse_oc(df, sp, rf, points):
    """
    Full option-chain analytics: OI walls (primary + secondary), PCR, weighted IV,
    IV skew, volume ratio, max pain, ITM/exit signals.
    Ported from the standalone Colab option-chain analyzer for feature parity.
    """
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

        # secondary OI walls (next-largest concentrations away from the primary wall)
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
            vr=vr, ce_wiv=ce_wiv, pe_wiv=pe_wiv,
            max_pain=max_pain,
        )
    except Exception:
        return None


def calc_suggestion(m, points):
    """
    7-factor scoring engine (PCR, OI sentiment, max pain, IV skew, volume ratio,
    OI-unwinding, ATM OI ratio). Ported from the Colab notebook — a strict
    superset of the 3-factor version previously in this app.
    Positive score → Bullish (Buy CE). Negative score → Bearish (Buy PE).
    """
    score = 0
    reasons = []  # (sentiment_label, explanation)

    # 1. Put-Call Ratio
    pcr = m['pcr']
    if pcr >= 1.3:
        score += 3
        reasons.append(('BULLISH', f'PCR {pcr} ≥ 1.3 — heavy put writing signals floor support'))
    elif pcr >= 1.1:
        score += 2
        reasons.append(('BULLISH', f'PCR {pcr} ∈ [1.1,1.3) — put OI dominance, mild bullish tilt'))
    elif pcr >= 0.9:
        reasons.append(('NEUTRAL', f'PCR {pcr} ∈ [0.9,1.1) — balanced OI, no strong directional signal'))
    elif pcr >= 0.7:
        score -= 2
        reasons.append(('BEARISH', f'PCR {pcr} ∈ [0.7,0.9) — call OI dominance, mild bearish tilt'))
    else:
        score -= 3
        reasons.append(('BEARISH', f'PCR {pcr} < 0.7 — aggressive call writing, strong ceiling resistance'))

    # 2. OI sentiment
    if m['sentiment'] == 'Bullish':
        score += 2
        reasons.append(('BULLISH', f'OI Diff {m["diff"]:+.1f} — PE writers outnumber CE writers (bullish pressure)'))
    else:
        score -= 2
        reasons.append(('BEARISH', f'OI Diff {m["diff"]:+.1f} — CE writers dominant (bearish pressure)'))

    # 3. Max pain
    pain_diff = m['max_pain'] - points
    if abs(pain_diff) < 50:
        reasons.append(('NEUTRAL', f'Price ≈ Max Pain ({int(m["max_pain"])}) — expiry magnet near; avoid directional bets'))
    elif pain_diff > 200:
        score += 2
        reasons.append(('BULLISH', f'Max Pain {int(m["max_pain"])} is {pain_diff:+.0f} pts above CMP — strong upward gravity'))
    elif pain_diff > 0:
        score += 1
        reasons.append(('BULLISH', f'Max Pain {int(m["max_pain"])} is {pain_diff:+.0f} pts above CMP — mild upward pull'))
    elif pain_diff < -200:
        score -= 2
        reasons.append(('BEARISH', f'Max Pain {int(m["max_pain"])} is {pain_diff:+.0f} pts below CMP — strong downward gravity'))
    else:
        score -= 1
        reasons.append(('BEARISH', f'Max Pain {int(m["max_pain"])} is {pain_diff:+.0f} pts below CMP — mild downward pull'))

    # 4. IV skew
    sk = m['iv_skew']
    if sk > 4:
        score -= 3
        reasons.append(('BEARISH', f'IV Skew +{sk}% — extreme put premium; market pricing fear/tail-risk event'))
    elif sk > 2:
        score -= 2
        reasons.append(('BEARISH', f'IV Skew +{sk}% — elevated put premium; protective buying active'))
    elif sk > 0.5:
        score -= 1
        reasons.append(('MILD BEAR', f'IV Skew +{sk}% — slight put IV bias'))
    elif sk < -4:
        score += 3
        reasons.append(('BULLISH', f'IV Skew {sk}% — extreme call premium; speculation/breakout demand'))
    elif sk < -2:
        score += 2
        reasons.append(('BULLISH', f'IV Skew {sk}% — elevated call premium; bullish demand spike'))
    elif sk < -0.5:
        score += 1
        reasons.append(('MILD BULL', f'IV Skew {sk}% — slight call IV bias'))
    else:
        reasons.append(('NEUTRAL', f'IV Skew {sk}% — near-zero; CE/PE fairly priced'))

    # 5. Volume ratio
    vr = m['vr']
    if vr > 1.5:
        score += 2
        reasons.append(('BULLISH', f'Vol Ratio {vr} — strong PE volume: put buyers chasing protection or contrarians buying calls'))
    elif vr > 1.2:
        score += 1
        reasons.append(('BULLISH', f'Vol Ratio {vr} — PE volume slightly dominant'))
    elif vr < 0.6:
        score -= 2
        reasons.append(('BEARISH', f'Vol Ratio {vr} — heavy CE volume: call buyers aggressive or hedgers buying puts'))
    elif vr < 0.8:
        score -= 1
        reasons.append(('BEARISH', f'Vol Ratio {vr} — CE volume slightly dominant'))
    else:
        reasons.append(('NEUTRAL', f'Vol Ratio {vr} — CE/PE volume balanced'))

    # 6. OI unwinding
    if m['ce_exits'] == 'Yes' and m['pe_exits'] == 'Yes':
        reasons.append(('CAUTION', 'Both CE & PE OI unwinding — theta decay or position squaring; avoid new entries'))
    elif m['ce_exits'] == 'Yes':
        score += 1
        reasons.append(('MILD BULL', 'CE OI unwinding — call shorts covering; reduces resistance'))
    elif m['pe_exits'] == 'Yes':
        score -= 1
        reasons.append(('MILD BEAR', 'PE OI unwinding — put shorts covering; reduces support'))

    # 7. ATM CE vs PE OI ratio
    ce_atm = m['cs']
    pe_atm = m['ps']
    ratio = pe_atm / max(ce_atm, 0.01)
    if ratio > 1.5:
        score += 1
        reasons.append(('BULLISH', f'ATM PE OI ({pe_atm}) >> CE OI ({ce_atm}) — heavy put selling = support level'))
    elif ratio < 0.67:
        score -= 1
        reasons.append(('BEARISH', f'ATM CE OI ({ce_atm}) >> PE OI ({pe_atm}) — heavy call selling = resistance level'))

    if score >= 7:
        action, confidence, conf_pct = 'STRONG BUY CE 🚀', 'Very High', 90
    elif score >= 4:
        action, confidence, conf_pct = 'BUY CE 📈', 'High', 75
    elif score >= 2:
        action, confidence, conf_pct = 'MILD CE BIAS ↗', 'Moderate', 60
    elif score >= 1:
        action, confidence, conf_pct = 'SLIGHT CE LEAN ↗', 'Low', 52
    elif score <= -7:
        action, confidence, conf_pct = 'STRONG BUY PE 🔻', 'Very High', 90
    elif score <= -4:
        action, confidence, conf_pct = 'BUY PE 📉', 'High', 75
    elif score <= -2:
        action, confidence, conf_pct = 'MILD PE BIAS ↘', 'Moderate', 60
    elif score <= -1:
        action, confidence, conf_pct = 'SLIGHT PE LEAN ↘', 'Low', 52
    else:
        action, confidence, conf_pct = 'NEUTRAL / WAIT ⏸', 'Low', 50

    return dict(action=action, score=score, confidence=confidence, conf_pct=conf_pct, reasons=reasons)


# ==============================================================================
# NSE DATA LAYER — session/cookie handling with automatic retry on 401
# ==============================================================================
def get_nse_headers():
    return {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36',
        'accept-language': 'en,gu;q=0.9,hi;q=0.8',
        'accept-encoding': 'gzip, deflate',
    }


def get_nse_session():
    """One warm session per Streamlit session, reused across reruns/fetches."""
    if 'nse_session' not in st.session_state:
        st.session_state.nse_session = requests.Session()
        try:
            st.session_state.nse_session.get(
                'https://www.nseindia.com/option-chain', headers=get_nse_headers(), timeout=8
            )
        except Exception:
            pass
    return st.session_state.nse_session


def nse_get(url, retry=True):
    """GET with automatic cookie-refresh retry on 401/blocked responses."""
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
    """Fetch + reshape the option chain into the CE/Strike/PE merged frame."""
    t_str = 'Indices' if mode == 'Index' else 'Equity'
    url = f'https://www.nseindia.com/api/option-chain-v3?type={t_str}&symbol={symbol}&expiry={expiry}'
    r = nse_get(url)
    if r is None or r.status_code != 200:
        return None, None, None, f"HTTP {r.status_code if r is not None else 'no response'} from NSE."

    try:
        jd = r.json()
    except Exception:
        return None, None, None, "NSE response was not valid JSON (likely blocked/rate-limited)."

    ce_vals = [d['CE'] for d in jd.get('records', {}).get('data', [])
               if 'CE' in d and d.get('expiryDate', '').lower() == expiry.lower()]
    pe_vals = [d['PE'] for d in jd.get('records', {}).get('data', [])
               if 'PE' in d and d.get('expiryDate', '').lower() == expiry.lower()]

    if not ce_vals or not pe_vals:
        return None, None, None, "Empty chain retrieved for this expiry."

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


# ==============================================================================
# APP NAVIGATION
# ==============================================================================
st.sidebar.title("Navigation")
app_mode = st.sidebar.radio("Select Tool", [
    "Market Movers",
    "Sectoral Analysis",
    "Seasonality Analysis",
    "SMA Crossover Screener",
    "Portfolio Optimizer",
    "Correlation Scanner",
    "Probability & Timeframes",
    "Option Chain & Greeks",
    "IPO Dashboard"
])

st.sidebar.info("Data is cached for 1 hour to prevent API throttling.")

# ==============================================================================
# 1. MARKET MOVERS
# ==============================================================================
if app_mode == "Market Movers":
    st.title("Top Winners & Losers (1D / 1W / 1M)")
    st.write("Analyzes the core universe of ~200 NSE Options Equities.")

    with st.spinner("Fetching market data..."):
        data = fetch_data(TICKER_LIST, "2mo")

    if not data.empty and 'Close' in data.columns:
        close_prices = data['Close'].ffill().bfill()

        results = []
        for ticker in TICKER_LIST:
            if ticker in close_prices.columns:
                s = close_prices[ticker].dropna()
                if len(s) >= 22:
                    current = s.iloc[-1]
                    p_1d = s.iloc[-2]
                    p_1w = s.iloc[-6]
                    p_1m = s.iloc[-22]

                    results.append({
                        "Ticker": ticker,
                        "LTP": round(current, 2),
                        "1D Change (%)": round(((current - p_1d) / p_1d) * 100, 2),
                        "1W Change (%)": round(((current - p_1w) / p_1w) * 100, 2),
                        "1M Change (%)": round(((current - p_1m) / p_1m) * 100, 2)
                    })

        df = pd.DataFrame(results)

        c1, c2, c3 = st.columns(3)
        with c1:
            st.subheader("🚀 1-Day Performers")
            st.dataframe(df.nlargest(10, "1D Change (%)")[['Ticker', 'LTP', '1D Change (%)']].style.background_gradient(cmap="Greens"))
            st.dataframe(df.nsmallest(10, "1D Change (%)")[['Ticker', 'LTP', '1D Change (%)']].style.background_gradient(cmap="Reds_r"))

        with c2:
            st.subheader("🚀 1-Week Performers")
            st.dataframe(df.nlargest(10, "1W Change (%)")[['Ticker', 'LTP', '1W Change (%)']].style.background_gradient(cmap="Greens"))
            st.dataframe(df.nsmallest(10, "1W Change (%)")[['Ticker', 'LTP', '1W Change (%)']].style.background_gradient(cmap="Reds_r"))

        with c3:
            st.subheader("🚀 1-Month Performers")
            st.dataframe(df.nlargest(10, "1M Change (%)")[['Ticker', 'LTP', '1M Change (%)']].style.background_gradient(cmap="Greens"))
            st.dataframe(df.nsmallest(10, "1M Change (%)")[['Ticker', 'LTP', '1M Change (%)']].style.background_gradient(cmap="Reds_r"))

# ==============================================================================
# 2. SECTORAL ANALYSIS
# ==============================================================================
elif app_mode == "Sectoral Analysis":
    st.title("NSE Sectoral Performance Analysis")
    st.write("Aggregates market returns by sector to visualize capital rotation.")

    with st.spinner("Fetching market data..."):
        raw = fetch_data(TICKER_LIST, "2mo")

    if not raw.empty and 'Close' in raw.columns:
        close = raw['Close'].ffill().bfill()

        def safe_ret(series, n):
            c = series.dropna()
            if len(c) < n + 1:
                return np.nan
            return round(((c.iloc[-1] / c.iloc[-1 - n]) - 1) * 100, 2)

        records = []
        for t in close.columns:
            s = close[t]
            if len(s.dropna()) >= 22:
                records.append({
                    "Ticker": t,
                    "Sector": SECTOR_MAP.get(t, "Others"),
                    "1D %": safe_ret(s, 1),
                    "1W %": safe_ret(s, 5),
                    "1M %": safe_ret(s, 21),
                })

        df = pd.DataFrame(records).dropna()

        if not df.empty:
            sector_agg = (
                df.groupby("Sector")[["1D %", "1W %", "1M %"]]
                .mean().round(2).reset_index()
            )
            sector_agg["Count"] = df.groupby("Sector")["Ticker"].count().values
            sector_agg = sector_agg.sort_values("1M %", ascending=False).reset_index(drop=True)

            tab1, tab2, tab3 = st.tabs(["🔥 Heatmap", "📊 Bar Charts", "🌳 Treemap"])

            with tab1:
                heat_data = sector_agg.set_index("Sector")[["1D %", "1W %", "1M %"]]
                fig1 = px.imshow(heat_data, text_auto=True, color_continuous_scale="RdYlGn", color_continuous_midpoint=0, aspect="auto", title="Sector Performance Heatmap")
                st.plotly_chart(fig1, use_container_width=True)

            with tab2:
                fig2 = make_subplots(rows=1, cols=3, subplot_titles=("Avg 1D %", "Avg 1W %", "Avg 1M %"))

                for i, col in enumerate(["1D %", "1W %", "1M %"]):
                    data = sector_agg.sort_values(col)
                    colors = ['#00c48c' if x >= 0 else '#ff4d6d' for x in data[col]]
                    fig2.add_trace(go.Bar(x=data[col], y=data["Sector"], orientation='h', marker_color=colors, name=col), row=1, col=i+1)

                fig2.update_layout(height=600, showlegend=False, title_text="Sector Returns")
                st.plotly_chart(fig2, use_container_width=True)

            with tab3:
                df["Size"] = df["1M %"].abs().clip(lower=0.1)
                fig3 = px.treemap(df, path=['Sector', 'Ticker'], values='Size', color='1M %',
                                  color_continuous_scale='RdYlGn', color_continuous_midpoint=0,
                                  title="Market Treemap (Size = |1M Return|, Color = Return %)")
                st.plotly_chart(fig3, use_container_width=True)

# ==============================================================================
# 3. SEASONALITY ANALYSIS
# ==============================================================================
elif app_mode == "Seasonality Analysis":
    st.title("Monthly Seasonality Analysis")

    col1, col2 = st.columns([1, 3])
    with col1:
        months = list(calendar.month_name)[1:]
        current_month_idx = datetime.datetime.now().month
        target_month_name = st.selectbox("Select Target Month", options=months, index=(current_month_idx % 12))
        target_month = list(calendar.month_name).index(target_month_name)
        years_history = st.slider("Years of History", 5, 15, 10)
        min_years = st.slider("Min Years Traded", 3, 10, 5)
        run_seasonality = st.button("Run Analysis", type="primary")

    if run_seasonality:
        with st.spinner(f"Fetching {years_history} years of monthly data..."):
            raw = fetch_data(TICKER_LIST, f"{years_history}y", interval="1mo")
            daily_raw = fetch_data(TICKER_LIST, "5d", interval="1d")

        if not raw.empty and 'Close' in raw.columns:
            close = raw["Close"]
            daily_close = daily_raw["Close"]
            returns = close.pct_change() * 100

            ltp_map = {}
            for t in daily_close.columns:
                s = daily_close[t].dropna()
                ltp_map[t] = round(s.iloc[-1], 2) if len(s) > 0 else np.nan

            records = []
            for ticker in close.columns:
                monthly = returns[ticker][returns.index.month == target_month].dropna()
                if len(monthly) >= min_years:
                    avg = monthly.mean()
                    std = monthly.std()
                    win_rate = (monthly > 0).mean() * 100
                    sharpe = avg / std if std > 0 else np.nan

                    records.append({
                        "Ticker": ticker.replace(".NS", ""),
                        "LTP": ltp_map.get(ticker, np.nan),
                        "Win Rate (%)": round(win_rate, 1),
                        "Avg Return (%)": round(avg, 2),
                        "Std Dev (%)": round(std, 2),
                        "Sharpe Ratio": round(sharpe, 3) if not np.isnan(sharpe) else np.nan,
                        "Years": len(monthly)
                    })

            df = pd.DataFrame(records).dropna(subset=["Sharpe Ratio"]).sort_values("Sharpe Ratio", ascending=False).reset_index(drop=True)
            df.index += 1

            st.subheader(f"Top Seasonality Performers for {target_month_name.upper()}")
            st.dataframe(df.head(25).style.background_gradient(subset=["Sharpe Ratio"], cmap="Blues"))

            top = df.head(15)
            fig = make_subplots(rows=1, cols=2, subplot_titles=(f"Avg Return — {target_month_name}", f"Win Rate — {target_month_name}"))

            colors = ["#00C853" if v > 0 else "#D50000" for v in top["Avg Return (%)"]]
            fig.add_trace(go.Bar(x=top["Ticker"], y=top["Avg Return (%)"], marker_color=colors, name="Avg Return"), row=1, col=1)

            wr_colors = [f"rgba({int(255*(1-w/100))},{int(200*w/100)},0,0.85)" for w in top["Win Rate (%)"]]
            fig.add_trace(go.Bar(x=top["Ticker"], y=top["Win Rate (%)"], marker_color=wr_colors, name="Win Rate"), row=1, col=2)

            fig.add_hline(y=50, line_dash="dash", line_color="#888", row=1, col=2)
            fig.update_layout(height=500, showlegend=False, template="plotly_white")
            st.plotly_chart(fig, use_container_width=True)

# ==============================================================================
# 4. SMA CROSSOVER SCREENER
# ==============================================================================
elif app_mode == "SMA Crossover Screener":
    st.title("50/200 SMA Crossover Screener")
    st.write("Scans for Golden Cross (Bullish) and Death Cross (Bearish) signals.")

    if st.button("Run Screener", type="primary"):
        with st.spinner("Fetching 2 years of daily data for SMA calculations..."):
            raw = fetch_data(TICKER_LIST, "2y", "1d")

        if not raw.empty and 'Close' in raw.columns:
            close_df = raw['Close']
            results = []

            for ticker in close_df.columns:
                s = close_df[ticker].dropna()
                if len(s) < 200:
                    continue

                sma50 = s.rolling(window=50).mean()
                sma200 = s.rolling(window=200).mean()

                valid_data = pd.DataFrame({'Close': s, 'SMA_50': sma50, 'SMA_200': sma200}).dropna()
                if valid_data.empty:
                    continue

                last_close = valid_data['Close'].iloc[-1]
                last_sma50 = valid_data['SMA_50'].iloc[-1]
                last_sma200 = valid_data['SMA_200'].iloc[-1]
                diff_pct = ((last_sma50 - last_sma200) / last_sma200) * 100

                bullish = valid_data['SMA_50'] > valid_data['SMA_200']
                cross_points = bullish.ne(bullish.shift())
                cross_points.iloc[0] = False
                cross_dates = valid_data.index[cross_points]

                days_since_cross = None
                if len(cross_dates) > 0:
                    last_cross_date = cross_dates[-1]
                    days_since_cross = len(valid_data) - 1 - valid_data.index.get_loc(last_cross_date)

                status = "No Cross Proximity"
                signal = "Neutral"

                if days_since_cross is not None:
                    if days_since_cross <= 3:
                        status = "At Cross"
                        signal = "Bullish" if last_sma50 > last_sma200 else "Bearish"
                    elif 3 < days_since_cross <= 20:
                        status = "Post Bullish Cross" if last_sma50 > last_sma200 else "Post Bearish Cross"
                        signal = "Bullish" if last_sma50 > last_sma200 else "Bearish"

                if status == "No Cross Proximity" and abs(diff_pct) <= 2.0:
                    if last_sma50 < last_sma200:
                        status = "Approaching Bullish Cross"
                        signal = "Bullish"
                    elif last_sma50 > last_sma200:
                        status = "Approaching Bearish Cross"
                        signal = "Bearish"

                if status != "No Cross Proximity":
                    results.append({
                        "Ticker": ticker,
                        "Last_Close": round(last_close, 2),
                        "SMA_50": round(last_sma50, 2),
                        "SMA_200": round(last_sma200, 2),
                        "Diff_%": round(diff_pct, 2),
                        "Cross_Status": status,
                        "Signal_Type": signal
                    })

            if results:
                df_results = pd.DataFrame(results).sort_values(['Signal_Type', 'Diff_%'])
                st.success(f"Found {len(df_results)} actionable signals!")

                def color_signal(val):
                    color = 'green' if val == 'Bullish' else 'red' if val == 'Bearish' else 'black'
                    return f'color: {color}; font-weight: bold'

                st.dataframe(df_results.style.map(color_signal, subset=['Signal_Type']))
            else:
                st.info("No actionable crossover signals found today.")

# ==============================================================================
# 5. PORTFOLIO OPTIMIZER
# ==============================================================================
elif app_mode == "Portfolio Optimizer":
    st.title("Roy's Safety-First Portfolio Optimizer")

    col1, col2 = st.columns([1, 3])
    with col1:
        inv_amt = st.number_input("Investment Amount (₹)", min_value=10000, value=100000, step=10000)
        port_size = st.slider("Stocks per Portfolio", 3, 15, 10)
        threshold_ret = st.slider("Min Acceptable Return (%)", 1.0, 15.0, 6.0) / 100
        run_opt = st.button("Optimize Portfolio", type="primary")

    if run_opt:
        with st.spinner("Fetching 2 years of data & optimizing... (This may take a minute)"):
            raw = fetch_data(TICKER_LIST + ["^NSEI"], "2y")

        if not raw.empty and 'Close' in raw.columns:
            cleaned = raw['Close'].dropna(thresh=int(len(raw)*0.8), axis=1).ffill().bfill()
            benchmark = cleaned.pop("^NSEI") if "^NSEI" in cleaned.columns else None

            daily_ret = cleaned.pct_change().dropna()
            TRADING_DAYS = 252
            RISK_FREE_RATE = 0.065

            p_1y_ago = cleaned.iloc[-TRADING_DAYS] if len(cleaned) >= TRADING_DAYS else cleaned.iloc[0]
            p_today = cleaned.iloc[-1]
            actual_ret = (p_today - p_1y_ago) / p_1y_ago

            exp_ret = daily_ret.mean() * TRADING_DAYS
            ann_vol = daily_ret.std() * np.sqrt(TRADING_DAYS)
            sharpe = (exp_ret - RISK_FREE_RATE) / ann_vol

            def _mdd(series):
                peak = series.cummax()
                return ((series - peak) / peak).min()

            mdd = cleaned.apply(_mdd)

            score = (0.3 * exp_ret.rank(pct=True) + 0.2 * actual_ret.rank(pct=True) +
                     0.3 * sharpe.rank(pct=True) + 0.2 * (-mdd).rank(pct=True))

            hard_pass = (actual_ret > 0) & (exp_ret >= threshold_ret)
            elite = score[hard_pass].nlargest(20).index.tolist()

            if len(elite) < port_size:
                st.error("Not enough stocks passed the filter. Try lowering the threshold.")
            else:
                cov_mat = (daily_ret[elite].cov() * TRADING_DAYS).values
                exp_arr = exp_ret[elite].values
                n = len(elite)

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
                    return -(p_ret - RISK_FREE_RATE) / p_vol

                cons = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
                bounds = tuple((0.05, 0.25) for _ in range(port_size))
                init_guess = np.array([1/port_size] * port_size)

                opt_result = minimize(objective, init_guess, method='SLSQP', bounds=bounds, constraints=cons)

                opt_weights = opt_result.x
                opt_ret = np.sum(port_mu * opt_weights)
                opt_vol = np.sqrt(np.dot(opt_weights.T, np.dot(port_cov, opt_weights)))
                opt_sharpe = (opt_ret - RISK_FREE_RATE) / opt_vol

                st.success(f"Optimization Complete! Max Sharpe: {opt_sharpe:.3f}")

                c1, c2 = st.columns(2)
                with c1:
                    st.write("### Optimal Allocations")
                    alloc_df = pd.DataFrame({
                        "Ticker": [t.replace('.NS', '') for t in top_tickers],
                        "Weight (%)": opt_weights * 100,
                        "Amount (₹)": opt_weights * inv_amt
                    })
                    st.dataframe(alloc_df.style.format({"Weight (%)": "{:.1f}%", "Amount (₹)": "₹{:,.0f}"}))

                with c2:
                    fig = px.pie(alloc_df, values='Weight (%)', names='Ticker', hole=0.4, title="Capital Allocation")
                    st.plotly_chart(fig, use_container_width=True)

                st.write("### 2-Year Historical Backtest")
                port_hist_returns = (daily_ret[top_tickers] * opt_weights).sum(axis=1)
                port_cum_returns = (1 + port_hist_returns).cumprod()

                fig2 = go.Figure()
                fig2.add_trace(go.Scatter(x=port_cum_returns.index, y=port_cum_returns.values, name="Optimized Portfolio"))

                if benchmark is not None:
                    bm_ret = benchmark.pct_change().dropna()
                    bm_cum = (1 + bm_ret).cumprod()
                    bm_cum = bm_cum.reindex(port_cum_returns.index).ffill()
                    fig2.add_trace(go.Scatter(x=bm_cum.index, y=bm_cum.values, name="Nifty 50", line=dict(dash='dash', color='gray')))

                fig2.update_layout(yaxis_title="Cumulative Growth (1.0 = Initial)", template="plotly_white")
                st.plotly_chart(fig2, use_container_width=True)

# ==============================================================================
# 6. CORRELATION SCANNER
# ==============================================================================
elif app_mode == "Correlation Scanner":
    st.title("Inverse & Pair Trading Correlation Scanner")
    st.write("Finds the most negatively correlated pairs or specific hedges for your target stock.")

    target_ticker = st.text_input("Target Ticker (e.g., ITC.NS or leave blank for full matrix)", "")
    if st.button("Calculate Correlation"):
        with st.spinner("Fetching 1-year data..."):
            raw = fetch_data(TICKER_LIST, "1y")

        if not raw.empty and 'Close' in raw.columns:
            returns = raw['Close'].pct_change().dropna()

            returns = returns.loc[:, returns.isna().sum() < len(returns) * 0.05].ffill().bfill()
            corr_matrix = returns.corr()

            if target_ticker and target_ticker.upper() in corr_matrix.columns:
                target = target_ticker.upper()
                st.subheader(f"Top Inverse Correlations for {target}")

                target_corr = corr_matrix[target].sort_values(ascending=True)
                target_corr = target_corr.drop(labels=[target], errors='ignore')

                top_inv = target_corr.head(10).reset_index()
                top_inv.columns = ['Ticker', 'Correlation']
                st.dataframe(top_inv.style.background_gradient(cmap="Reds_r"))
            else:
                st.subheader("Top 15 Most Negatively Correlated Pairs in Universe")
                mask = np.tril(np.ones_like(corr_matrix, dtype=bool), k=-1)
                tri_corr = corr_matrix.where(mask)
                pairs = tri_corr.stack().reset_index()
                pairs.columns = ["Ticker 1", "Ticker 2", "Correlation"]
                pairs = pairs.sort_values("Correlation").reset_index(drop=True)

                st.dataframe(pairs.head(15).style.background_gradient(subset=['Correlation'], cmap="Reds_r"))

# ==============================================================================
# 7. PROBABILITY & TIMEFRAMES
# ==============================================================================
elif app_mode == "Probability & Timeframes":
    st.title("Probability & Multi-Timeframe Volatility Dashboard")

    ticker = st.text_input("Enter Ticker Symbol", "RELIANCE.NS").strip().upper()
    if st.button("Analyze Timeframes", type="primary") and ticker:
        with st.spinner(f"Analyzing {ticker}..."):
            stock = yf.Ticker(ticker)
            df = stock.history(period="5y")

        if not df.empty and len(df) > 30:
            df = df.dropna(subset=['Close'])
            ltp = df['Close'].iloc[-1]
            st.write(f"### Current Price (LTP): ₹{ltp:,.2f}")

            df_daily = df.copy()
            df_daily['Return'] = df_daily['Close'].pct_change()
            df_daily = df_daily.dropna(subset=['Return'])
            df_daily['Direction'] = df_daily['Return'].apply(lambda x: 'Up' if x > 0 else ('Down' if x < 0 else 'Flat'))
            df_daily['Prev_Direction'] = df_daily['Direction'].shift(1)

            last_dir = df_daily['Direction'].iloc[-1]
            last_date = df_daily.index[-1].strftime('%Y-%m-%d')

            sim_setups = df_daily[df_daily['Prev_Direction'] == last_dir]
            tot_sim = len(sim_setups)

            if tot_sim > 0:
                up_prob = (len(sim_setups[sim_setups['Direction'] == 'Up']) / tot_sim) * 100
                dn_prob = (len(sim_setups[sim_setups['Direction'] == 'Down']) / tot_sim) * 100

                st.info(f"Yesterday ({last_date}) was an **{last_dir}** day. Historically, after an {last_dir} day:")
                col1, col2 = st.columns(2)
                col1.metric("Probability of UP Day Today", f"{up_prob:.1f}%")
                col2.metric("Probability of DOWN Day Today", f"{dn_prob:.1f}%")

            st.write("---")
            st.subheader("Multi-Timeframe Expected Ranges")

            def analyze_timeframe(data_frame, windows, period_label, current_p):
                temp_df = data_frame.copy()
                temp_df['Return'] = temp_df['Close'].pct_change() * 100
                temp_df['Up_Move'] = temp_df['Return'].apply(lambda x: x if x > 0 else np.nan)
                temp_df['Down_Move'] = temp_df['Return'].apply(lambda x: abs(x) if x < 0 else np.nan)
                temp_df['Swing_Pct'] = ((temp_df['High'] - temp_df['Low']) / temp_df['Low']) * 100

                results = []
                for w in windows:
                    if len(temp_df) >= w:
                        df_window = temp_df.tail(w)
                        avg_swing = df_window['Swing_Pct'].mean()
                        avg_up = df_window['Up_Move'].mean()
                        avg_dn = df_window['Down_Move'].mean()

                        p_low = current_p - ((avg_dn / 100) * current_p)
                        p_high = current_p + ((avg_up / 100) * current_p)

                        results.append({
                            "Window": f"Last {w} {period_label}s",
                            "Avg Swing Volatility": f"{avg_swing:.2f}%",
                            "Avg Up Move": f"{avg_up:.2f}%",
                            "Avg Down Move": f"{avg_dn:.2f}%",
                            "Projected Low (₹)": round(p_low, 2),
                            "Projected High (₹)": round(p_high, 2)
                        })
                return pd.DataFrame(results).set_index("Window") if results else None

            df_weekly = df.resample('W-FRI').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'}).dropna()
            df_monthly = df.resample('ME').agg({'Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last'}).dropna()

            t1, t2, t3 = st.tabs(["Daily Range", "Weekly Range", "Monthly Range"])
            with t1:
                res_d = analyze_timeframe(df, [30, 60, 150, 300], "Day", ltp)
                if res_d is not None:
                    st.dataframe(res_d, use_container_width=True)
            with t2:
                res_w = analyze_timeframe(df_weekly, [12, 26, 52, 104], "Week", ltp)
                if res_w is not None:
                    st.dataframe(res_w, use_container_width=True)
            with t3:
                res_m = analyze_timeframe(df_monthly, [3, 6, 12, 24], "Month", ltp)
                if res_m is not None:
                    st.dataframe(res_m, use_container_width=True)

# ==============================================================================
# 8. OPTION CHAIN & GREEKS  (fully merged with the standalone analyzer engine)
# ==============================================================================
elif app_mode == "Option Chain & Greeks":
    st.title("NSE Option Chain, Greeks & Smart Suggestion")
    st.markdown(
        "Live Option Chain data fetched directly from NSE India — now with the full analytics "
        "engine: primary/secondary OI walls, weighted IV, max pain, IV skew, volume ratio, "
        "OI-unwinding detection, Black-Scholes Greeks, and a 7-factor Smart Suggestion score. "
        "*(Note: works best when run locally — Streamlit Cloud IPs are occasionally rate-limited by NSE.)*"
    )

    c1, c2, c3 = st.columns(3)
    mode = c1.selectbox("Mode", ["Index", "Stock"])
    idx_list, stk_list = fetch_nse_symbols()
    symbol = c2.selectbox("Symbol", idx_list if mode == "Index" else stk_list)

    expiries = fetch_nse_expiries(symbol)
    if not expiries:
        st.warning(
            "⚠️ Could not load expiry dates from NSE. The API might be rate-limiting or blocking "
            "cloud IPs. Try again in a minute, or run this app locally for reliable access."
        )
    else:
        expiry = c3.selectbox("Expiry Date", expiries)

        colf1, colf2 = st.columns([1, 3])
        with colf1:
            fetch_clicked = st.button("Fetch Option Chain", type="primary")
        with colf2:
            auto_atm = st.checkbox("Auto-select ATM strike after fetch", value=True)

        # Persist the fetched chain in session_state so tab switches / widget
        # interactions don't force a fresh network round-trip every rerun.
        state_key = f"oc_{mode}_{symbol}_{expiry}"

        if fetch_clicked:
            with st.spinner(f"Fetching Option Chain for {symbol} ({expiry})..."):
                merged, ts, points, err = fetch_option_chain_raw(symbol, expiry, mode)
            if err:
                st.error(f"Failed to fetch data from NSE: {err}")
                st.session_state.pop(state_key, None)
            else:
                st.session_state[state_key] = {"df": merged, "ts": ts, "points": points}

        cached = st.session_state.get(state_key)

        if cached is None:
            st.info("Click **Fetch Option Chain** to load live data.")
        else:
            merged = cached["df"]
            ts = cached["ts"]
            points = cached["points"]

            strikes = merged['Strike Price'].tolist()
            atm_sp = min(strikes, key=lambda x: abs(x - points))
            rf = 1000 if mode == 'Index' else 10

            st.write(f"### Underlying: **{symbol} @ ₹{points:,.2f}**  ·  Last update: `{ts}`")

            sel_key = f"sp_select_{state_key}"
            default_sp = st.session_state.get(sel_key, atm_sp) if not auto_atm else atm_sp
            if default_sp not in strikes:
                default_sp = atm_sp
            sp = st.selectbox(
                "Analysis Strike (defaults to ATM)",
                options=sorted(strikes),
                index=sorted(strikes).index(default_sp),
                key=sel_key,
            )

            m = analyse_oc(merged, sp, rf, points)

            tab1, tab2, tab3, tab4, tab5 = st.tabs([
                "💡 Summary & Smart Suggestion", "📐 Greeks (Selected Strike)",
                "📈 Charts", "📊 History", "📄 Full Option Chain"
            ])

            # ---------------- TAB 1: Summary & Smart Suggestion ----------------
            with tab1:
                if m is None:
                    st.warning("Could not compute advanced metrics for this chain/strike.")
                else:
                    sug = calc_suggestion(m, points)

                    mc1, mc2, mc3, mc4, mc5 = st.columns(5)
                    mc1.metric("PCR", m['pcr'])
                    mc2.metric("Max Pain", int(m['max_pain']), delta=f"{int(m['max_pain'] - points)} pts")
                    mc3.metric("ATM CE IV", f"{m['ce_iv']}%", delta=f"Wtd {m['ce_wiv']}%")
                    mc4.metric("ATM PE IV", f"{m['pe_iv']}%", delta=f"Wtd {m['pe_wiv']}%")
                    mc5.metric("IV Skew (PE−CE)", f"{m['iv_skew']:+.2f}%")

                    st.write("---")
                    st.subheader(f"Smart Verdict: {sug['action']}")
                    st.write(f"**Directional Score:** {sug['score']:+d} / ±10  ·  **Confidence:** {sug['confidence']} ({sug['conf_pct']}%)")

                    score_bar_pct = max(2, min(98, int((sug['score'] + 10) / 20 * 100)))
                    bar_color = "#00c48c" if sug['score'] > 0 else ("#ff4d6d" if sug['score'] < 0 else "#e3b341")
                    st.markdown(
                        f"""
                        <div style="position:relative;height:16px;background:#222;border-radius:8px;overflow:hidden;margin-bottom:10px">
                            <div style="position:absolute;left:50%;top:0;width:1px;height:100%;background:#555"></div>
                            <div style="position:absolute;left:{score_bar_pct}%;transform:translateX(-50%);top:1px;
                                        width:14px;height:14px;border-radius:50%;background:{bar_color}"></div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    st.write("**Factor Analysis:**")
                    for lbl, txt in sug['reasons']:
                        badge_color = {
                            'BULLISH': '🟢', 'MILD BULL': '🟢', 'BEARISH': '🔴', 'MILD BEAR': '🔴',
                            'NEUTRAL': '🟡', 'CAUTION': '🟠'
                        }.get(lbl, '⚪')
                        st.markdown(f"- {badge_color} **{lbl}:** {txt}")

                    st.caption(
                        "⚠️ This suggestion is purely algorithmic and based on open-interest analysis. "
                        "It does NOT constitute financial advice. Always apply your own judgement, "
                        "manage risk, and consult a SEBI-registered advisor before trading."
                    )

                    st.write("---")
                    st.write("**OI Walls**")
                    w1, w2, w3, w4 = st.columns(4)
                    w1.metric("Max Call OI (1°)", f"{int(m['mc_sp'])}", f"{m['mc']} {'K' if mode=='Index' else '×10'}")
                    w2.metric("Max Put OI (1°)", f"{int(m['mp_sp'])}", f"{m['mp']} {'K' if mode=='Index' else '×10'}")
                    w3.metric("Max Call OI (2°)", f"{int(m['mc_sp2'])}", f"{m['mc2']} {'K' if mode=='Index' else '×10'}")
                    w4.metric("Max Put OI (2°)", f"{int(m['mp_sp2'])}", f"{m['mp2']} {'K' if mode=='Index' else '×10'}")

            # ---------------- TAB 2: Greeks ----------------
            with tab2:
                if m is None:
                    st.warning("Could not locate the selected strike in the chain.")
                else:
                    try:
                        exp_date = datetime.datetime.strptime(expiry, '%d-%b-%Y')
                        t_days = max((exp_date - datetime.datetime.now()).days, 1)
                    except Exception:
                        t_days = 7

                    atm_row = merged[merged['Strike Price'] == sp].iloc[0]
                    ce_g = calc_greeks(points, sp, t_days, atm_row['CE IV'], 'CE')
                    pe_g = calc_greeks(points, sp, t_days, atm_row['PE IV'], 'PE')

                    st.write(f"**Strike {int(sp)}** · {t_days}d to expiry · Underlying {points:,.1f}")

                    g_df = pd.DataFrame([
                        {"Greek": "Delta (Δ)", "CE Value": f"{ce_g['delta']:+.4f}", "PE Value": f"{pe_g['delta']:+.4f}",
                         "Meaning": "Rate of price change per ₹1 move in underlying; CE∈[0,1], PE∈[-1,0]"},
                        {"Greek": "Gamma (Γ)", "CE Value": f"{ce_g['gamma']:.6f}", "PE Value": f"{pe_g['gamma']:.6f}",
                         "Meaning": "Rate of change of Delta; highest near ATM close to expiry"},
                        {"Greek": "Theta (Θ)", "CE Value": f"{ce_g['theta']:+.4f}", "PE Value": f"{pe_g['theta']:+.4f}",
                         "Meaning": "Daily time decay (₹/day); always negative for option buyers"},
                        {"Greek": "Vega (ν)", "CE Value": f"{ce_g['vega']:+.4f}", "PE Value": f"{pe_g['vega']:+.4f}",
                         "Meaning": "Price change per 1% rise in IV; long options gain from rising IV"},
                        {"Greek": "Rho (ρ)", "CE Value": f"{ce_g['rho']:+.4f}", "PE Value": f"{pe_g['rho']:+.4f}",
                         "Meaning": "Sensitivity to interest-rate changes; minor for short-dated options"},
                    ])
                    st.dataframe(g_df, use_container_width=True, hide_index=True)

                    pc1, pc2 = st.columns(2)
                    with pc1:
                        st.markdown("**CE (Call) Pricing**")
                        st.write(f"LTP: ₹{atm_row['CE LTP']:.2f}  ·  Theo (B-S): ₹{ce_g['theo_price']:.2f}")
                        st.write(f"Intrinsic: ₹{ce_g['intrinsic']:.2f}  ·  Time Value: ₹{ce_g['time_value']:.2f}")
                        st.write(f"IV: {atm_row['CE IV']:.1f}%  ·  Moneyness: {ce_g['moneyness']}")
                    with pc2:
                        st.markdown("**PE (Put) Pricing**")
                        st.write(f"LTP: ₹{atm_row['PE LTP']:.2f}  ·  Theo (B-S): ₹{pe_g['theo_price']:.2f}")
                        st.write(f"Intrinsic: ₹{pe_g['intrinsic']:.2f}  ·  Time Value: ₹{pe_g['time_value']:.2f}")
                        st.write(f"IV: {atm_row['PE IV']:.1f}%  ·  Moneyness: {pe_g['moneyness']}")

                    with st.expander("📖 Greeks Quick Guide"):
                        st.markdown(
                            "- **Δ Delta** — probability proxy: CE Δ=0.7 ≈ 70% chance of expiring ITM; "
                            "also the equivalent underlying-share hedge.\n"
                            "- **Γ Gamma** — how fast Delta changes; dangerous near ATM on expiry day.\n"
                            "- **Θ Theta** — time decay per day; sellers earn it, buyers pay it.\n"
                            "- **ν Vega** — IV sensitivity; buy before events (IV low→high), sell after "
                            "announcements (IV crush).\n"
                            "- **ρ Rho** — interest-rate sensitivity; rarely significant for near-dated "
                            "Indian options.\n\n"
                            f"Greeks are computed via Black-Scholes using each side's own IV and "
                            f"{t_days} days to expiry. Actual market prices may differ due to bid/ask "
                            "spread and skew."
                        )

            # ---------------- TAB 3: Charts ----------------
            with tab3:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=merged['Strike Price'], y=merged['CE OI'], name='CE OI', marker_color='#f85149', opacity=0.85))
                fig.add_trace(go.Bar(x=merged['Strike Price'], y=-merged['PE OI'], name='PE OI', marker_color='#3fb950', opacity=0.85))
                fig.add_vline(x=points, line_color="#58a6ff", line_width=2, line_dash="dot", annotation_text="LTP")
                fig.add_vline(x=sp, line_color="#e3b341", line_width=1.5, line_dash="dash", annotation_text="Selected")
                fig.update_layout(title="Open Interest Distribution", barmode='overlay', template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)

                atm_i = merged.index[merged['Strike Price'] == sp].tolist()
                lo, hi = (max(0, atm_i[0]-10), min(len(merged)-1, atm_i[0]+10)) if atm_i else (0, len(merged)-1)
                sub = merged.iloc[lo:hi+1]
                fig_iv = go.Figure()
                fig_iv.add_trace(go.Scatter(x=sub['Strike Price'], y=sub['CE IV'], name='CE IV',
                                             line=dict(color='#f85149', width=2), mode='lines+markers'))
                fig_iv.add_trace(go.Scatter(x=sub['Strike Price'], y=sub['PE IV'], name='PE IV',
                                             line=dict(color='#3fb950', width=2), mode='lines+markers'))
                fig_iv.add_vline(x=sp, line_color="#e3b341", line_width=1.5, line_dash="dash")
                fig_iv.update_layout(title="IV Smile (near selected strike)", yaxis_title="IV (%)", template="plotly_dark")
                st.plotly_chart(fig_iv, use_container_width=True)

            # ---------------- TAB 4: History (per-session snapshot log) ----------------
            with tab4:
                hist_key = f"oc_history_{state_key}"
                if hist_key not in st.session_state:
                    st.session_state[hist_key] = []

                if st.button("📌 Log current snapshot to history"):
                    if m is not None:
                        st.session_state[hist_key].append({
                            "Time": ts, "Underlying": points, "Strike": int(sp),
                            "PCR": m['pcr'], "Max Pain": int(m['max_pain']),
                            "CE IV": m['ce_iv'], "PE IV": m['pe_iv'], "IV Skew": m['iv_skew'],
                            "Sentiment": m['sentiment'],
                        })

                hist = st.session_state[hist_key]
                if hist:
                    hist_df = pd.DataFrame(hist)
                    st.dataframe(hist_df, use_container_width=True, hide_index=True)
                    if len(hist_df) >= 2:
                        fig_h = make_subplots(specs=[[{"secondary_y": True}]])
                        fig_h.add_trace(go.Scatter(x=hist_df.index, y=hist_df['Underlying'], name='Underlying',
                                                    line=dict(color='#e3b341')), secondary_y=False)
                        fig_h.add_trace(go.Scatter(x=hist_df.index, y=hist_df['PCR'], name='PCR',
                                                    line=dict(color='#58a6ff')), secondary_y=True)
                        fig_h.update_layout(title="Logged Snapshots — Underlying vs PCR", template="plotly_dark")
                        st.plotly_chart(fig_h, use_container_width=True)
                    csv = hist_df.to_csv(index=False).encode('utf-8')
                    st.download_button("💾 Download history CSV", csv, file_name=f"NSE-OCA-{symbol}-{expiry}.csv")
                else:
                    st.info("No snapshots logged yet in this session. Use the button above to start a log — "
                            "each click captures the current fetch, so re-fetch periodically to build a time series.")

            # ---------------- TAB 5: Full Option Chain ----------------
            with tab5:
                def _highlight_strike(row):
                    return ['background-color: rgba(227,179,65,.15)' if row['Strike Price'] == sp else '' for _ in row]

                st.dataframe(
                    merged.style.format(precision=2).apply(_highlight_strike, axis=1),
                    height=600, use_container_width=True
                )
                csv_full = merged.to_csv(index=False).encode('utf-8')
                st.download_button("💾 Download full chain CSV", csv_full, file_name=f"NSE-OC-{symbol}-{expiry}-full.csv")

# ==============================================================================
# 9. IPO DASHBOARD
# ==============================================================================
elif app_mode == "IPO Dashboard":
    st.title("NSE/BSE IPO Market Pulse")
    st.markdown("Live IPO data fetched directly from Screener.in.")

    urls_to_scrape = {
        "Upcoming & Active IPOs": "https://www.screener.in/ipo/",
        "Recently Listed IPOs": "https://www.screener.in/ipo/recent/",
        "IPOs Trading Below Issue Price": "https://www.screener.in/ipo/below-price/"
    }

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
    }

    tab1, tab2, tab3 = st.tabs(list(urls_to_scrape.keys()))

    for idx, (title, url) in enumerate(urls_to_scrape.items()):
        with [tab1, tab2, tab3][idx]:
            with st.spinner(f"Fetching {title}..."):
                try:
                    response = requests.get(url, headers=headers, timeout=10)
                    response.raise_for_status()
                    tables = pd.read_html(response.text)

                    if tables:
                        df = tables[0].dropna(how='all', axis=0).dropna(how='all', axis=1)
                        st.success(f"Found {len(df)} records.")
                        st.dataframe(df, use_container_width=True)
                    else:
                        st.warning("No HTML tables could be parsed from this page.")
                except Exception as e:
                    st.error(f"Failed to fetch data from Screener.in (IP might be blocked): {e}")
