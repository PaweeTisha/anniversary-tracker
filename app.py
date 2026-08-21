import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date
import base64

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Paweetida & Dawis 💜", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

# ---- CSS: AURORA THEME + SHOOTING STARS + HIDE INPUTS ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&display=swap');
.stApp { background: linear-gradient(135deg, #050210 0%, #10072B 30%, #031B26 70%, #020C1B 100%); min-height: 100vh; }
div[data-testid="stTextInput"]:has(input[aria-label="hidden_welcome"]),
div[data-testid="stTextInput"]:has(input[aria-label="hidden_pin"]) { display: none !important; }
.hero-section { background: linear-gradient(135deg, rgba(123,44,191,0.6), rgba(0,245,212,0.25)); border-radius: 16px; padding: 1.5rem; text-align: center; border: 1px solid rgba(76,201,240,0.4); backdrop-filter: blur(12px); margin-bottom: 1.5rem; color: #F0E9FA; }
.section-title { font-size: 1.2rem; font-weight: 700; color: #FFD166; margin-bottom: 1rem; border-bottom: 1px solid #00F5D4; padding-bottom: 0.3rem; }
.memory-card { background: rgba(30, 15, 60, 0.8); border: 1px solid rgba(76,201,240,0.3); border-radius: 12px; padding: 1rem; margin-bottom: 0.8rem; }
</style>
""", unsafe_allow_html=True)

# ---- DATABASE ----
def init_db():
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, date TEXT, category TEXT, emoji TEXT, image_data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS milestones (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date TEXT, description TEXT, type TEXT, image_data TEXT)''')
    conn.commit(); conn.close()

init_db()

# ---- LOGIN & WELCOME LOGIC ----
if "authenticated" not in st.session_state: st.session_state.authenticated = False
if "welcomed" not in st.session_state: st.session_state.welcomed = False

if not st.session_state.authenticated:
    components.html("""
    <script>
    function checkPin() {
        let pin = Array.from(document.querySelectorAll('.pin-box')).map(b => b.value).join('');
        if (pin === '220825') {
            const hidden = window.parent.document.querySelector('input[aria-label="hidden_pin"]');
            let setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
            setter.call(hidden, pin);
            hidden.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }
    </script>
    <div style="text-align:center; color:white; font-family: sans-serif;">
        <h1>Paweetida & Dawis</h1>
        <input type="password" id="p0" maxlength="1" class="pin-box" style="width:40px;height:50px;text-align:center;font-size:20px;">
        <input type="password" id="p1" maxlength="1" class="pin-box" style="width:40px;height:50px;text-align:center;font-size:20px;">
        <input type="password" id="p2" maxlength="1" class="pin-box" style="width:40px;height:50px;text-align:center;font-size:20px;">
        <input type="password" id="p3" maxlength="1" class="pin-box" style="width:40px;height:50px;text-align:center;font-size:20px;">
        <input type="password" id="p4" maxlength="1" class="pin-box" style="width:40px;height:50px;text-align:center;font-size:20px;">
        <input type="password" id="p5" maxlength="1" class="pin-box" style="width:40px;height:50px;text-align:center;font-size:20px;">
        <br><button onclick="checkPin()" style="margin-top:10px; padding:10px 20px;">Enter</button>
    </div>
    """, height=400)
    if st.text_input("hidden_pin", type="password", key="pwd") == "220825":
        st.session_state.authenticated = True; st.rerun()
    st.stop()

if not st.session_state.welcomed:
    components.html("""
    <div style="background:linear-gradient(135deg, #7B2CBF, #00F5D4); color:white; padding:40px; border-radius:20px; text-align:center;">
        <h1>¡Buenos, Dawis!</h1>
        <p>⚠️ Watch out for scammers! Anyway, luv u tho 💜</p>
        <button onclick="letMeIn()" style="padding:15px 30px; font-weight:bold;">Check my skills!</button>
    </div>
    <script>
    function letMeIn() {
        const hidden = window.parent.document.querySelector('input[aria-label="hidden_welcome"]');
        let setter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
        setter.call(hidden, 'done');
        hidden.dispatchEvent(new Event('input', { bubbles: true }));
    }
    </script>
    """, height=400)
    if st.text_input("hidden_welcome", key="welcome") == "done":
        st.session_state.welcomed = True; st.rerun()
    st.stop()

# ---- MAIN TABS ----
tab1, tab2, tab3 = st.tabs(["📊 Our Stats", "⚔️ Battle Phase", "📸 Timeline"])

with tab1:
    st.markdown('<div class="hero-section"><h2>Our journey started 27 Jul 2025 (first liked my IG story ✨)</h2></div>', unsafe_allow_html=True)
with tab2:
    st.write("Battle active...")
with tab3:
    st.markdown('<div class="section-title">Timeline Scrapbook</div>', unsafe_allow_html=True)
    memories = get_memories()
    for _, row in memories.iterrows():
        st.markdown(f'<div class="memory-card"><b>{row["title"]}</b><br>{row["description"]}</div>', unsafe_allow_html=True)
