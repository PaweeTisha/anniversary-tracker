import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date
import plotly.graph_objects as go
import base64

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Paweetida & Dawis 💜", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

# ---- CUSTOM CSS (AURORA THEME + SHOOTING STARS + FLOATING EMOJIS) ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&display=swap');

.stApp {
    background: linear-gradient(135deg, #050210 0%, #10072B 30%, #031B26 70%, #020C1B 100%);
    background-size: 400% 400%; animation: auroraFlow 15s ease infinite; min-height: 100vh; overflow-x: hidden;
}
@keyframes auroraFlow { 0% { background-position: 0% 50%; } 50% { background-position: 100% 50%; } 100% { background-position: 0% 50%; } }

.shooting-star { position: fixed; width: 2px; height: 2px; background: #00F5D4; border-radius: 50%; box-shadow: 0 0 10px 2px #00F5D4, 0 0 25px 6px #4CC9F0; animation: shootingStar linear infinite; z-index: 1; pointer-events: none; }
@keyframes shootingStar { 0% { transform: translateX(0) translateY(0); opacity: 1; } 100% { transform: translateX(-600px) translateY(600px); opacity: 0; } }

.floating-emoji { position: fixed; font-size: 1.5rem; animation: floatUp linear infinite; pointer-events: none; z-index: 1; opacity: 0.75; }
@keyframes floatUp { 0% { transform: translateY(100vh) rotate(0deg); opacity: 0; } 10% { opacity: 0.75; } 90% { opacity: 0.75; } 100% { transform: translateY(-10vh) rotate(360deg); opacity: 0; } }

.breaking-news-bar { background: linear-gradient(90deg, #8B0000, #00F5D4, #8B0000); border: 1px solid #FFD166; border-radius: 8px; padding: 0.5rem 1rem; color: #FFFFFF; font-weight: 700; font-size: 0.9rem; margin-bottom: 1.0rem; display: flex; align-items: center; gap: 12px; box-shadow: 0 0 25px rgba(0, 245, 212, 0.4); position: relative; z-index: 2; }
.breaking-badge { background: #FFFFFF; color: #8B0000; padding: 0.25rem 0.6rem; border-radius: 4px; font-size: 0.7rem; font-weight: 800; text-transform: uppercase; letter-spacing: 1px; white-space: nowrap; }
.hero-section { background: linear-gradient(135deg, rgba(123,44,191,0.6), rgba(0,245,212,0.25)); border-radius: 16px; padding: 1.2rem 1.5rem; text-align: center; border: 1px solid rgba(76,201,240,0.4); backdrop-filter: blur(12px); margin-bottom: 1rem; position: relative; z-index: 2; }
.section-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.1rem; font-weight: 600; color: #F0E9FA; border-bottom: 1px solid rgba(0,245,212,0.4); padding-bottom: 0.2rem; margin-bottom: 0.6rem; position: relative; z-index: 2; }
.memory-card { background: rgba(30, 15, 60, 0.8); border: 1px solid rgba(76,201,240,0.4); border-radius: 10px; padding: 0.8rem 1rem; margin-bottom: 0.5rem; position: relative; z-index: 2; }
.stButton button { background: linear-gradient(135deg, #7B2CBF, #00F5D4) !important; color: #0A041A !important; border: none; border-radius: 8px !important; font-weight: 700 !important; }
</style>

<script>
window.addEventListener('DOMContentLoaded', (event) => {
    // Shooting Stars
    for (let i = 0; i < 15; i++) {
        let star = document.createElement('div');
        star.className = 'shooting-star';
        star.style.top = Math.random() * 70 + 'vh';
        star.style.left = Math.random() * 100 + 'vw';
        star.style.animationDuration = (3 + Math.random() * 4) + 's';
        star.style.animationDelay = (Math.random() * 5) + 's';
        document.body.appendChild(star);
    }
    // Floating Emojis
    const emojis = ['💐','🍀','🪐','🌜','🌹','🌻','☃️','🌟','💜','💚','🌷','🌹','💙','❄️','⭐','🤍','☃️','💛','🧡','❤️','🌻','🍀','🌷','🌐','🌻','💻','📡','🛜','🍀','💜','🤍','❄️'];
    for (let i = 0; i < 15; i++) {
        let el = document.createElement('div');
        el.className = 'floating-emoji';
        el.textContent = emojis[Math.floor(Math.random() * emojis.length)];
        el.style.left = Math.random() * 100 + 'vw';
        el.style.animationDuration = (8 + Math.random() * 8) + 's';
        el.style.animationDelay = (Math.random() * 8) + 's';
        el.style.fontSize = (1 + Math.random() * 1.5) + 'rem';
        document.body.appendChild(el);
    }
});
</script>
""", unsafe_allow_html=True)

# ---- LOGIC & DATABASE (ย่อให้สั้น) ----
def init_db():
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, date TEXT, category TEXT, emoji TEXT, image_data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS milestones (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date TEXT, description TEXT, type TEXT, image_data TEXT)''')
    conn.commit(); conn.close()
init_db()

def check_password():
    if "authenticated" not in st.session_state: st.session_state.authenticated = False
    if "welcomed" not in st.session_state: st.session_state.welcomed = False

    if not st.session_state.authenticated:
        # หน้า LOGIN คลาสสิกเดิม
        components.html("""
        <!DOCTYPE html>
        <html>
        <head>
        <link href="https://fonts.googleapis.com/css2?family=Pacifico&display=swap" rel="stylesheet">
        <style>
        body { background: #0A041A; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; font-family: sans-serif; color: white; }
        .title { font-family: 'Pacifico', cursive; font-size: 3rem; margin-bottom: 2rem; }
        .pin-box { width: 45px; height: 55px; border: 2px solid #00F5D4; border-radius: 10px; background: #1E0B36; color: #FFD166; text-align: center; font-size: 1.5rem; }
        .enter-btn { background: #7B2CBF; color: white; border: none; border-radius: 10px; padding: 0.7rem 2rem; margin-top: 1rem; cursor: pointer; }
        </style>
        </head>
        <body>
            <div class="title">Paweetida & Dawis</div>
            <div id="pin-container"><input class="pin-box" maxlength="1" type="password" id="p0"><input class="pin-box" maxlength="1" type="password" id="p1"><input class="pin-box" maxlength="1" type="password" id="p2"><input class="pin-box" maxlength="1" type="password" id="p3"><input class="pin-box" maxlength="1" type="password" id="p4"><input class="pin-box" maxlength="1" type="password" id="p5"></div>
            <button class="enter-btn" onclick="checkPin()">Enter Our World 💜</button>
            <script>
            function checkPin() {
                let pin = Array.from(document.querySelectorAll('.pin-box')).map(b => b.value).join('');
                if (pin === '220825') {
                    const h = window.parent.document.querySelector('input[aria-label="hidden_pin"]');
                    h.value = pin; h.dispatchEvent(new Event('input', { bubbles: true }));
                }
            }
            </script>
        </body>
        </html>
        """, height=400)
        p = st.text_input("hidden_pin", type="password", key="pwd_backup", label_visibility="collapsed")
        if p == "220825": st.session_state.authenticated = True; st.rerun()
        return False

    # หน้า WELCOME (Say Hi ถึง Dawis ภาษาอังกฤษ กวนๆ)
    if not st.session_state.welcomed:
        components.html("""
        <!DOCTYPE html>
        <html>
        <head>
        <link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Plus+Jakarta+Sans:wght@600;700&display=swap" rel="stylesheet">
        <style>
        body { background: #0A041A; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: 'Plus Jakarta Sans', sans-serif; color: white; }
        .welcome-card { background: linear-gradient(135deg, #7B2CBF, #00F5D4); padding: 3rem; border-radius: 20px; text-align: center; max-width: 450px; }
        .explore-btn { background: #1E0B36; color: white; border: none; border-radius: 10px; padding: 1rem 2rem; margin-top: 2rem; cursor: pointer; }
        </style>
        </head>
        <body>
            <div class="welcome-card">
                <h1>Yo, Dawis! 👋</h1>
                <p>Don't get too excited, okay? I only built this website to level up my IT and Data Engineering skills! 55555</p>
                <button class="explore-btn" onclick="letMeIn()">Check out my coding skills! 🚀</button>
            </div>
            <script>
            function letMeIn() {
                const h = window.parent.document.querySelector('input[aria-label="hidden_welcome"]');
                h.value = 'done'; h.dispatchEvent(new Event('input', { bubbles: true }));
            }
            </script>
        </body>
        </html>
        """, height=600)
        w = st.text_input("hidden_welcome", key="welcome_backup", label_visibility="collapsed")
        if w == "done": st.session_state.welcomed = True; st.rerun()
        return False
    return True

if not check_password(): st.stop()

# (จากนั้นนำ Code ของ Tab ต่างๆ มาต่อด้านล่างได้เลยค่ะ)
