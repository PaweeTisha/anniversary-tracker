import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date
import plotly.graph_objects as go

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Paweetida & Dawis 💜", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

# ---- CUSTOM CSS ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,400;0,600;0,700;0,800;1,400&family=DM+Sans:ital,wght@0,400;0,500;0,700;1,400&display=swap');
:root { --aurora-purple: #4A154B; --aurora-violet: #7B2CBF; --aurora-green: #00F5D4; --aurora-cyan: #4CC9F0; --aurora-dark: #0A041A; --gold: #FFD166; }
* { font-family: 'DM Sans', sans-serif; font-weight: 500; }
h1, h2, h3, .hero-title, .metric-number { font-family: 'Plus Jakarta Sans', sans-serif !important; font-weight: 800 !important; }
div[data-testid="stTextInput"]:has(input[aria-label="hidden_welcome"]),
div[data-testid="stTextInput"]:has(input[aria-label="hidden_pin"]) { display: none !important; }

.stApp { background: linear-gradient(135deg, #050210 0%, #10072B 30%, #031B26 70%, #020C1B 100%); min-height: 100vh; }
.hero-section { background: linear-gradient(135deg, rgba(123,44,191,0.6), rgba(0,245,212,0.25)); border-radius: 20px; padding: 1.5rem; text-align: center; border: 1px solid rgba(76,201,240,0.4); backdrop-filter: blur(12px); margin-bottom: 1rem; box-shadow: 0 0 35px rgba(0,245,212,0.25); }
.hero-title { font-size: 2.2rem; font-weight: 800; color: #F0E9FA; margin: 0; }
.hero-subtitle { font-size: 0.85rem; color: #4CC9F0; margin-top: 0.3rem; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 700; }
.metric-card { background: linear-gradient(135deg, rgba(123,44,191,0.5), rgba(76,201,240,0.25)); border: 1px solid rgba(0,245,212,0.3); border-radius: 16px; padding: 1rem; text-align: center; backdrop-filter: blur(8px); box-shadow: 0 0 15px rgba(123,44,191,0.2); }
.metric-number { font-size: 2.6rem; font-weight: 800; color: #FFD166; line-height: 1; }
.metric-label { font-size: 0.8rem; color: #4CC9F0; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.3rem; font-weight: 700; }
.section-title { font-size: 1.2rem; font-weight: 800; color: #F0E9FA; margin-bottom: 0.6rem; border-bottom: 1px solid rgba(0,245,212,0.4); padding-bottom: 0.3rem; }
.stButton button { background: linear-gradient(135deg, #7B2CBF, #00F5D4) !important; color: #0A041A !important; border-radius: 12px !important; font-weight: 800 !important; padding: 0.6rem 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

# ---- DATABASE & STATS ----
def init_db():
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS milestones")
    c.execute('''CREATE TABLE milestones (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, date TEXT NOT NULL)''')
    data = [
        ("First Liked Story ✨", "2025-07-27"), ("First Date 🍿", "2025-08-15"),
        ("Official Anniversary 2025 🎉", "2025-08-22"), ("NZ 1st Trip 🏔️", "2026-03-29"),
        ("Dawis Enlists Army 🪖", "2026-04-20"), ("Dawis HBD 🎂", "2026-06-29"),
        ("Paweetida HBD 🎂", "2026-07-16"), ("1st Anniversary 2026 🎉", "2026-08-22"),
    ]
    c.executemany("INSERT INTO milestones (title, date) VALUES (?,?)", data)
    conn.commit(); conn.close()

def get_milestones():
    conn = sqlite3.connect('anniversary.db')
    df = pd.read_sql_query("SELECT * FROM milestones ORDER BY date ASC", conn)
    conn.close(); return df

def calculate_stats():
    today = date.today()
    start_date = date(2025, 7, 27); official_date = date(2025, 8, 22); army_date = date(2026, 4, 20)
    next_anniv = date(2026, 8, 22)
    return {
        "days_since_first": (today - start_date).days,
        "days_together": (today - official_date).days,
        "weeks_together": (today - official_date).days // 7,
        "months_together": (today - official_date).days // 30,
        "days_to_anniversary": (next_anniv - today).days,
        "days_since_army": (today - army_date).days if today >= army_date else 0,
        "next_anniversary": next_anniv,
    }

init_db()
stats = calculate_stats()

# ---- NAVIGATION & TABS ----
if "selected_tab" not in st.session_state: st.session_state.selected_tab = "💐 Get Flowers"

nav_col1, nav_col2, nav_col3 = st.columns(3)
if nav_col1.button("💐 Get Flowers", use_container_width=True): st.session_state.selected_tab = "💐 Get Flowers"
if nav_col2.button("💌 Love Capsule", use_container_width=True): st.session_state.selected_tab = "💌 Love Capsule"
if nav_col3.button("⚔️ Battle & Stats", use_container_width=True): st.session_state.selected_tab = "⚔️ Battle Phase & Stats"

# ---- CONTENT ----
if st.session_state.selected_tab == "💐 Get Flowers":
    st.markdown("<div style='text-align:center; padding:2rem 0;'><h1 style='color:#FFD166; font-size:3rem;'>Get Flowers! 🌷</h1><p style='color:#4CC9F0; font-size:1.2rem; font-weight:700;'>Well done! A bouquet for my favorite enemy. 😜</p></div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("""
        <div style="background: linear-gradient(135deg, rgba(123,44,191,0.5), rgba(255,182,193,0.25)); border: 2px solid rgba(255,192,203,0.7); border-radius: 28px; padding: 2.2rem; text-align: center; backdrop-filter: blur(12px);">
            <div style="font-size: 5rem;">🌷🌻💐</div>
            <h2 style="color:#FFD166;">For My Favorite Rival 😈</h2>
            <p style="color:#F0E9FA; font-weight:600;">Thanks for sticking around, even when I'm super moody and don't want to talk! 555. Let's keep supporting and driving each other crazy for a long, long time. 💜</p>
        </div>
        """, unsafe_allow_html=True)

elif st.session_state.selected_tab == "💌 Love Capsule":
    st.markdown('<div class="section-title">Love Capsule — Open a Secret Note 💌</div>', unsafe_allow_html=True)
    # (Insert Love Capsule HTML code here)

elif st.session_state.selected_tab == "⚔️ Battle Phase & Stats":
    # Hero Section + Stats Counter + Timeline (Use the combined logic from previous response)
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-title">Paweetida & Dawis</div>
        <div class="hero-subtitle">OUR STORY · SINCE 27 JULY 2025</div>
    </div>
    """, unsafe_allow_html=True)
    # (Insert Stats Cards & Timeline code here)
