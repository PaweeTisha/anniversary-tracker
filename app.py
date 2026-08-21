import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date
import plotly.graph_objects as go
import base64

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Paweetida & Dawis 💜", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

# ---- CUSTOM CSS (AURORA THEME + SHOOTING STARS + HIDE HIDDEN INPUTS + MENU BOXES) ----
# (คง CSS เดิมไว้ทั้งหมด และเพิ่ม CSS สำหรับกล่องเมนูใหม่)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&display=swap');

:root {
    --aurora-purple: #4A154B;
    --aurora-violet: #7B2CBF;
    --aurora-green: #00F5D4;
    --aurora-cyan: #4CC9F0;
    --aurora-dark: #0A041A;
    --gold: #FFD166;
}

* { font-family: 'DM Sans', sans-serif; }

/* ซ่อนช่องอินพุตระบบ (hidden inputs) แบบถาวรไม่ให้มีแถบโผล่มากวนใจ */
div[data-testid="stTextInput"]:has(input[aria-label="hidden_welcome"]),
div[data-testid="stTextInput"]:has(input[aria-label="hidden_pin"]) {
    display: none !important;
    height: 0px !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* AURORA LIGHTS DYNAMIC BACKGROUND ANIMATION */
.stApp {
    background: linear-gradient(135deg, #050210 0%, #10072B 30%, #031B26 70%, #020C1B 100%);
    background-size: 400% 400%;
    animation: auroraFlow 15s ease infinite;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}

@keyframes auroraFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp::before {
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(0,245,212,0.12) 0%, rgba(76,201,240,0.08) 30%, transparent 70%);
    animation: auroraShimmer 10s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

@keyframes auroraShimmer {
    0% { transform: translateY(-20px) scale(1); opacity: 0.6; }
    100% { transform: translateY(20px) scale(1.1); opacity: 1; }
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1250px !important;
    position: relative;
    z-index: 1;
}

@keyframes shootingStar {
    0% { transform: translateX(0) translateY(0); opacity: 1; }
    100% { transform: translateX(-600px) translateY(600px); opacity: 0; }
}

.shooting-star {
    position: fixed;
    width: 2px;
    height: 2px;
    background: #00F5D4;
    border-radius: 50%;
    box-shadow: 0 0 10px 2px #00F5D4, 0 0 25px 6px #4CC9F0;
    animation: shootingStar linear infinite;
    z-index: 1;
    pointer-events: none;
}

.breaking-news-bar {
    background: linear-gradient(90deg, #8B0000, #00F5D4, #8B0000);
    border: 1px solid #FFD166;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    color: #FFFFFF;
    font-weight: 700;
    font-size: 0.9rem;
    margin-bottom: 1.0rem;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 0 25px rgba(0, 245, 212, 0.4);
    position: relative;
    z-index: 2;
}
.breaking-badge {
    background: #FFFFFF;
    color: #8B0000;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    white-space: nowrap;
    animation: pulse 1.5s infinite;
}
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

.hero-section {
    background: linear-gradient(135deg, rgba(123,44,191,0.6), rgba(0,245,212,0.25));
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(76,201,240,0.4);
    backdrop-filter: blur(12px);
    margin-bottom: 1rem;
    box-shadow: 0 0 35px rgba(0,245,212,0.25);
    position: relative;
    z-index: 2;
}

.hero-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2rem; font-weight: 700; color: #F0E9FA; margin: 0; }
.hero-subtitle { font-size: 0.8rem; color: #4CC9F0; margin-top: 0.2rem; letter-spacing: 1.5px; text-transform: uppercase; }

.metric-card {
    background: linear-gradient(135deg, rgba(123,44,191,0.5), rgba(76,201,240,0.25));
    border: 1px solid rgba(0,245,212,0.3);
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    backdrop-filter: blur(8px);
    position: relative;
    z-index: 2;
    box-shadow: 0 0 15px rgba(123,44,191,0.2);
}

.metric-number { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2.4rem; font-weight: 700; color: #FFD166; line-height: 1; }
.metric-label { font-size: 0.75rem; color: #4CC9F0; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.3rem; }

.section-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #F0E9FA;
    margin-bottom: 0.6rem;
    border-bottom: 1px solid rgba(0,245,212,0.4);
    padding-bottom: 0.2rem;
    position: relative;
    z-index: 2;
}

.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: rgba(30, 15, 60, 0.85) !important;
    border: 1px solid rgba(76,201,240,0.5) !important;
    color: #F0E9FA !important;
    border-radius: 8px !important;
}

.stButton button {
    background: linear-gradient(135deg, #7B2CBF, #00F5D4) !important;
    color: #0A041A !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 0.4rem 1.2rem !important;
    box-shadow: 0 0 20px rgba(0,245,212,0.5);
}

.stTabs [data-baseweb="tab"] { color: #4CC9F0 !important; z-index: 2; }
.stTabs [aria-selected="true"] { color: #00F5D4 !important; border-bottom: 2px solid #FFD166 !important; }

/* เมนู 4 กล่องใหม่ */
.menu-container { display: flex; flex-wrap: wrap; justify-content: center; gap: 15px; margin-bottom: 1.5rem; }
.menu-box {
    background: linear-gradient(135deg, rgba(123,44,191,0.75), rgba(255,209,102,0.3));
    border: 2px solid #00F5D4;
    border-radius: 24px;
    padding: 1.5rem;
    width: 250px; /* ปรับขนาดให้พอดี */
    text-align: center;
    transition: all 0.3s;
    cursor: pointer;
    box-shadow: 0 0 25px rgba(0,245,212,0.4);
    display: flex; flex-direction: column; align-items: center; justify-content: center;
    text-decoration: none !important;
}
.menu-box:hover { transform: scale(1.05); border-color: #FFD166; box-shadow: 0 0 30px rgba(255,209,102,0.6); background: linear-gradient(135deg, rgba(157,78,221,0.85), rgba(255,209,102,0.4)); }
.menu-icon { font-size: 3.5rem; margin-bottom: 0.8rem; filter: drop-shadow(0 0 10px rgba(255,209,102,0.7)); }
.menu-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.1rem; font-weight: 700; color: #FFD166; line-height: 1.3; }
.menu-subtitle { font-size: 0.8rem; color: #F0E9FA; margin-top: 0.4rem; font-weight: 500; }
</style>

<script>
window.addEventListener('DOMContentLoaded', (event) => {
    for (let i = 0; i < 18; i++) {
        let star = document.createElement('div');
        star.className = 'shooting-star';
        star.style.top = Math.random() * 70 + 'vh';
        star.style.left = Math.random() * 100 + 'vw';
        star.style.animationDuration = (2 + Math.random() * 4) + 's';
        star.style.animationDelay = (Math.random() * 5) + 's';
        document.body.appendChild(star);
    }
});
</script>
""", unsafe_allow_html=True)

# ---- DATABASE & STATS ----
def init_db():
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS milestones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        type TEXT DEFAULT 'milestone'
    )''')
    
    c.execute("DROP TABLE IF EXISTS milestones")
    c.execute('''CREATE TABLE IF NOT EXISTS milestones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        type TEXT DEFAULT 'milestone'
    )''')
    
    default_milestones = [
        ("First Liked Story ✨", "2025-07-27", "The day you first liked my IG story", "start"),
        ("First Date 🍿", "2025-08-15", "Our first movie and food date", "date"),
        ("Official Anniversary 2025 🎉", "2025-08-22", "The day we became official couple", "anniversary"),
        ("NZ 1st Trip 🏔️", "2026-03-29", "1st trip together in NZ", "trip"),
        ("Dawis Enlists Army 🪖", "2026-04-20", "Dawis joined the Australian Army", "milestone"),
        ("Dawis HBD 🎂", "2026-06-29", "Happy Birthday Dawis", "hbd"),
        ("Paweetida HBD 🎂", "2026-07-16", "Happy Birthday Paweetida", "hbd"),
        ("1st Anniversary 2026 🎉", "2026-08-22", "Celebrating 1 year together", "anniversary"),
    ]
    c.executemany("INSERT INTO milestones (title, date, description, type) VALUES (?,?,?,?)", default_milestones)
    conn.commit()
    conn.close()

def get_milestones():
    conn = sqlite3.connect('anniversary.db')
    df = pd.read_sql_query("SELECT * FROM milestones ORDER BY date ASC", conn)
    conn.close()
    return df

def calculate_stats():
    today = date.today()
    start_date = date(2025, 7, 27)
    official_date = date(2025, 8, 22)
    army_date = date(2026, 4, 20)
    next_anniversary = date(2026, 8, 22)
    if today > next_anniversary:
        next_anniversary = date(today.year + 1, 8, 22)

    return {
        "days_since_first": (today - start_date).days,
        "days_together": (today - official_
