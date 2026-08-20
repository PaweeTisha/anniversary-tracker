import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date
import plotly.graph_objects as go
import base64

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Tisha & Dawis 💜", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

# ---- CUSTOM CSS ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&display=swap');
:root { --purple-deep: #3D1A6E; --purple-mid: #6B3FA0; --purple-light: #B08FD4; --gold: #C9A84C; }
* { font-family: 'DM Sans', sans-serif; }
.stApp { background: linear-gradient(135deg, #1A0A2E 0%, #2D1854 40%, #1E3A2A 100%); min-height: 100vh; }
.block-container { padding-top: 1.2rem !important; padding-bottom: 2rem !important; max-width: 1250px !important; }
.hero-section { background: linear-gradient(135deg, rgba(61,26,110,0.9), rgba(74,92,58,0.8)); border-radius: 16px; padding: 1.2rem 1.5rem; text-align: center; border: 1px solid rgba(176,143,212,0.3); backdrop-filter: blur(10px); margin-bottom: 1rem; }
.hero-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2rem; font-weight: 700; color: #F0E9FA; margin: 0; }
.hero-subtitle { font-size: 0.8rem; color: #B08FD4; margin-top: 0.2rem; letter-spacing: 1.5px; text-transform: uppercase; }
.metric-card { background: linear-gradient(135deg, rgba(61,26,110,0.7), rgba(74,92,58,0.5)); border: 1px solid rgba(176,143,212,0.25); border-radius: 12px; padding: 1rem; text-align: center; backdrop-filter: blur(8px); }
.metric-number { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2.4rem; font-weight: 700; color: #C9A84C; line-height: 1; }
.metric-label { font-size: 0.75rem; color: #B08FD4; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.3rem; }
.section-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.1rem; font-weight: 600; color: #F0E9FA; margin-bottom: 0.6rem; border-bottom: 1px solid rgba(176,143,212,0.3); padding-bottom: 0.2rem; }
.memory-card { background: rgba(61,26,110,0.5); border: 1px solid rgba(176,143,212,0.2); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem; }
.army-badge { background: linear-gradient(135deg, rgba(74,92,58,0.8), rgba(122,140,106,0.4)); border: 1px solid rgba(122,140,106,0.5); border-radius: 12px; padding: 1rem; text-align: center; color: #E8EDE4; }
.stTextInput input, .stTextArea textarea, .stSelectbox select { background: rgba(61,26,110,0.5) !important; border: 1px solid rgba(176,143,212,0.3) !important; color: #F0E9FA !important; border-radius: 8px !important; }
.stButton button { background: linear-gradient(135deg, #6B3FA0, #4A5C3A) !important; color: white !important; border: none !important; border-radius: 8px !important; font-weight: 500 !important; padding: 0.4rem 1.2rem !important; }
.stTabs [data-baseweb="tab"] { color: #B08FD4 !important; }
.stTabs [aria-selected="true"] { color: #F0E9FA !important; border-bottom: 2px solid #C9A84C !important; }
</style>
""", unsafe_allow_html=True)

# ---- DATABASE ----
def init_db():
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT, date TEXT NOT NULL, category TEXT DEFAULT 'memory', emoji TEXT DEFAULT '💜', image_data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS milestones (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, date TEXT NOT NULL, description TEXT, type TEXT DEFAULT 'milestone', image_data TEXT)''')
    try:
        c.execute("ALTER TABLE memories ADD COLUMN image_data TEXT")
    except: pass
    try:
        c.execute("ALTER TABLE milestones ADD COLUMN image_data TEXT")
    except: pass
    c.execute("SELECT COUNT(*) FROM milestones")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO milestones (title, date, description, type, image_data) VALUES (?,?,?,?,?)", [
            ("First Like on Story 🚌", "2025-07-27", "The day you liked my story on the bus", "start", None),
            ("Official Couple 💜", "2025-08-22", "The day we became official", "anniversary", None),
            ("Dawis Enlists Army 🪖", "2026-04-20", "Dawis joined the Australian Army", "milestone", None),
        ])
    conn.commit(); conn.close()

def get_memories():
    conn = sqlite3.connect('anniversary.db')
    df = pd.read_sql_query("SELECT * FROM memories ORDER BY date DESC", conn)
    conn.close(); return df

def add_memory(title, description, date_val, category, emoji, image_data):
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute("INSERT INTO memories (title, description, date, category, emoji, image_data) VALUES (?,?,?,?,?,?)", (title, description, str(date_val), category, emoji, image_data))
    conn.commit(); conn.close()

def delete_memory(memory_id):
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute("DELETE FROM memories WHERE id=?", (memory_id,))
    conn.commit(); conn.close()

def get_milestones():
    conn = sqlite3.connect('anniversary.db')
    df = pd.read_sql_query("SELECT * FROM milestones ORDER BY date ASC", conn)
    conn.close(); return df

def calculate_stats():
    today = date.today()
    official_date = date(2025, 8, 22)
    army_date = date(2026, 4, 20)
    next_anniversary = date(2026, 8, 22)
    if today > next_anniversary: next_anniversary = date(today.year + 1, 8, 22)
    return {
        "days_since_first": (today - date(2025, 7, 27)).days,
        "days_together": (today - official_date).days,
        "weeks_together": (today - official_date).days // 7,
        "months_together": (today - official_date).days // 30,
        "days_to_anniversary": (next_anniversary - today).days,
        "days_since_army": (today - army_date).days if today >= army_date else 0,
        "next_anniversary": next_anniversary,
    }

# ---- PASSWORD LOGIN ----
def check_password():
    if "authenticated" not in st.session_state: st.session_state.authenticated = False
    if not st.session_state.authenticated:
        st.markdown("<style>div[data-testid='stTextInput']{position:absolute; width:0; height:0; overflow:hidden; opacity:0; z-index:-9999;}</style>", unsafe_allow_html=True)
        components.html("""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: transparent; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: 'Plus Jakarta Sans', sans-serif; text-align: center; padding: 1rem; }
.title { font-family: 'Pacifico', cursive; font-size: 3.2rem; background: linear-gradient(135deg, #B08FD4, #C9A84C); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.stars { font-size: 1.2rem; letter-spacing: 0.4rem; margin: 0.5rem 0; }
.pin-section { margin-top: 1.5rem; background: rgba(61,26,110,0.6); border: 1px solid rgba(176,143,212,0.3); border-radius: 20px; padding: 1.5rem 2rem; max-width: 400px; width: 100%; backdrop-filter: blur(10px); }
.pin-boxes { display: flex; justify-content: center; gap: 0.6rem; margin-bottom: 1.2rem; }
.pin-box { width: 46px; height: 56px; border: 2px solid rgba(176,143,212,0.4); border-radius: 10px; background: rgba(61,26,110,0.5); font-size: 1.6rem; color: #C9A84C; text-align: center; font-weight: 700; outline: none; }
.enter-btn { background: linear-gradient(135deg, #6B3FA0, #4A5C3A); color: white; border: none; border-radius: 10px; padding: 0.75rem 2.5rem; width: 100%; cursor: pointer; }
</style></head>
<body>
    <div class="title">Paweetida & Mr. Dawis</div>
    <div class="stars">🪐 🌙 🌟 ⭐ ❄️</div>
    <div class="pin-section">
        <div class="pin-boxes">
            <input class="pin-box" maxlength="1" type="password" id="p0" inputmode="numeric"><input class="pin-box" maxlength="1" type="password" id="p1" inputmode="numeric"><input class="pin-box" maxlength="1" type="password" id="p2" inputmode="numeric"><input class="pin-box" maxlength="1" type="password" id="p3" inputmode="numeric"><input class="pin-box" maxlength="1" type="password" id="p4" inputmode="numeric"><input class="pin-box" maxlength="1" type="password" id="p5" inputmode="numeric">
        </div>
        <button class="enter-btn" onclick="checkPin()">Enter Our World 💜</button>
    </div>
    <script>
    const boxes = document.querySelectorAll('.pin-box');
    boxes[0].focus();
    boxes.forEach((box, i) => {
        box.addEventListener('input', (e) => { if(box.value && i < 5) boxes[i+1].focus(); });
        box.addEventListener('keydown', (e) => { if(e.key === 'Backspace' && !box.value && i > 0) boxes[i-1].focus(); });
    });
    function checkPin() {
        let pin = Array.from(boxes).map(b => b.value).join('');
        if (pin === '220825') {
            const h = window.parent.document.querySelector('input[aria-label="hidden_pin"]');
            let s = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            s.call(h, pin); h.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }
    </script>
</body>
</html>
""", height=720)
        p = st.text_input("hidden_pin", type="password", key="pwd_backup", label_visibility="collapsed")
        if p == "220825": st.session_state.authenticated = True; st.rerun()
        st.stop()

# ---- APP ----
check_password()
init_db()
stats = calculate_stats()
st.markdown(f"<div class='hero-section'><div class='hero-title'>Paweetida & Mr. Dawis</div><div class='hero-subtitle'>OUR STORY · SINCE 27 JULY 2025</div></div>", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["📊 Our Stats", "💜 Memories", "📸 Timeline", "➕ Add Memory"])
with t1:
    col1, col2 = st.columns(2)
    with col1: st.markdown(f'<div class="metric-card"><div class="metric-number">{stats["days_together"]}</div><div class="metric-label">Days Together</div></div>', unsafe_allow_html=True)
    with col2: st.markdown(f'<div class="metric-card"><div class="metric-number">{stats["days_since_army"]}</div><div class="metric-label">Days in Service</div></div>', unsafe_allow_html=True)

with t2:
    for _, row in get_memories().iterrows():
        st.markdown(f'<div class="memory-card"><b>{row["emoji"]} {row["title"]}</b> ({row["date"]})</div>', unsafe_allow_html=True)

with t3:
    st.markdown('<div class="section-title">Our Timeline Scrapbook 📸</div>', unsafe_allow_html=True)
    milestones = get_milestones()
    memories = get_memories()
    all_events = pd.concat([
        milestones[['title', 'date', 'image_data']].assign(emoji='⭐'),
        memories[['title', 'date', 'emoji', 'image_data']]
    ]).sort_values('date')

    html_items = ""
    for _, event in all_events.iterrows():
        img_html = f'<img src="data:image/jpeg;base64,{event["image_data"]}" style="width:100%;height:100px;object-fit:cover;">' if pd.notna(event.get('image_data')) else event['emoji']
        html_items += f"""
        <div class="tl-row" style="display:flex; justify-content:space-between; margin-bottom:20px;">
            <div style="width:45%; text-align:right;">
                <div style="background:#3D1A6E; padding:10px; border-radius:10px; cursor:pointer; position:relative;">
                    <div style="font-size:0.8rem; color:#C9A84C;">{event['date']}</div>
                    <div style="font-weight:bold;">{event['title']}</div>
                    <div class="pop" style="display:none; position:absolute; bottom:110%; left:0; background:white; padding:5px; border-radius:5px; width:120px;">{img_html}</div>
                </div>
            </div>
        </div>
        <style>.tl-row:hover .pop{{display:block;}}</style>
        """
    components.html(f"<div style='padding:20px;'>{html_items}</div>", height=500, scrolling=True)

with t4:
    t = st.text_input("Title")
    img = st.file_uploader("Upload Image", type=['jpg', 'png'])
    if st.button("Save Memory"):
        img_b64 = base64.b64encode(img.getvalue()).decode() if img else None
        add_memory(t, "", date.today(), "General", "💜", img_b64)
        st.rerun()
