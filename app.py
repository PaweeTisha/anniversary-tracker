import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date
import plotly.graph_objects as go
import os

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Tisha & Dawis 💜", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

# ---- CSS ----
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #1A0A2E 0%, #2D1854 40%, #1E3A2A 100%); }
.block-container { padding: 1.5rem !important; max-width: 1200px !important; }
.hero-section { background: rgba(61,26,110,0.6); border-radius: 16px; padding: 1.5rem; text-align: center; border: 1px solid rgba(176,143,212,0.3); backdrop-filter: blur(10px); margin-bottom: 1rem; }
.hero-title { font-family: 'Pacifico', cursive; font-size: 2.2rem; color: #F0E9FA; margin: 0; }
.section-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.1rem; color: #F0E9FA; border-bottom: 1px solid #B08FD4; padding-bottom: 0.3rem; margin-bottom: 0.8rem; }
.metric-card { background: rgba(61,26,110,0.5); padding: 1rem; border-radius: 12px; text-align: center; }
.stTabs [data-baseweb="tab"] { color: #B08FD4 !important; }
.stTabs [aria-selected="true"] { color: #F0E9FA !important; border-bottom: 2px solid #C9A84C !important; }
</style>
""", unsafe_allow_html=True)

# ---- DB & STATS ----
def init_db():
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, date TEXT, category TEXT, emoji TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS milestones (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date TEXT, description TEXT)')
    conn.commit(); conn.close()

def get_memories():
    conn = sqlite3.connect('anniversary.db')
    df = pd.read_sql_query("SELECT * FROM memories ORDER BY date DESC", conn)
    conn.close(); return df

def add_memory(t, d, date_val, cat, em):
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute("INSERT INTO memories (title, description, date, category, emoji) VALUES (?,?,?,?,?)", (t, d, str(date_val), cat, em))
    conn.commit(); conn.close()

# ---- LOGIN (คงขนาดเดิม) ----
def check_password():
    if "auth" not in st.session_state: st.session_state.auth = False
    if not st.session_state.auth:
        components.html("""
        <!DOCTYPE html>
        <html>
        <head><style>
        body{display:flex;justify-content:center;align-items:center;height:100vh;margin:0;background:linear-gradient(135deg, #1A0A2E, #2D1854);font-family:sans-serif;}
        .container{background:rgba(61,26,110,0.6);padding:2.5rem;border-radius:20px;backdrop-filter:blur(10px);border:1px solid #B08FD4;text-align:center;}
        .title{font-family:cursive;font-size:2.5rem;color:#C9A84C;margin-bottom:1rem;}
        .pin-box{width:45px;height:55px;text-align:center;font-size:1.5rem;background:rgba(0,0,0,0.3);color:white;border:1px solid #B08FD4;border-radius:10px;margin:3px;}
        .btn{margin-top:1rem;padding:0.7rem 2rem;background:#6B3FA0;color:white;border:none;border-radius:10px;cursor:pointer;}
        </style></head>
        <body><div class="container"><div class="title">Paweetida & Mr. Dawis</div>
        <input class="pin-box" maxlength="6" type="password" id="pin" inputmode="numeric">
        <br><button class="btn" onclick="check()">Enter Our World</button></div>
        <script>function check(){if(document.getElementById('pin').value==='220825'){const h=window.parent.document.querySelector('input[aria-label="hidden_pin"]');let s=Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;s.call(h,'220825');h.dispatchEvent(new Event('input',{bubbles:true}));}}</script></body></html>
        """, height=720) # คงขนาด 720 ไว้ตามที่คุณชอบ
        p = st.text_input("hidden_pin", type="password", key="pwd_b", label_visibility="collapsed")
        if p == "220825": st.session_state.auth = True; st.rerun()
        st.stop()

# ---- APP ----
check_password()
init_db()
st.markdown("<div class='hero-section'><div class='hero-title'>Paweetida & Mr. Dawis</div><div class='hero-subtitle'>OUR STORY · FOREVER</div></div>", unsafe_allow_html=True)

t1, t2, t3, t4 = st.tabs(["📊 Stats", "💜 Memories", "📸 Timeline", "➕ Add"])

with t1:
    days = (date.today() - date(2025, 8, 22)).days
    st.markdown(f'<div class="metric-card"><div class="metric-number">{days}</div><div class="metric-label">Days Together</div></div>', unsafe_allow_html=True)

with t2:
    for _, row in get_memories().iterrows():
        st.markdown(f'<div class="memory-card"><b>{row["emoji"]} {row["title"]}</b> ({row["date"]}) - {row["description"]}</div>', unsafe_allow_html=True)

with t3:
    components.html("""
    <style>
    .timeline{position:relative;max-width:800px;margin:20px auto;}
    .timeline::after{content:'';position:absolute;width:3px;background:#C9A84C;top:0;bottom:0;left:50%;margin-left:-1.5px;}
    .item{padding:10px 40px;position:relative;width:50%;}
    .left{left:0;text-align:right;} .right{left:50%;text-align:left;}
    .content{padding:10px;background:rgba(255,255,255,0.1);border-radius:10px;color:white;}
    </style>
    <div class="timeline">
        <div class="item left"><div class="content"><b>2025-07-27</b><br>First Like on Story 🚌</div></div>
        <div class="item right"><div class="content"><b>2025-08-22</b><br>Official Couple 💜</div></div>
    </div>
    """, height=300)

with t4:
    t = st.text_input("Title")
    desc = st.text_area("Description")
    if st.button("Save Memory"): add_memory(t, desc, date.today(), "General", "💜"); st.rerun()
