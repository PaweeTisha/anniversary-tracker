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

# ---- CUSTOM CSS (SCAPBOOK STYLE & FIT) ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=Sacramento&display=swap');

:root { --purple-deep: #3D1A6E; --purple-mid: #6B3FA0; --purple-light: #B08FD4; --gold: #C9A84C; }
* { font-family: 'DM Sans', sans-serif; }
.stApp { background: linear-gradient(135deg, #1A0A2E 0%, #2D1854 40%, #1E3A2A 100%); min-height: 100vh; }
.block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; max-width: 1200px !important; }

.hero-section { background: linear-gradient(135deg, rgba(61,26,110,0.9), rgba(74,92,58,0.8)); border-radius: 12px; padding: 0.8rem 1rem; text-align: center; border: 1px solid rgba(176,143,212,0.3); backdrop-filter: blur(10px); margin-bottom: 0.6rem; }
.hero-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.6rem; font-weight: 700; color: #F0E9FA; margin: 0; }
.hero-subtitle { font-size: 0.65rem; color: #B08FD4; margin-top: 0.1rem; letter-spacing: 1.5px; text-transform: uppercase; }

.metric-card { background: linear-gradient(135deg, rgba(61,26,110,0.7), rgba(74,92,58,0.5)); border: 1px solid rgba(176,143,212,0.25); border-radius: 8px; padding: 0.5rem; text-align: center; backdrop-filter: blur(8px); }
.metric-number { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.8rem; font-weight: 700; color: #C9A84C; line-height: 1; }
.metric-label { font-size: 0.6rem; color: #B08FD4; text-transform: uppercase; letter-spacing: 0.8px; margin-top: 0.2rem; }

.section-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.9rem; font-weight: 600; color: #F0E9FA; margin-bottom: 0.4rem; border-bottom: 1px solid rgba(176,143,212,0.3); padding-bottom: 0.1rem; }

.stTextInput input, .stTextArea textarea, .stSelectbox select { background: rgba(61,26,110,0.5) !important; border: 1px solid rgba(176,143,212,0.3) !important; color: #F0E9FA !important; border-radius: 6px !important; }
.stButton button { background: linear-gradient(135deg, #6B3FA0, #4A5C3A) !important; color: white !important; border: none !important; border-radius: 6px !important; font-weight: 500 !important; padding: 0.2rem 0.8rem !important; }
.stTabs [data-baseweb="tab"] { color: #B08FD4 !important; }
.stTabs [aria-selected="true"] { color: #F0E9FA !important; border-bottom: 2px solid #C9A84C !important; }
</style>
""", unsafe_allow_html=True)

# ---- DATABASE & CALC ----
def init_db():
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, date TEXT, category TEXT, emoji TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS milestones (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date TEXT, description TEXT)''')
    c.execute("SELECT COUNT(*) FROM milestones")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO milestones (title, date, description) VALUES (?,?,?)", 
                      [("Met on the bus", "2025-07-27", "The start of everything"), ("Official Couple", "2025-08-22", "Always together")])
    conn.commit(); conn.close()

def get_memories():
    conn = sqlite3.connect('anniversary.db')
    df = pd.read_sql_query("SELECT * FROM memories ORDER BY date DESC", conn)
    conn.close(); return df

def add_memory(title, desc, date_val, cat, emoji):
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute("INSERT INTO memories (title, description, date, category, emoji) VALUES (?,?,?,?,?)", (title, desc, str(date_val), cat, emoji))
    conn.commit(); conn.close()

def delete_memory(mid):
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute("DELETE FROM memories WHERE id=?", (mid,))
    conn.commit(); conn.close()

def get_milestones():
    conn = sqlite3.connect('anniversary.db')
    df = pd.read_sql_query("SELECT * FROM milestones ORDER BY date ASC", conn)
    conn.close(); return df

def calculate_stats():
    today = date.today(); official = date(2025, 8, 22)
    return {"days": (today - official).days, "weeks": (today - official).days // 7}

# ---- LOGIN ----
def check_password():
    if "auth" not in st.session_state: st.session_state.auth = False
    if not st.session_state.auth:
        st.markdown("<style>div[data-testid='stTextInput']{position:absolute; opacity:0;}</style>", unsafe_allow_html=True)
        components.html("""
<!DOCTYPE html>
<html>
<head><link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>body{margin:0;display:flex;justify-content:center;align-items:center;height:100vh;background:transparent;font-family:'Plus Jakarta Sans';text-align:center;}
.pin-section{background:rgba(61,26,110,0.6);padding:2rem;border-radius:20px;backdrop-filter:blur(10px);border:1px solid #B08FD4;}
.title{font-family:'Pacifico';font-size:2.5rem;color:#C9A84C;}
.pin-box{width:40px;height:50px;text-align:center;font-size:1.5rem;background:rgba(0,0,0,0.3);color:white;border:1px solid #B08FD4;border-radius:10px;margin:2px;}
</style></head>
<body><div class="pin-section"><div class="title">Paweetida & Mr. Dawis</div><div style="margin:1rem 0;"><input class="pin-box" maxlength="6" type="password" id="pin" inputmode="numeric"></div><button onclick="check()">Enter</button></div>
<script>function check(){if(document.getElementById('pin').value==='220825'){const h=window.parent.document.querySelector('input[aria-label="hidden_pin"]');let s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;s.call(h,'220825');h.dispatchEvent(new Event('input',{bubbles:true}));}}</script></body></html>
""", height=300)
        p = st.text_input("hidden_pin", type="password", key="pwd_b", label_visibility="collapsed")
        if p == "220825": st.session_state.auth = True; st.rerun()
        st.stop()
check_password()
init_db(); stats = calculate_stats()

# ---- MAIN ----
st.markdown(f"""<div class="hero-section"><div class="hero-title">Paweetida & Mr. Dawis</div><div class="hero-subtitle">OUR STORY · {stats['days']} DAYS OF LOVE</div></div>""", unsafe_allow_html=True)
t1, t2, t3, t4 = st.tabs(["📊 Stats", "💜 Memories", "📸 Timeline", "➕ Add"])

with t1:
    c1, c2 = st.columns(2)
    with c1: st.markdown(f'<div class="metric-card"><div class="metric-number">{stats["days"]}</div><div class="metric-label">Days Together</div></div>', unsafe_allow_html=True)
    with c2: st.markdown(f'<div class="metric-card"><div class="metric-number">{stats["weeks"]}</div><div class="metric-label">Weeks Together</div></div>', unsafe_allow_html=True)

with t2:
    st.markdown('<div class="section-title">Memories</div>', unsafe_allow_html=True)
    for _, row in get_memories().iterrows():
        st.markdown(f'<div class="memory-card"><b>{row["emoji"]} {row["title"]}</b> ({row["date"]}) - {row["description"]}</div>', unsafe_allow_html=True)

with t3:
    st.markdown('<div class="section-title">Timeline Scrapbook</div>', unsafe_allow_html=True)
    for _, event in pd.concat([get_milestones().rename(columns={'title':'title', 'date':'date', 'description':'desc'}), get_memories()]).sort_values('date').iterrows():
        with st.expander(f"{event['date']} — {event.get('title', 'Moment')}"):
            st.write(event.get('desc', 'A special moment 💜'))

with t4:
    st.markdown('<div class="section-title">Add Memory (English)</div>', unsafe_allow_html=True)
    t = st.text_input("Title")
    d = st.date_input("Date")
    desc = st.text_area("Description")
    if st.button("Save"): add_memory(t, desc, d, "General", "💜"); st.rerun()
