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
.hero-section { background: linear-gradient(135deg, rgba(123,44,191,0.6), rgba(0,245,212,0.25)); border-radius: 20px; padding: 1.5rem; text-align: center; border: 1px solid rgba(76,201,240,0.4); box-shadow: 0 0 35px rgba(0,245,212,0.25); }
.metric-card { background: linear-gradient(135deg, rgba(123,44,191,0.5), rgba(76,201,240,0.25)); border: 1px solid rgba(0,245,212,0.3); border-radius: 16px; padding: 1rem; text-align: center; }
.metric-number { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2.4rem; font-weight: 800; color: #FFD166; }
.stButton button { background: linear-gradient(135deg, #7B2CBF, #00F5D4) !important; color: #0A041A !important; border-radius: 12px !important; font-weight: 800 !important; padding: 0.6rem 1.5rem !important; }
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

# ---- AUTH (Clean HTML Login without trailing Streamlit inputs) ----
if not st.session_state.auth:
    login_code = st.text_input("code", type="password", label_visibility="collapsed")
    
    components.html("""
    <div style="text-align:center; padding:80px; color:white; font-family:sans-serif;">
        <h1 style="font-family:'Plus Jakarta Sans',sans-serif; color:#00F5D4; margin-bottom:20px;">Enter Secret Code</h1>
        <input type="password" id="p" placeholder="Enter code..." style="padding:12px 20px; border-radius:12px; border:2px solid #00F5D4; background:rgba(10,4,26,0.8); color:white; font-size:1.2rem; width:280px; outline:none; text-align:center;"><br><br>
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
            } else {
                alert('Wrong code, try again! 💜');
            }
        " style="background:linear-gradient(135deg, #7B2CBF, #00F5D4); color:#0A041A; border:none; border-radius:12px; padding:12px 35px; font-weight:800; font-size:1.1rem; cursor:pointer; box-shadow:0 0 15px rgba(0,245,212,0.4);">Enter Our World 💜</button>
    </div>
    """, height=350, scrolling=False)

    if login_code == "220825":
        st.session_state.auth = True
        st.session_state.view = "welcome"
        st.rerun()
    st.stop()

# ---- NAVIGATION ----
if st.session_state.view == "welcome":
    st.markdown("<h1 style='text-align:center; margin-top:50px;'>Welcome back, my favorite rival! 💜</h1>", unsafe_allow_html=True)
    col_w1, col_w2, col_w3 = st.columns([1, 2, 1])
    with col_w2:
        if st.button("💐 Get Flowers & Enter", use_container_width=True): 
            st.session_state.view = "menu"
            st.rerun()

elif st.session_state.view == "menu":
    st.markdown("<h1 style='text-align:center;'>Get Flowers! 🌷</h1>", unsafe_allow_html=True)
    st.markdown("""<div class='hero-section'>🌷🌻💐<br><br><b>For My Favorite Rival 😈</b><br><br>Thanks for sticking around, even when I'm moody! 555. Let's keep supporting each other for a long, long time. 💜</div>""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🍒 Journey & Stats", use_container_width=True): 
            st.session_state.view = "stats"
            st.rerun()
    with col2:
        if st.button("💌 Love Capsule", use_container_width=True): 
            st.session_state.view = "capsule"
            st.rerun()
    with col3:
        if st.button("⚔️ Battle Arena", use_container_width=True): 
            st.session_state.view = "battle"
            st.rerun()

elif st.session_state.view == "stats":
    st.write("## 📊 Our Journey & Stats")
    if st.button("← Back to Menu"): 
        st.session_state.view = "menu"
        st.rerun()

elif st.session_state.view == "capsule":
    st.write("## 💌 Love Capsule")
    if st.button("← Back to Menu"): 
        st.session_state.view = "menu"
        st.rerun()

elif st.session_state.view == "battle":
    st.write("## ⚔️ Battle Arena")
    if st.button("← Back to Menu"): 
        st.session_state.view = "menu"
        st.rerun()
