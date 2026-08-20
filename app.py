import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date
import os
import base64

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Tisha & Dawis 💜", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

# ---- CUSTOM CSS & DB & STATS (เหมือนเดิม) ----
st.markdown("""<style>
.stApp { background: linear-gradient(135deg, #1A0A2E 0%, #2D1854 40%, #1E3A2A 100%); min-height: 100vh; }
.hero-section { background: rgba(61,26,110,0.6); border-radius: 20px; padding: 3rem 2rem; text-align: center; border: 1px solid rgba(176,143,212,0.3); backdrop-filter: blur(10px); margin-bottom: 2rem; }
.hero-title { font-family: 'Pacifico', cursive; font-size: 3rem; color: #F0E9FA; }
.section-title { font-size: 1.4rem; font-weight: 600; color: #F0E9FA; border-bottom: 1px solid #B08FD4; padding-bottom: 0.5rem; }
.memory-card { background: rgba(61,26,110,0.5); padding: 1rem; border-radius: 12px; margin-bottom: 0.75rem; }
</style>""", unsafe_allow_html=True)

def init_db():
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, date TEXT, category TEXT, emoji TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS milestones (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date TEXT, description TEXT, type TEXT)')
    conn.commit(); conn.close()

def calculate_stats():
    today = date.today(); official_date = date(2025, 8, 22)
    return {"days_together": (today - official_date).days}

# ---- LOGIN & PUZZLE (Full Version) ----
def main():
    if "auth" not in st.session_state: st.session_state.auth = False
    
    if not st.session_state.auth:
        st.markdown("<h1 style='text-align:center; color:#C9A84C'>Enter Secret Code 💜</h1>", unsafe_allow_html=True)
        code = st.text_input("Code", type="password", label_visibility="collapsed")
        if st.button("Enter"):
            if code == "220825": st.session_state.auth = True; st.rerun()
        st.stop()

    # เมื่อรหัสผ่านผ่านแล้ว
    init_db()
    stats = calculate_stats()
    
    # แสดงเมนูหลัก
    st.markdown(f"<div class='hero-section'><div class='hero-title'>Paweetida & Mr. Dawis</div></div>", unsafe_allow_html=True)
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Our Stats", "💜 Memories", "🗓️ Timeline", "➕ Add Memory"])
    
    with tab1:
        st.metric("Days Together", stats['days_together'])
    with tab2:
        st.subheader("Our Memories")
    with tab3:
        st.subheader("Timeline")
    with tab4:
        st.subheader("Add Memory")

if __name__ == "__main__":
    main()
