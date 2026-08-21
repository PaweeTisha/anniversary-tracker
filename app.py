import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import date
import plotly.graph_objects as go

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Paweetida & Dawis 💜", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

# ---- CSS STYLING ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700;800&family=DM+Sans:wght@400;500;700&display=swap');
.stApp { background: linear-gradient(135deg, #050210 0%, #10072B 30%, #031B26 70%, #020C1B 100%); color: #F0E9FA; }
.hero-section { background: linear-gradient(135deg, rgba(123,44,191,0.6), rgba(0,245,212,0.25)); border-radius: 20px; padding: 2rem; text-align: center; border: 1px solid rgba(76,201,240,0.4); box-shadow: 0 0 35px rgba(0,245,212,0.25); margin-bottom: 1.5rem; }
.stButton button { background: linear-gradient(135deg, #7B2CBF, #00F5D4) !important; color: #0A041A !important; border-radius: 12px !important; font-weight: 800 !important; padding: 1rem !important; width: 100% !important; border: none !important; }
</style>
""", unsafe_allow_html=True)

# ---- DATABASE ----
def init_db():
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute("DROP TABLE IF EXISTS milestones")
    c.execute('''CREATE TABLE milestones (title TEXT, date TEXT)''')
    data = [("First Liked Story ✨", "2025-07-27"), ("Official Anniversary 🎉", "2025-08-22"), ("NZ Trip 🏔️", "2026-03-29"), ("Army 🪖", "2026-04-20"), ("1st Anniv 2026 🎉", "2026-08-22")]
    c.executemany("INSERT INTO milestones VALUES (?,?)", data)
    conn.commit(); conn.close()

init_db()

# ---- SESSION STATE ----
if "auth" not in st.session_state: st.session_state.auth = False
if "view" not in st.session_state: st.session_state.view = "login"

# ---- AUTH & WELCOME FLOW ----
if not st.session_state.auth:
    components.html("""
    <div style="text-align:center; padding:100px; color:white; font-family:sans-serif;">
        <h1 style="color:#00F5D4;">Enter Secret Code</h1>
        <input type="password" id="p" style="padding:10px; border-radius:10px; border:none; width:300px;"><br><br>
        <button onclick="
            let val = document.getElementById('p').value;
            if(val == '220825') {
                const parentDoc = window.parent.document;
                const inputs = parentDoc.querySelectorAll('input[type=password]');
                inputs.forEach(input => {
                    let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                    nativeSetter.call(input, '220825');
                    input.dispatchEvent(new Event('input', {bubbles: true}));
                });
            }" style="padding:10px 30px; border-radius:10px; cursor:pointer;">Enter</button>
    </div>
    """, height=400)
    if st.text_input("code", type="password", label_visibility="collapsed") == "220825":
        st.session_state.auth = True; st.session_state.view = "welcome"; st.rerun()
    st.stop()

if st.session_state.view == "welcome":
    st.markdown("<h1 style='text-align:center;'>Welcome back, favorite rival! 💜</h1>", unsafe_allow_html=True)
    if st.button("💐 Get Flowers & Enter"): st.session_state.view = "menu"; st.rerun()

# ---- MENU ----
elif st.session_state.view == "menu":
    st.markdown("<h1 style='text-align:center;'>Get Flowers! 🌷</h1>", unsafe_allow_html=True)
    st.markdown("""<div class='hero-section'><img src='https://images.unsplash.com/photo-1526047932273-341f2a7631f9?w=400' style='width:200px; border-radius:50%; border:4px solid #FFD166;'><br><br><b>For My Favorite Rival 😈</b><br><br>Thanks for sticking around, even when I'm moody! 555. Let's keep supporting each other for a long time. 💜</div>""", unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns(3)
    with c1: 
        if st.button("🍒 Journey & Stats"): st.session_state.view = "stats"; st.rerun()
    with c2: 
        if st.button("💌 Love Capsule"): st.session_state.view = "capsule"; st.rerun()
    with c3: 
        if st.button("⚔️ Battle Arena"): st.session_state.view = "battle"; st.rerun()

# ---- FEATURES ----
elif st.session_state.view == "stats":
    st.write("## 📊 Our Journey & Stats")
    today = date.today(); official_date = date(2025, 8, 22); diff = (today - official_date).days
    st.markdown(f"<div class='hero-section'><h1>{diff} Days Together</h1></div>", unsafe_allow_html=True)
    if st.button("← Back to Menu"): st.session_state.view = "menu"; st.rerun()

elif st.session_state.view == "capsule":
    st.write("## 💌 Love Capsule")
    if st.button("Open Secret Note"): st.success("The moon is beautiful, isn't it? 💜")
    if st.button("← Back to Menu"): st.session_state.view = "menu"; st.rerun()

elif st.session_state.view == "battle":
    st.write("## ⚔️ Battle Arena")
    st.write("Duel mode activated!")
    if st.button("← Back to Menu"): st.session_state.view = "menu"; st.rerun()
