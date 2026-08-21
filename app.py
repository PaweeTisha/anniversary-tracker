import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date
import plotly.graph_objects as go
import base64

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Tisha & Dawis 💜", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

# (คง CSS เดิมไว้ทั้งหมด)
st.markdown("""
<style>
:root { --purple-deep: #3D1A6E; --purple-mid: #6B3FA0; --purple-light: #B08FD4; --gold: #C9A84C; }
* { font-family: 'DM Sans', sans-serif; }
.stApp { background: linear-gradient(135deg, #1A0A2E 0%, #2D1854 40%, #1E3A2A 100%); min-height: 100vh; }
.section-title { font-size: 1.2rem; font-weight: 700; color: #F0E9FA; margin-bottom: 1rem; border-bottom: 2px solid #C9A84C; padding-bottom: 0.5rem; }
</style>
""", unsafe_allow_html=True)

# (ฟังก์ชัน init_db, get_memories, add_memory, delete_memory, get_milestones, calculate_stats, check_password ไว้ที่เดิม)
# ... [เหมือนโค้ดเดิมทั้งหมด] ...

def init_db():
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, description TEXT, date TEXT NOT NULL, category TEXT, emoji TEXT, image_data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS milestones (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, date TEXT NOT NULL, description TEXT, type TEXT, image_data TEXT)''')
    conn.commit()
    conn.close()

def calculate_stats():
    today = date.today()
    official_date = date(2025, 8, 22)
    army_date = date(2026, 4, 20)
    return {"days_together": (today - official_date).days, "days_since_army": (today - army_date).days}

init_db()
stats = calculate_stats()

# ---- TABS (เพิ่ม ⚔️ Battle Phase) ----
tab_capsule, tab_battle, tab_stats, tab_memories, tab_timeline = st.tabs(["💌 Love Capsule", "⚔️ Battle Phase", "📊 Our Stats", "💜 Memories", "📸 Timeline"])

# ======== TAB: BATTLE PHASE (Tap/Untap Game) ========
with tab_battle:
    st.markdown('<div class="section-title">Battle Phase: Tap or Untap ⚔️</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#B08FD4;">Let\'s see if you can manage our resources! Tap the card to attack or Untap to prepare. 🃏</p>', unsafe_allow_html=True)
    
    components.html("""
    <div style="display: flex; gap: 20px; justify-content: center;">
        <div id="card" style="width: 150px; height: 210px; background: #C9A84C; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-weight: bold; cursor: pointer; transition: transform 0.3s; border: 4px solid #3D1A6E;">
            TAP ME!
        </div>
    </div>
    <div style="text-align: center; margin-top: 20px;" id="status">Status: Untapped</div>
    
    <script>
    let isTapped = false;
    const card = document.getElementById('card');
    const status = document.getElementById('status');
    card.onclick = () => {
        isTapped = !isTapped;
        card.style.transform = isTapped ? 'rotate(90deg)' : 'rotate(0deg)';
        status.innerText = isTapped ? 'Status: Tapped (Attacking!)' : 'Status: Untapped (Ready)';
    };
    </script>
    """, height=300)

# (ที่เหลือก็ใส่โค้ดหน้า Stats, Memories, Timeline เดิมต่อท้ายได้เลยค่ะ)
