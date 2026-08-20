import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date
import plotly.graph_objects as go
import plotly.express as px
import os

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Tisha & Dawis 💜",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---- CUSTOM CSS ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --purple-deep: #3D1A6E;
    --purple-mid: #6B3FA0;
    --purple-light: #B08FD4;
    --purple-pale: #F0E9FA;
    --army-green: #4A5C3A;
    --army-light: #7A8C6A;
    --army-pale: #E8EDE4;
    --gold: #C9A84C;
    --white: #FAFAFA;
    --text-dark: #1A1A2E;
}

* { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #1A0A2E 0%, #2D1854 40%, #1E3A2A 100%);
    min-height: 100vh;
}

.hero-section {
    background: linear-gradient(135deg, rgba(61,26,110,0.9), rgba(74,92,58,0.8));
    border-radius: 20px;
    padding: 3rem 2rem;
    text-align: center;
    border: 1px solid rgba(176,143,212,0.3);
    backdrop-filter: blur(10px);
    margin-bottom: 2rem;
}

.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    color: #F0E9FA;
    margin: 0;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 1rem;
    color: #B08FD4;
    margin-top: 0.5rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.metric-card {
    background: linear-gradient(135deg, rgba(61,26,110,0.7), rgba(74,92,58,0.5));
    border: 1px solid rgba(176,143,212,0.25);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    backdrop-filter: blur(8px);
    transition: transform 0.2s;
}

.metric-card:hover { transform: translateY(-4px); }

.metric-number {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    color: #C9A84C;
    line-height: 1;
}

.metric-label {
    font-size: 0.8rem;
    color: #B08FD4;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 0.5rem;
}

.metric-desc {
    font-size: 0.85rem;
    color: #E0D4F5;
    margin-top: 0.3rem;
}

.section-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.4rem;
    font-weight: 600;
    color: #F0E9FA;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(176,143,212,0.3);
    padding-bottom: 0.5rem;
    letter-spacing: -0.3px;
}

.memory-card {
    background: rgba(61,26,110,0.5);
    border: 1px solid rgba(176,143,212,0.2);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    backdrop-filter: blur(6px);
}

.memory-date {
    font-size: 0.75rem;
    color: #C9A84C;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.memory-title {
    font-size: 1rem;
    font-weight: 600;
    color: #F0E9FA;
    margin: 0.25rem 0;
}

.memory-desc {
    font-size: 0.85rem;
    color: #B08FD4;
}

.emoji-tag {
    font-size: 1.2rem;
    margin-right: 0.5rem;
}

.army-badge {
    background: linear-gradient(135deg, rgba(74,92,58,0.8), rgba(122,140,106,0.4));
    border: 1px solid rgba(122,140,106,0.5);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    text-align: center;
    color: #E8EDE4;
}

.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: rgba(61,26,110,0.5) !important;
    border: 1px solid rgba(176,143,212,0.3) !important;
    color: #F0E9FA !important;
    border-radius: 8px !important;
}

.stButton button {
    background: linear-gradient(135deg, #6B3FA0, #4A5C3A) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    padding: 0.5rem 1.5rem !important;
}

.stButton button:hover {
    background: linear-gradient(135deg, #8B5CC0, #5A7048) !important;
    transform: translateY(-1px) !important;
}

div[data-testid="stMetricValue"] {
    color: #C9A84C !important;
    font-family: 'Playfair Display', serif !important;
}

.stTabs [data-baseweb="tab"] {
    color: #B08FD4 !important;
}

.stTabs [aria-selected="true"] {
    color: #F0E9FA !important;
    border-bottom: 2px solid #C9A84C !important;
}
</style>
""", unsafe_allow_html=True)

# ---- DATABASE & CALC ----
def init_db():
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT, date TEXT NOT NULL, category TEXT DEFAULT 'memory', emoji TEXT DEFAULT '💜', created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS milestones (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, date TEXT NOT NULL, description TEXT, type TEXT DEFAULT 'milestone')''')
    c.execute("SELECT COUNT(*) FROM milestones")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO milestones (title, date, description, type) VALUES (?,?,?,?)", 
                      [("First Like on Story 🚌", "2025-07-27", "กดไลค์สตอรี่ครั้งแรก — บนรถบัส", "start"),
                       ("Official Couple 💜", "2025-08-22", "วันที่เป็นแฟนกันอย่างเป็นทางการ", "anniversary"),
                       ("Dawis Enlists Army 🪖", "2026-04-20", "วันที่ Dawis เข้า Australian Army", "milestone")])
    conn.commit()
    conn.close()

def get_memories():
    conn = sqlite3.connect('anniversary.db')
    df = pd.read_sql_query("SELECT * FROM memories ORDER BY date DESC", conn)
    conn.close()
    return df

def add_memory(title, description, date_val, category, emoji):
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute("INSERT INTO memories (title, description, date, category, emoji) VALUES (?,?,?,?,?)", (title, description, str(date_val), category, emoji))
    conn.commit()
    conn.close()

def delete_memory(memory_id):
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute("DELETE FROM memories WHERE id=?", (memory_id,))
    conn.commit()
    conn.close()

def get_milestones():
    conn = sqlite3.connect('anniversary.db')
    df = pd.read_sql_query("SELECT * FROM milestones ORDER BY date ASC", conn)
    conn.close()
    return df

def calculate_stats():
    today = date.today()
    start_date = date(2025, 7, 27); official_date = date(2025, 8, 22); army_date = date(2026, 4, 20); next_anniversary = date(2026, 8, 22)
    if today > next_anniversary: next_anniversary = date(today.year + 1, 8, 22)
    return {"days_since_first": (today - start_date).days, "days_together": (today - official_date).days, "weeks_together": (today - official_date).days // 7, "months_together": (today - official_date).days // 30, "days_to_anniversary": (next_anniversary - today).days, "days_since_army": (today - army_date).days if today >= army_date else 0, "next_anniversary": next_anniversary}

# ---- LOGIN ----
def check_password():
    if "authenticated" not in st.session_state: st.session_state.authenticated = False
    if not st.session_state.authenticated:
        st.markdown("""<style>.block-container{padding-top:1rem!important; max-width:100%!important;} div[data-testid="stTextInput"]{position:absolute; opacity:0;}</style>""", unsafe_allow_html=True)
        components.html("""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
body { background: transparent; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: 'Plus Jakarta Sans', sans-serif; text-align: center; }
@keyframes bounce { 0%, 100% { transform: translateY(0px) rotate(-3deg); } 50% { transform: translateY(-15px) rotate(3deg); } }
.chars { display: flex; justify-content: center; align-items: center; gap: 1.5rem; margin-bottom: 1rem; }
.girl { font-size: 4rem; animation: bounce 1.4s ease-in-out infinite; display: inline-block; }
.heart { font-size: 2.8rem; animation: bounce 1.2s ease-in-out infinite; display: inline-block; }
.soldier { font-size: 4rem; animation: bounce 1.6s ease-in-out infinite; display: inline-block; }
.title { font-family: 'Pacifico', cursive; font-size: 3.2rem; background: linear-gradient(135deg, #B08FD4, #C9A84C); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.pin-section { margin-top: 1.5rem; background: rgba(61,26,110,0.6); border: 1px solid rgba(176,143,212,0.3); border-radius: 20px; padding: 1.5rem 2rem; max-width: 400px; width: 100%; backdrop-filter: blur(10px); }
.pin-box { width: 46px; height: 56px; border: 2px solid rgba(176,143,212,0.4); border-radius: 10px; background: rgba(61,26,110,0.5); font-size: 1.6rem; color: #C9A84C; text-align: center; margin: 0 3px; outline: none; }
.enter-btn { background: linear-gradient(135deg, #6B3FA0, #4A5C3A); color: white; border: none; border-radius: 10px; padding: 0.75rem 2.5rem; margin-top:1rem; cursor: pointer; width: 100%; }
.floating-emoji { position: fixed; font-size: 1.5rem; animation: floatUp linear infinite; pointer-events: none; z-index: 0; opacity: 0.7; }
@keyframes floatUp { 0% { transform: translateY(100vh); } 100% { transform: translateY(-10vh); } }
</style>
</head>
<body>
    <div id="floaters"></div>
    <div style="position:relative; z-index:1;">
    <div class="chars"><span class="girl">💻</span><span class="heart">💜</span><span class="soldier">🪖</span></div>
    <div class="title">Paweetida & Mr. Dawis</div>
    <div style="color:#B08FD4; letter-spacing:2px; margin:0.5rem 0;">OUR PRIVATE LITTLE WORLD 💜</div>
    <div class="pin-section">
        <div style="color:#C9A84C; font-family:'Pacifico'; margin-bottom:0.5rem;">Enter our secret code</div>
        <div id="boxes"><input class="pin-box" maxlength="1" type="password" id="p0" inputmode="numeric"><input class="pin-box" maxlength="1" type="password" id="p1" inputmode="numeric"><input class="pin-box" maxlength="1" type="password" id="p2" inputmode="numeric"><input class="pin-box" maxlength="1" type="password" id="p3" inputmode="numeric"><input class="pin-box" maxlength="1" type="password" id="p4" inputmode="numeric"><input class="pin-box" maxlength="1" type="password" id="p5" inputmode="numeric"></div>
        <button class="enter-btn" onclick="checkPin()">Enter Our World 💜</button>
    </div>
    </div>
    <script>
    const container = document.getElementById('floaters');
    const emojis = ['🌟','💜','💚','💙','⭐','🤍','💛','🍀','🌐','💻'];
    for(let i=0; i<20; i++){
        const el = document.createElement('div'); el.className = 'floating-emoji'; el.textContent = emojis[Math.floor(Math.random()*emojis.length)];
        el.style.left = Math.random()*100 + 'vw'; el.style.animationDuration = (5+Math.random()*8) + 's'; container.appendChild(el);
    }
    function checkPin() {
        let pin = Array.from(document.querySelectorAll('.pin-box')).map(b => b.value).join('');
        if(pin === '220825') {
            const hidden = window.parent.document.querySelector('input[aria-label="hidden_pin"]');
            let setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            setter.call(hidden, pin); hidden.dispatchEvent(new Event('input', {bubbles: true}));
        } else { alert("Hmm, try again! 💔"); }
    }
    </script>
</body>
</html>
""", height=400, scrolling=False)
        password = st.text_input("hidden_pin", type="password", key="pwd_backup", label_visibility="collapsed")
        if password == "220825": st.session_state.authenticated = True; st.rerun()
        return False
    return True

if not check_password(): st.stop()

# ---- MAIN APP ----
init_db(); stats = calculate_stats()
st.markdown(f"""
<div class="hero-section">
    <div class="hero-title">Paweetida & Mr. Dawis</div>
    <div class="hero-subtitle">OUR STORY · SINCE 27 JULY 2025</div>
</div>
""", unsafe_allow_html=True)

tab1, tab2, tab3, tab4 = st.tabs(["📊 Our Stats", "💜 Memories", "🗓️ Timeline", "➕ Add Memory"])
# ... (ส่วนตารางอื่นๆ เหมือนเดิมตามไฟล์ล่าสุดของคุณ)
