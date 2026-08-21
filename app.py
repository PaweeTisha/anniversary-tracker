import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date
import plotly.graph_objects as go
import base64

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Paweetida & Dawis 💜", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

# ---- CUSTOM CSS (AURORA THEME + GLOBAL SHOOTING STARS) ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&display=swap');

:root {
    --aurora-purple: #4A154B;
    --aurora-violet: #7B2CBF;
    --aurora-green: #00F5D4;
    --aurora-cyan: #4CC9F0;
    --aurora-dark: #0A041A;
    --gold: #FFD166;
}

* { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #050210 0%, #10072B 30%, #031B26 70%, #020C1B 100%);
    background-size: 400% 400%;
    animation: auroraFlow 15s ease infinite;
    min-height: 100vh;
    position: relative;
    overflow-x: hidden;
}

@keyframes auroraFlow {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}

.stApp::before {
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(0,245,212,0.12) 0%, rgba(76,201,240,0.08) 30%, transparent 70%);
    animation: auroraShimmer 10s ease-in-out infinite alternate;
    pointer-events: none;
    z-index: 0;
}

@keyframes auroraShimmer {
    0% { transform: translateY(-20px) scale(1); opacity: 0.6; }
    100% { transform: translateY(20px) scale(1.1); opacity: 1; }
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1250px !important;
    position: relative;
    z-index: 1;
}

@keyframes shootingStar {
    0% { transform: translateX(0) translateY(0); opacity: 1; }
    100% { transform: translateX(-600px) translateY(600px); opacity: 0; }
}

.shooting-star {
    position: fixed;
    width: 2px;
    height: 2px;
    background: #00F5D4;
    border-radius: 50%;
    box-shadow: 0 0 10px 2px #00F5D4, 0 0 25px 6px #4CC9F0;
    animation: shootingStar linear infinite;
    z-index: 1;
    pointer-events: none;
}

.breaking-news-bar {
    background: linear-gradient(90deg, #8B0000, #00F5D4, #8B0000);
    border: 1px solid #FFD166;
    border-radius: 8px;
    padding: 0.5rem 1rem;
    color: #FFFFFF;
    font-weight: 700;
    font-size: 0.9rem;
    margin-bottom: 1.0rem;
    display: flex;
    align-items: center;
    gap: 12px;
    box-shadow: 0 0 25px rgba(0, 245, 212, 0.4);
    position: relative;
    z-index: 2;
}
.breaking-badge {
    background: #FFFFFF;
    color: #8B0000;
    padding: 0.25rem 0.6rem;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 1px;
    white-space: nowrap;
    animation: pulse 1.5s infinite;
}
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

.hero-section {
    background: linear-gradient(135deg, rgba(123,44,191,0.6), rgba(0,245,212,0.25));
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    border: 1px solid rgba(76,201,240,0.4);
    backdrop-filter: blur(12px);
    margin-bottom: 1rem;
    box-shadow: 0 0 35px rgba(0,245,212,0.25);
    position: relative;
    z-index: 2;
}

.hero-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2rem; font-weight: 700; color: #F0E9FA; margin: 0; }
.hero-subtitle { font-size: 0.8rem; color: #4CC9F0; margin-top: 0.2rem; letter-spacing: 1.5px; text-transform: uppercase; }

.metric-card {
    background: linear-gradient(135deg, rgba(123,44,191,0.5), rgba(76,201,240,0.25));
    border: 1px solid rgba(0,245,212,0.3);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    backdrop-filter: blur(8px);
    position: relative;
    z-index: 2;
    box-shadow: 0 0 15px rgba(123,44,191,0.2);
}

.metric-number { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2.4rem; font-weight: 700; color: #FFD166; line-height: 1; }
.metric-label { font-size: 0.75rem; color: #4CC9F0; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.3rem; }

.section-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #F0E9FA;
    margin-bottom: 0.6rem;
    border-bottom: 1px solid rgba(0,245,212,0.4);
    padding-bottom: 0.2rem;
    position: relative;
    z-index: 2;
}

.memory-card {
    background: rgba(30, 15, 60, 0.8);
    border: 1px solid rgba(76,201,240,0.4);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
    position: relative;
    z-index: 2;
}

.army-badge {
    background: linear-gradient(135deg, rgba(0,245,212,0.35), rgba(76,201,240,0.25));
    border: 1px solid rgba(0,245,212,0.6);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    color: #E8EDE4;
    box-shadow: 0 0 20px rgba(0,245,212,0.3);
    position: relative;
    z-index: 2;
}

.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: rgba(30, 15, 60, 0.85) !important;
    border: 1px solid rgba(76,201,240,0.5) !important;
    color: #F0E9FA !important;
    border-radius: 8px !important;
}

.stButton button {
    background: linear-gradient(135deg, #7B2CBF, #00F5D4) !important;
    color: #0A041A !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
    padding: 0.4rem 1.2rem !important;
    box-shadow: 0 0 20px rgba(0,245,212,0.5);
}

.stTabs [data-baseweb="tab"] { color: #4CC9F0 !important; z-index: 2; }
.stTabs [aria-selected="true"] { color: #00F5D4 !important; border-bottom: 2px solid #FFD166 !important; }
</style>

<script>
window.addEventListener('DOMContentLoaded', (event) => {
    for (let i = 0; i < 18; i++) {
        let star = document.createElement('div');
        star.className = 'shooting-star';
        star.style.top = Math.random() * 70 + 'vh';
        star.style.left = Math.random() * 100 + 'vw';
        star.style.animationDuration = (2 + Math.random() * 4) + 's';
        star.style.animationDelay = (Math.random() * 5) + 's';
        document.body.appendChild(star);
    }
});
</script>
""", unsafe_allow_html=True)

# ---- DATABASE & IMAGE SUPPORT ----
def init_db():
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memories (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        description TEXT,
        date TEXT NOT NULL,
        category TEXT DEFAULT 'memory',
        emoji TEXT DEFAULT '💜',
        image_data TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS milestones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        type TEXT DEFAULT 'milestone',
        image_data TEXT
    )''')
    
    try:
        c.execute("ALTER TABLE memories ADD COLUMN image_data TEXT")
    except:
        pass
    try:
        c.execute("ALTER TABLE milestones ADD COLUMN image_data TEXT")
    except:
        pass

    c.execute("SELECT COUNT(*) FROM milestones")
    if c.fetchone()[0] == 0:
        default_milestones = [
            ("First Like on Story 🚌", "2025-07-27", "The day you liked my story on the bus", "start"),
            ("Official Couple 💜", "2025-08-22", "The day we became official", "anniversary"),
            ("Dawis Enlists Army 🪖", "2026-04-20", "Dawis joined the Australian Army", "milestone"),
        ]
        c.executemany("INSERT INTO milestones (title, date, description, type) VALUES (?,?,?,?)", default_milestones)
    conn.commit()
    conn.close()

def get_memories():
    conn = sqlite3.connect('anniversary.db')
    df = pd.read_sql_query("SELECT * FROM memories ORDER BY date DESC", conn)
    conn.close()
    return df

def add_memory(title, description, date_val, category, emoji, image_data):
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute("INSERT INTO memories (title, description, date, category, emoji, image_data) VALUES (?,?,?,?,?,?)",
              (title, description, str(date_val), category, emoji, image_data))
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
    start_date = date(2025, 7, 27)
    official_date = date(2025, 8, 22)
    army_date = date(2026, 4, 20)
    next_anniversary = date(2026, 8, 22)
    if today > next_anniversary:
        next_anniversary = date(today.year + 1, 8, 22)

    return {
        "days_since_first": (today - start_date).days,
        "days_together": (today - official_date).days,
        "weeks_together": (today - official_date).days // 7,
        "months_together": (today - official_date).days // 30,
        "days_to_anniversary": (next_anniversary - today).days,
        "days_since_army": (today - army_date).days if today >= army_date else 0,
        "next_anniversary": next_anniversary,
    }

# ---- PASSWORD LOGIN (With Shooting Stars & Floating Emojis) ----
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "welcomed" not in st.session_state:
        st.session_state.welcomed = False

    if not st.session_state.authenticated:
        st.markdown("""
        <style>
        .block-container { padding-top: 1rem !important; padding-bottom: 1rem !important; max-width: 100% !important; }
        div[data-testid="stTextInput"] { position: absolute !important; width: 0px !important; height: 0px !important; opacity: 0 !important; z-index: -9999 !important; }
        </style>
        """, unsafe_allow_html=True)
        components.html("""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: transparent; min-height: 100vh; display: flex; flex-direction: column; align-items: center; justify-content: center; font-family: 'Plus Jakarta Sans', sans-serif; text-align: center; padding: 1rem; overflow: hidden; }
@keyframes shootingStar { 0% { transform: translateX(0) translateY(0); opacity: 1; } 100% { transform: translateX(-500px) translateY(500px); opacity: 0; } }
.login-star { position: fixed; width: 2px; height: 2px; background: #00F5D4; border-radius: 50%; box-shadow: 0 0 8px #00F5D4; animation: shootingStar linear infinite; }
.floating-emoji { position: fixed; font-size: 1.5rem; animation: floatUp linear infinite; pointer-events: none; opacity: 0.7; }
@keyframes floatUp { 0% { transform: translateY(100vh) rotate(0deg); opacity: 0; } 50% { opacity: 0.7; } 100% { transform: translateY(-10vh) rotate(360deg); opacity: 0; } }
.chars { display: flex; justify-content: center; align-items: center; gap: 1.5rem; margin-bottom: 1rem; }
.girl { font-size: 4rem; animation: bounce 1.4s ease-in-out infinite; }
.heart { font-size: 2.8rem; animation: heartbeat 1.2s ease-in-out infinite; }
.soldier { font-size: 4rem; animation: bounce2 1.6s ease-in-out infinite; }
.title { font-family: 'Pacifico', cursive; font-size: 3.2rem; background: linear-gradient(135deg, #00F5D4, #FFD166); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.pin-section { margin-top: 1.5rem; background: rgba(30, 15, 60, 0.75); border: 2px solid #00F5D4; border-radius: 20px; padding: 1.5rem 2rem; max-width: 400px; width: 100%; backdrop-filter: blur(10px); }
.pin-box { width: 45px; height: 55px; border: 2px solid #00F5D4; border-radius: 10px; background: rgba(10,4,26,0.6); color: #FFD166; text-align: center; font-size: 1.5rem; }
.enter-btn { background: linear-gradient(135deg, #7B2CBF, #00F5D4); color: #0A041A; border: none; border-radius: 10px; padding: 0.7rem 2rem; font-weight: 700; cursor: pointer; }
</style>
</head>
<body>
    <script>
    for (let i = 0; i < 15; i++) {
        let s = document.createElement('div'); s.className = 'login-star'; s.style.top = Math.random()*60+'vh'; s.style.left = Math.random()*100+'vw'; s.style.animationDuration = (2+Math.random()*3)+'s'; document.body.appendChild(s);
    }
    const e = ['💐','🍀','🪐','🌜','🌹','🌻','☃️','🌟','💜','💚','🌷','🌹','💙','❄️','⭐','🤍','☃️','💛','🧡','❤️','🌻','🍀','🌷','🌐','💻','📡','🛜','🪖'];
    for (let i = 0; i < 20; i++) {
        let el = document.createElement('div'); el.className = 'floating-emoji'; el.textContent = e[Math.floor(Math.random()*e.length)]; el.style.left = Math.random()*100+'vw'; el.style.animationDuration = (5+Math.random()*8)+'s'; document.body.appendChild(el);
    }
    </script>
    <div class="chars"><span class="girl">💻</span><span class="heart">💜</span><span class="soldier">🪖</span></div>
    <div class="title">Paweetida & Dawis</div>
    <div class="pin-section">
        <div class="pin-boxes"><input class="pin-box" maxlength="1" type="password" id="p0" inputmode="numeric"><input class="pin-box" maxlength="1" type="password" id="p1" inputmode="numeric"><input class="pin-box" maxlength="1" type="password" id="p2" inputmode="numeric"><input class="pin-box" maxlength="1" type="password" id="p3" inputmode="numeric"><input class="pin-box" maxlength="1" type="password" id="p4" inputmode="numeric"><input class="pin-box" maxlength="1" type="password" id="p5" inputmode="numeric"></div>
        <button class="enter-btn" onclick="checkPin()">Enter Our World 💜</button>
    </div>
    <script>
    const boxes = document.querySelectorAll('.pin-box'); boxes[0].focus(); boxes.forEach((b,i) => { b.addEventListener('input', (e) => { if(b.value && i<5) boxes[i+1].focus(); }); });
    function checkPin() {
        let pin = Array.from(boxes).map(b => b.value).join('');
        if (pin === '220825') {
            const parentDoc = window.parent.document;
            const hiddenInput = parentDoc.querySelector('input[aria-label="hidden_pin"]');
            if (hiddenInput) {
                let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                nativeSetter.call(hiddenInput, pin);
                hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
                hiddenInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', bubbles: true }));
            }
        }
    }
    </script>
</body>
</html>
""", height=720, scrolling=False)
        password = st.text_input("hidden_pin", type="password", key="pwd_backup", label_visibility="collapsed")
        if password == "220825":
            st.session_state.authenticated = True
            st.rerun()
        return False

    if not st.session_state.welcomed:
        components.html("""
        <!DOCTYPE html>
        <html>
        <head>
        <link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Plus+Jakarta+Sans:wght@600;700&display=swap" rel="stylesheet">
        <style>
        body { background: transparent; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: 'Plus Jakarta Sans', sans-serif; }
        .welcome-card { background: linear-gradient(135deg, rgba(123,44,191,0.85), rgba(0,245,212,0.6)); border: 2px solid #FFD166; border-radius: 28px; padding: 3rem 2.5rem; text-align: center; max-width: 450px; width: 90%; box-shadow: 0 0 50px rgba(0,245,212,0.5); color: #FFFFFF; }
        .welcome-title { font-family: 'Pacifico', cursive; font-size: 2.5rem; color: #FFD166; margin-bottom: 0.5rem; }
        .explore-btn { background: linear-gradient(135deg, #FFD166, #00F5D4); color: #0A041A; border: none; border-radius: 14px; padding: 0.85rem 2.5rem; font-weight: 700; cursor: pointer; }
        </style>
        </head>
        <body>
            <div class="welcome-card">
                <div style="font-size: 3.5rem;">💻✨😏</div>
                <div class="welcome-title">Yo, Dawis!</div>
                <p>บอกก่อนนะ... ที่นั่งทำเว็บนี้ขึ้นมา ไม่ใช่เพราะรักเธอมากหรอก! ก็แค่... อยากฝึกสกิล IT พัฒนาทักษะ Data Engineering ของตัวเองเฉยๆ หรอกน่า! 55555</p>
                <button class="explore-btn" onclick="letMeIn()">Go check my coding skills! 🚀</button>
            </div>
            <script>
            function letMeIn() {
                const parentDoc = window.parent.document;
                const hiddenInput = parentDoc.querySelector('input[aria-label="hidden_welcome"]');
                if (hiddenInput) {
                    let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                    nativeSetter.call(hiddenInput, 'done');
                    hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
                    hiddenInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', bubbles: true }));
                }
            }
            </script>
        </body>
        </html>
        """, height=700, scrolling=False)
        welcome_trigger = st.text_input("hidden_welcome", key="welcome_backup", label_visibility="collapsed")
        if welcome_trigger == "done":
            st.session_state.welcomed = True
            st.rerun()
        return False
    return True

if not check_password():
    st.stop()

# ---- BREAKING NEWS POPUP ----
components.html("""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
<style>
.news-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(10,4,26,0.85); backdrop-filter: blur(8px); display: flex; justify-content: center; align-items: center; z-index: 99999; }
.news-modal { background: linear-gradient(135deg, #8B0000, #1E0B36); border: 3px solid #00F5D4; border-radius: 20px; padding: 2rem; max-width: 420px; width: 90%; text-align: center; color: #FFFFFF; box-shadow: 0 0 40px rgba(0,245,212,0.4); animation: popUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
@keyframes popUp { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
.news-header { background: #00F5D4; color: #0A041A; font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.7rem; font-weight: 700; padding: 0.3rem 0.8rem; border-radius: 4px; display: inline-block; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.6rem; white-space: nowrap; }
.news-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.3rem; font-weight: 700; margin-bottom: 0.5rem; color: #FFD166; }
.news-desc { font-size: 0.9rem; line-height: 1.4; margin-bottom: 1.2rem; color: #F0E9FA; font-weight: 500; }
.warning-box { background: rgba(0, 245, 212, 0.15); border: 2px dashed #00F5D4; border-radius: 10px; padding: 0.7rem; margin-bottom: 1.2rem; color: #00F5D4; font-weight: 700; font-size: 0.85rem; }
.ack-btn { background: linear-gradient(135deg, #7B2CBF, #00F5D4); color: #0A041A; border: none; border-radius: 10px; padding: 0.6rem 1.8rem; font-weight: 700; font-size: 0.9rem; cursor: pointer; box-shadow: 0 0 15px rgba(0,245,212,0.4); transition: transform 0.2s; }
.ack-btn:hover { transform: scale(1.05); }
</style>
</head>
<body>
<div class="news-overlay" id="newsModal">
    <div class="news-modal">
        <div class="news-header">🚨 BREAKING NEWS 🚨</div>
        <div class="news-title">Upcoming Anniversary Alert! 💜</div>
        <div class="news-desc">
            Get ready for special dates, love capsules, and epic card duels!
        </div>
        <div class="warning-box">
            ⚠️ WARNING: DO NOT FORGET OUR SPECIAL DATE! DO NOT MISS IT! 🚨🔥
        </div>
        <button class="ack-btn" onclick="closeNews()">Acknowledge & Enter 🚀</button>
    </div>
</div>
<script>
function closeNews() {
    document.getElementById('newsModal').style.display = 'none';
}
</script>
</body>
</html>
""", height=330, scrolling=False)

# ---- INIT & STATS ----
init_db()
stats = calculate_stats()

# ---- BREAKING NEWS TICKER BANNER ----
st.markdown("""
<div class="breaking-news-bar">
    <div class="breaking-badge">🔴 BREAKING NEWS</div>
    <div style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: #FFFFFF; font-weight: 700;">
        ⚠️ WARNING: DO NOT FORGET OUR SPECIAL ANNIVERSARY! Stay tuned for card duels and memories! 💜🪖
    </div>
</div>
""", unsafe_allow_html=True)

# ---- TABS ----
tab_capsule, tab_battle, tab_stats, tab_memories, tab_timeline, tab_add = st.tabs(["💌 Love Capsule", "⚔️ Battle Phase", "📊 Our Stats", "💜 Memories", "📸 Timeline", "➕ Add Memory"])

# ======== TAB 0: LOVE CAPSULE ========
with tab_capsule:
    st.markdown('<div class="section-title">Love Capsule — Open a Secret Note 💌</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #4CC9F0; font-size: 0.9rem; margin-bottom: 1.5rem;">Pick a letter to reveal a supportive message or a playful tease from your favorite rival! ✨</div>', unsafe_allow_html=True)
    
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
    <style>
    body { background: transparent; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: 'DM Sans', sans-serif; }
    .capsule-container { text-align: center; max-width: 360px; width: 100%; background: linear-gradient(135deg, rgba(123,44,191,0.6), rgba(0,245,212,0.2)); border: 1px solid rgba(0,245,212,0.4); border-radius: 24px; padding: 2rem; backdrop-filter: blur(12px); box-shadow: 0 0 30px rgba(123,44,191,0.3); }
    .letter-icon { font-size: 4.5rem; animation: floatLetter 2.5s ease-in-out infinite; margin-bottom: 0.8rem; filter: drop-shadow(0 0 15px rgba(0,245,212,0.5)); }
    @keyframes floatLetter { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
    .open-btn { background: linear-gradient(135deg, #7B2CBF, #00F5D4); color: #0A041A; border: none; border-radius: 14px; padding: 0.8rem 2rem; font-size: 1rem; font-weight: 700; cursor: pointer; box-shadow: 0 0 15px rgba(0,245,212,0.4); transition: all 0.2s; }
    .open-btn:hover { transform: scale(1.06); background: linear-gradient(135deg, #9D4EDD, #4CC9F0); }
    
    .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(10,4,26,0.5); backdrop-filter: blur(4px); justify-content: center; align-items: center; z-index: 999; }
    .modal-content { background: #1E0B36; color: #00F5D4; padding: 2.4rem 2rem; border-radius: 24px; text-align: center; max-width: 330px; width: 90%; box-shadow: 0 0 40px rgba(0,245,212,0.4); border: 2px solid #00F5D4; animation: popUp 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); position: relative; }
    @keyframes popUp { 0% { transform: scale(0.6); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
    .msg-box { font-size: 1.05rem; font-weight: 700; color: #F0E9FA; margin: 1.2rem 0; line-height: 1.5; }
    .close-btn { background: linear-gradient(135deg, #7B2CBF, #00F5D4); color: #0A041A; border: none; border-radius: 12px; padding: 0.65rem 2rem; font-weight: 700; font-size: 0.95rem; cursor: pointer; transition: transform 0.2s; box-shadow: 0 0 15px rgba(0,245,212,0.4); }
    .close-btn:hover { transform: scale(1.05); }
    </style>
    </head>
    <body>
    <div class="capsule-container">
        <div class="letter-icon">✉️</div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif; color:#FFD166; font-size:1.3rem; font-weight:700; margin-bottom:0.3rem;">Love Capsule Letter</div>
        <div style="color:#4CC9F0; font-size:0.75rem; margin-bottom:1.5rem; letter-spacing:0.5px;">Open a note from me ✨</div>
        <button class="open-btn" onclick="openLetter()">Open Letter 💌</button>
    </div>

    <div class="modal" id="modal">
        <div class="modal-content">
            <div style="font-size: 2.2rem;">💌</div>
            <div style="font-size:0.7rem; color:#4CC9F0; text-transform:uppercase; font-weight:700; letter-spacing:1.5px; margin-top:0.4rem;" id="modalSub">Secret Note Unlocked</div>
            <div class="msg-box" id="secretMsg">...</div>
            <button class="close-btn" onclick="closeModal()">Got it</button>
        </div>
    </div>

    <script>
    const messages = [
        "I love you so much! Keep crushing your goals, my favorite rival!",
        "¡Muchísima suerte hoy! You are going to do amazing things, my favorite rival.",
        "I admire you so much. Proud of you every single day, soldier!",
        "¡Eres el mejor! Even if you are a stubborn little trouble-maker.",
        "Everything is going to be amazing. Sending you all my love and energy!",
        "You and me make an unstoppable team. I am definitely the smart one here.",
        "Have an incredible day! Sending you a giant hug and all my support.",
        "No matter how tough it gets, I have your back forever. Let us conquer it all!",
        "I love you a lot! Now go ace it so I can proudly brag about you.",
        "A triunfar hoy. But always remember who is actually in charge here.",
        "So proud of the hard worker you are. You are truly incredible, my love!",
        "Warning: High level of cuteness and unstoppable support coming your way!",
        "Go get them, soldier! Make me proud today and always.",
        "You are my favorite distraction and my greatest motivation. I love you!"
    ];

    function openLetter() {
        const randomMsg = messages[Math.floor(Math.random() * messages.length)];
        document.getElementById('secretMsg').innerText = randomMsg;
        document.getElementById('modalSub').innerText = "Secret Note Unlocked";
        document.getElementById('modal').style.display = 'flex';
    }

    function closeModal() {
        document.getElementById('modal').style.display = 'none';
    }
    </script>
    </body>
    </html>
    """, height=380, scrolling=False)

# ======== TAB 1: BATTLE PHASE ========
with tab_battle:
    st.markdown('<div class="section-title">Battle Phase: 5 Cards Choice & Tap/Untap ⚔️🃏</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #4CC9F0; font-size: 0.9rem; margin-bottom: 1.0rem;">Pick one of 5 cards every turn, then Tap to attack/heal! First to 0 HP loses. ✨</div>', unsafe_allow_html=True)
    
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
    <style>
    body { background: transparent; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: 'DM Sans', sans-serif; }
    .duel-arena { text-align: center; background: rgba(30,15,60,0.75); border: 1px solid rgba(0,245,212,0.4); border-radius: 20px; padding: 1.2rem 1.5rem; backdrop-filter: blur(12px); box-shadow: 0 0 30px rgba(123,44,191,0.4); max-width: 560px; width: 100%; position: relative; }
    
    /* Picker Phase */
    #pickerPhase { display: block; }
    .card-options { display: flex; justify-content: center; gap: 8px; margin: 0.6rem 0; flex-wrap: wrap; }
    .option-card {
        width: 95px; height: 130px;
        background: linear-gradient(135deg, #7B2CBF, #1E0B36);
        border: 2px solid #00F5D4; border-radius: 8px;
        display: flex; flex-direction: column; align-items: center; justify-content: center;
        cursor: pointer; transition: transform 0.2s; padding: 6px; color: #F0E9FA;
        box-shadow: 0 0 10px rgba(0,245,212,0.2);
    }
    .option-card:hover { transform: translateY(-5px) scale(1.05); border-color: #FFD166; box-shadow: 0 0 15px rgba(255,209,102,0.4); }
    
    /* Battle Phase */
    #battlePhase { display: none; }
    .players-container { display: flex; justify-content: space-around; align-items: center; gap: 15px; margin-bottom: 0.8rem; }
    .player-box { background: rgba(10,4,26,0.7); border: 2px solid rgba(0,245,212,0.3); border-radius: 14px; padding: 0.8rem; width: 48%; text-align: center; transition: all 0.3s; }
    .player-box.active-turn { border-color: #FFD166; box-shadow: 0 0 20px rgba(255,209,102,0.6); background: rgba(123,44,191,0.4); }
    
    .player-name { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 0.85rem; color: #FFD166; font-weight: 700; margin-bottom: 0.3rem; }
    .hp-text { font-size: 0.8rem; color: #F0E9FA; font-weight: 600; margin-bottom: 0.6rem; }
    
    .card-container { perspective: 1000px; display: inline-block; cursor: pointer; }
    .mtg-card { 
        width: 110px; height: 150px; 
        background: linear-gradient(135deg, #7B2CBF, #1E0B36); 
        border: 2px solid #00F5D4; border-radius: 10px; 
        display: flex; flex-direction: column; align-items: center; justify-content: center; 
        transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s; 
        box-shadow: 0 0 15px rgba(0,245,212,0.3); user-select: none; margin: 0 auto;
    }
    .mtg-card.tapped { transform: rotate(90deg) scale(1.03); border-color: #FF6B6B; box-shadow: -12px 8px 20px rgba(0,0,0,0.6); }
    
    .turn-indicator { font-size: 0.95rem; color: #FFD166; font-weight: 700; margin-bottom: 0.5rem; font-family: 'Plus Jakarta Sans', sans-serif; }
    .action-btn { background: linear-gradient(135deg, #7B2CBF, #00F5D4); color: #0A041A; border: none; border-radius: 10px; padding: 0.5rem 1.5rem; font-size: 0.85rem; font-weight: 700; cursor: pointer; box-shadow: 0 0 15px rgba(0,245,212,0.4); transition: transform 0.2s; margin-top: 0.4rem; }
    .action-btn:hover { transform: scale(1.05); }
    .game-log { font-size: 0.75rem; color: #4CC9F0; margin-top: 0.6rem; font-style: italic; min-height: 30px; }
    
    /* CONGRATULATIONS WIN MODAL */
    .win-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(10,4,26,0.85); backdrop-filter: blur(6px); justify-content: center; align-items: center; z-index: 9999; }
    .win-content { background: linear-gradient(135deg, #7B2CBF, #1E0B36); color: #F0E9FA; padding: 2.5rem 2rem; border-radius: 24px; text-align: center; max-width: 380px; width: 90%; box-shadow: 0 0 50px rgba(0,245,212,0.6); border: 3px solid #00F5D4; animation: popUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
    .win-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.6rem; font-weight: 700; color: #FFD166; margin-bottom: 0.5rem; text-shadow: 0 0 15px rgba(255,209,102,0.6); }
    .win-msg { font-size: 1rem; font-weight: 600; margin-bottom: 1.5rem; color: #F0E9FA; line-height: 1.4; }
    .restart-btn { background: linear-gradient(135deg, #7B2CBF, #00F5D4); color: #0A041A; border: none; border-radius: 12px; padding: 0.7rem 2rem; font-weight: 700; font-size: 1rem; cursor: pointer; box-shadow: 0 0 15px rgba(0,245,212,0.4); transition: transform 0.2s; }
    .restart-btn:hover { transform: scale(1.06); }
    </style>
    </head>
    <body>
    <div class="duel-arena">
        <!-- PICKER PHASE (5 Cards including Matcha Boost) -->
        <div id="pickerPhase">
            <div style="font-family:'Plus Jakarta Sans',sans-serif; color:#FFD166; font-size:1.1rem; font-weight:700; margin-bottom:0.3rem;" id="pickerTitle">Player 1 (Paweetida): Choose your Card! 🎴</div>
            <div style="font-size:0.75rem; color:#4CC9F0; margin-bottom:0.8rem;">Select 1 of 5 cards to summon for this turn.</div>
            <div class="card-options">
                <div class="option-card" onclick="pickCard('💻', 'Coder Tech', 5)">
                    <div style="font-size:1.8rem;">💻</div>
                    <div style="font-size:0.65rem; font-weight:700; margin-top:3px;">Coder Tech</div>
                    <div style="font-size:0.5rem; color:#FFD166;">Attack: 5</div>
                </div>
                <div class="option-card" onclick="pickCard('🪖', 'Army Scout', 6)">
                    <div style="font-size:1.8rem;">🪖</div>
                    <div style="font-size:0.65rem; font-weight:700; margin-top:3px;">Army Scout</div>
                    <div style="font-size:0.5rem; color:#FFD166;">Attack: 6</div>
                </div>
                <div class="option-card" onclick="pickCard('👑', 'Rival Queen', 8)">
                    <div style="font-size:1.8rem;">👑</div>
                    <div style="font-size:0.65rem; font-weight:700; margin-top:3px;">Rival Queen</div>
                    <div style="font-size:0.5rem; color:#FFD166;">Attack: 8</div>
                </div>
                <div class="option-card" style="border-color: #00F5D4;" onclick="pickCard('🍵', 'Matcha Boost', 3)">
                    <div style="font-size:1.8rem;">🍵</div>
                    <div style="font-size:0.65rem; font-weight:700; margin-top:3px;">Matcha Boost</div>
                    <div style="font-size:0.5rem; color:#00F5D4;">Atk 3 & Heal 2</div>
                </div>
                <div class="option-card" style="border-color: #00F5D4;" onclick="pickCard('💖', 'Love Buff', -5)">
                    <div style="font-size:1.8rem;">💖</div>
                    <div style="font-size:0.65rem; font-weight:700; margin-top:3px;">Love Buff</div>
                    <div style="font-size:0.5rem; color:#00F5D4;">Heal: +5 HP</div>
                </div>
            </div>
        </div>

        <!-- BATTLE PHASE -->
        <div id="battlePhase">
            <div class="turn-indicator" id="turnText">Turn: Player 1 (Paweetida)</div>
            
            <div class="players-container">
                <!-- Player 1 -->
                <div class="player-box active-turn" id="p1Box">
                    <div class="player-name">Player 1 (Paweetida)</div>
                    <div class="hp-text">HP: <span id="p1Hp">20</span> ❤️</div>
                    <div class="card-container" onclick="playerTap(1)">
                        <div class="mtg-card" id="p1Card">
                            <div style="font-size: 0.6rem; color: #FFD166; font-weight: 700;" id="p1CardName">Ready</div>
                            <div style="font-size: 2.2rem;" id="p1Art">💻</div>
                            <div style="font-size: 0.55rem; color: #F0E9FA;" id="p1Status">Untapped</div>
                        </div>
                    </div>
                </div>
                
                <!-- Player 2 -->
                <div class="player-box" id="p2Box">
                    <div class="player-name">Player 2 (Dawis)</div>
                    <div class="hp-text">HP: <span id="p2Hp">20</span> ❤️</div>
                    <div class="card-container" onclick="playerTap(2)">
                        <div class="mtg-card" id="p2Card">
                            <div style="font-size: 0.6rem; color: #FFD166; font-weight: 700;" id="p2CardName">Ready</div>
                            <div style="font-size: 2.2rem;" id="p2Art">🪖</div>
                            <div style="font-size: 0.55rem; color: #F0E9FA;" id="p2Status">Untapped</div>
                        </div>
                    </div>
                </div>
            </div>
            
            <div>
                <button class="action-btn" onclick="endTurn()">End Turn / Next Round ⏭️</button>
            </div>
            <div class="game-log" id="gameLog">Click your card to Tap (Attack/Heal), then End Turn to pick a new card! ✨</div>
        </div>
    </div>

    <!-- CONGRATULATIONS WIN MODAL -->
    <div class="win-modal" id="winModal">
        <div class="win-content">
            <div style="font-size: 3rem;">🎉🏆✨</div>
            <div class="win-title">CONGRATULATIONS U WIN!</div>
            <div class="win-msg" id="winMsg">Winner is Player 1! Pure love and strategy triumph! 💜</div>
            <button class="restart-btn" onclick="location.reload()">Play Again 🔄</button>
        </div>
    </div>

    <script>
    let currentTurn = 1; // 1 = P1, 2 = P2
    let p1Hp = 20;
    let p2Hp = 20;
    let p1Card = { emoji: '💻', name: 'Coder', power: 5 };
    let p2Card = { emoji: '🪖', name: 'Soldier', power: 6 };
    let hasActed = false;

    function pickCard(emoji, name, power) {
        if (currentTurn === 1) {
            p1Card = { emoji, name, power };
            document.getElementById('p1Art').innerText = emoji;
            document.getElementById('p1CardName').innerText = name;
        } else {
            p2Card = { emoji, name, power };
            document.getElementById('p2Art').innerText = emoji;
            document.getElementById('p2CardName').innerText = name;
        }

        document.getElementById('pickerPhase').style.display = 'none';
        document.getElementById('battlePhase').style.display = 'block';
        hasActed = false;
        document.getElementById('gameLog').innerText = `Player ${currentTurn} summoned ${name}! Click your card to Tap/Action.`;
    }

    function playerTap(playerNum) {
        if (playerNum !== currentTurn) {
            document.getElementById('gameLog').innerText = `Not your turn! It is Player ${currentTurn}'s turn. 🛑`;
            return;
        }
        if (hasActed) {
            document.getElementById('gameLog').innerText = `You already acted this turn! Click 'End Turn'. ⏭️`;
            return;
        }

        hasActed = true;
        const cardEl = document.getElementById(playerNum === 1 ? 'p1Card' : 'p2Card');
        const statusEl = document.getElementById(playerNum === 1 ? 'p1Status' : 'p2Status');
        cardEl.classList.add('tapped');
        statusEl.innerText = "TAPPED";

        if (currentTurn === 1) {
            if (p1Card.name === 'Matcha Boost') {
                p2Hp = Math.max(0, p2Hp - 3);
                p1Hp = Math.min(20, p1Hp + 2);
                document.getElementById('p2Hp').innerText = p2Hp;
                document.getElementById('p1Hp').innerText = p1Hp;
                document.getElementById('gameLog').innerText = `Player 1 dealt 3 damage & healed +2 HP with Matcha Boost! 🍵`;
            } else if (p1Card.power > 0) {
                p2Hp = Math.max(0, p2Hp - p1Card.power);
                document.getElementById('p2Hp').innerText = p2Hp;
                document.getElementById('gameLog').innerText = `Player 1 dealt ${p1Card.power} damage to Player 2! 💥`;
            } else {
                p1Hp = Math.min(20, p1Hp + Math.abs(p1Card.power));
                document.getElementById('p1Hp').innerText = p1Hp;
                document.getElementById('gameLog').innerText = `Player 1 healed +${Math.abs(p1Card.power)} HP! 💚`;
            }
        } else {
            if (p2Card.name === 'Matcha Boost') {
                p1Hp = Math.max(0, p1Hp - 3);
                p2Hp = Math.min(20, p2Hp + 2);
                document.getElementById('p1Hp').innerText = p1Hp;
                document.getElementById('p2Hp').innerText = p2Hp;
                document.getElementById('gameLog').innerText = `Player 2 dealt 3 damage & healed +2 HP with Matcha Boost! 🍵`;
            } else if (p2Card.power > 0) {
                p1Hp = Math.max(0, p1Hp - p2Card.power);
                document.getElementById('p1Hp').innerText = p1Hp;
                document.getElementById('gameLog').innerText = `Player 2 dealt ${p2Card.power} damage to Player 1! 💥`;
            } else {
                p2Hp = Math.min(20, p2Hp + Math.abs(p2Card.power));
                document.getElementById('p2Hp').innerText = p2Hp;
                document.getElementById('gameLog').innerText = `Player 2 healed +${Math.abs(p2Card.power)} HP! 💚`;
            }
        }

        if (p1Hp <= 0 || p2Hp <= 0) {
            const winner = p1Hp <= 0 ? "Player 2 (Dawis 🪖)" : "Player 1 (Paweetida 💻)";
            document.getElementById('winMsg').innerText = `${winner} wins the ultimate duel with unmatched love and strategy! 🎉`;
            document.getElementById('winModal').style.display = 'flex';
        }
    }

    function endTurn() {
        if (p1Hp <= 0 || p2Hp <= 0) return;

        document.getElementById('p1Card').classList.remove('tapped');
        document.getElementById('p1Status').innerText = "Untapped";
        document.getElementById('p2Card').classList.remove('tapped');
        document.getElementById('p2Status').innerText = "Untapped";

        currentTurn = currentTurn === 1 ? 2 : 1;
        document.getElementById('turnText').innerText = `Turn: Player ${currentTurn} (${currentTurn === 1 ? 'Paweetida' : 'Dawis'})`;
        
        if (currentTurn === 1) {
            document.getElementById('p1Box').classList.add('active-turn');
            document.getElementById('p2Box').classList.remove('active-turn');
        } else {
            document.getElementById('p2Box').classList.add('active-turn');
            document.getElementById('p1Box').classList.remove('active-turn');
        }

        document.getElementById('battlePhase').style.display = 'none';
        document.getElementById('pickerPhase').style.display = 'block';
        document.getElementById('pickerTitle').innerText = `Player ${currentTurn} (${currentTurn === 1 ? 'Paweetida' : 'Dawis'}): Pick your Card for this turn! 🎴`;
    }
    </script>
    </body>
    </html>
    """, height=440, scrolling=False)

# ======== TAB 2: STATS ========
with tab_stats:
    st.markdown(f"""
    <div class="hero-section">
        <div style="font-size:2.2rem; margin-bottom:0.2rem">💜 🪖</div>
        <div class="hero-title">Paweetida & Dawis</div>
        <div class="hero-subtitle">OUR STORY · SINCE 27 JULY 2025 (the day you liked my story 🚌)</div>
        <div style="margin-top:0.5rem; color:#FFD166; font-family:'DM Sans',sans-serif; font-size:0.9rem; font-style:italic;">
            "{stats['days_together']} days of loving you — and counting."
        </div>
    </div>
    """, unsafe_allow_html=True)

    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
    <style>
    body { background: transparent; margin: 0; font-family: 'DM Sans', sans-serif; display: flex; justify-content: center; align-items: center; padding: 5px; }
    .live-card {
        background: linear-gradient(135deg, rgba(123,44,191,0.4), rgba(0,245,212,0.2));
        border: 1px solid rgba(0,245,212,0.3);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        backdrop-filter: blur(8px);
        width: 100%;
        max-width: 1000px;
    }
    .main-title { font-size: 0.75rem; color: #4CC9F0; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.3rem; font-weight: 500; }
    .main-number { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2.8rem; font-weight: 700; color: #FFD166; line-height: 1; margin-bottom: 0.2rem; }
    .main-unit { font-size: 0.9rem; color: #F0E9FA; margin-bottom: 1rem; font-weight: 500; }
    .sub-grid { display: flex; justify-content: center; gap: 10px; }
    .sub-box {
        background: rgba(10,4,26,0.6);
        border: 1px solid rgba(0,245,212,0.3);
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        min-width: 80px;
        text-align: center;
    }
    .sub-num { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.3rem; font-weight: 700; color: #F0E9FA; line-height: 1.1; }
    .sub-lbl { font-size: 0.7rem; color: #4CC9F0; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.2rem; }
    </style>
    </head>
    <body>
        <div class="live-card">
            <div class="main-title">Since Day One (Official Couple) 💜</div>
            <div class="main-number" id="daysNum">0</div>
            <div class="main-unit">Days</div>
            <div class="sub-grid">
                <div class="sub-box">
                    <div class="sub-num" id="hoursNum">0</div>
                    <div class="sub-lbl">Hours</div>
                </div>
                <div class="sub-box">
                    <div class="sub-num" id="minsNum">0</div>
                    <div class="sub-lbl">Minutes</div>
                </div>
                <div class="sub-box">
                    <div class="sub-num" id="secsNum" style="color: #FFD166;">0</div>
                    <div class="sub-lbl">Seconds</div>
                </div>
            </div>
        </div>
        <script>
        const startDate = new Date("2025-08-22T00:00:00");
        function updateCounter() {
            const now = new Date();
            const diff = now - startDate;
            if (diff > 0) {
                const days = Math.floor(diff / (1000 * 60 * 60 * 24));
                const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
                const mins = Math.floor((diff / 1000 / 60) % 60);
                const secs = Math.floor((diff / 1000) % 60);

                document.getElementById("daysNum").innerText = days.toLocaleString();
                document.getElementById("hoursNum").innerText = hours;
                document.getElementById("minsNum").innerText = mins;
                document.getElementById("secsNum").innerText = secs;
            }
        }
        setInterval(updateCounter, 1000);
        updateCounter();
        </script>
    </body>
    </html>
    """, height=190, scrolling=False)

    st.markdown("<div style='margin-top:0.4rem'></div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-number">{stats["weeks_together"]}</div><div class="metric-label">Weeks Together</div><div class="metric-desc">{stats["months_together"]} months of us 🌙</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-number">{stats["days_to_anniversary"]}</div><div class="metric-label">Days to Anniversary</div><div class="metric-desc">22 Aug {stats["next_anniversary"].year} 🎉</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-number">{stats["days_since_first"]}</div><div class="metric-label">Days Since We Met</div><div class="metric-desc">27 Jul 2025 on the bus 🚌</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-number">{stats["days_together"]}</div><div class="metric-label">Total Days</div><div class="metric-desc">Counting every single day 💜</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top:0.6rem'></div>", unsafe_allow_html=True)

    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.markdown(f"""
        <div class="army-badge">
            <div style="font-size:1.8rem">🪖</div>
            <div style="font-size:1.4rem; font-family:'Playfair Display',serif; color:#FFD166; font-weight:700;">{stats['days_since_army']}</div>
            <div style="font-size:0.7rem; letter-spacing:1px; text-transform:uppercase; color:#00F5D4;">Days in Service</div>
            <div style="font-size:0.8rem; margin-top:0.2rem; color:#F0E9FA;">Dawis in Australian Army (20 Apr 2026)</div>
        </div>""", unsafe_allow_html=True)

    with col_b:
        milestones_df = get_milestones()
        if not milestones_df.empty:
            milestones_df['date'] = pd.to_datetime(milestones_df['date'])
            fig = go.Figure()
            colors = ['#FFD166', '#00F5D4', '#4CC9F0']
            positions = ['top center', 'bottom center', 'top center']
            
            for i, row in milestones_df.iterrows():
                fig.add_trace(go.Scatter(
                    x=[row['date']], y=[1.0],
                    mode='markers+text',
                    marker=dict(size=12, color=colors[i % 3], symbol='diamond'),
                    text=[row['title']], 
                    textposition=positions[i % 3],
                    textfont=dict(color='#F0E9FA', size=8.5),
                    showlegend=False
                ))
            
            fig.add_shape(type='line',
                x0=milestones_df['date'].min(), x1=date.today(),
                y0=1.0, y1=1.0,
                line=dict(color='rgba(0,245,212,0.5)', width=2))

            fig.update_layout(
                title=dict(text='Our Journey Together', font=dict(color='#F0E9FA', size=11)),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(visible=False, range=[0.3, 1.7]), xaxis=dict(showgrid=False, color='#4CC9F0'),
                height=150, margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)

    progress = max(0, min(1, 1 - (stats['days_to_anniversary'] / 365)))
    st.progress(progress)
    st.markdown(f'<div style="color:#4CC9F0; font-size:0.75rem; text-align:center; margin-top:0.3rem;">{stats["days_to_anniversary"]} days until 22 August {stats["next_anniversary"].year}</div>', unsafe_allow_html=True)

# ======== TAB 3: MEMORIES ========
with tab_memories:
    st.markdown('<div class="section-title">Our Memories 💜</div>', unsafe_allow_html=True)
    memories_df = get_memories()
    if memories_df.empty:
        st.markdown('<div style="text-align:center; color:#4CC9F0; padding:1.5rem;">No memories yet — add your first one!</div>', unsafe_allow_html=True)
    else:
        categories = ['All'] + list(memories_df['category'].unique())
        selected_cat = st.selectbox("Filter by category", categories, label_visibility="collapsed")
        filtered_df = memories_df[memories_df['category'] == selected_cat] if selected_cat != 'All' else memories_df
        for _, row in filtered_df.iterrows():
            col_mem, col_del = st.columns([11, 1])
            with col_mem:
                st.markdown(f'<div class="memory-card"><span style="color:#FFD166; font-size:0.7rem;">{row["date"]}</span> <b style="font-size:0.95rem;">{row["emoji"]} {row["title"]}</b> — <span style="color:#4CC9F0">{row["description"] or ""}</span></div>', unsafe_allow_html=True)
            with col_del:
                if st.button("🗑️", key=f"del_{row['id']}"):
                    delete_memory(row['id'])
                    st.rerun()

# ======== TAB 4: TIMELINE ========
with tab_timeline:
    st.markdown('<div class="section-title">Our Timeline Scrapbook 📸 (Hover to view Polaroid)</div>', unsafe_allow_html=True)
    milestones_df = get_milestones()
    memories_df = get_memories()
    
    all_events = []
    for _, row in milestones_df.iterrows():
        img_data = row['image_data'] if 'image_data' in row and pd.notna(row['image_data']) else None
        img_content = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; height:100%; object-fit:cover; border-radius:2px;">' if img_data else '⭐'
        all_events.append({'date': row['date'], 'title': row['title'], 'img_html': img_content})
        
    for _, row in memories_df.iterrows():
        img_data = row['image_data'] if 'image_data' in row and pd.notna(row['image_data']) else None
        emoji_val = row['emoji'] if 'emoji' in row and pd.notna(row['emoji']) else '💜'
        img_content = f'<img src="data:image/jpeg;base64,{img_data}" style="width:100%; height:100%; object-fit:cover; border-radius:2px;">' if img_data else emoji_val
        all_events.append({'date': row['date'], 'title': row['title'], 'img_html': img_content})
    
    all_events = sorted(all_events, key=lambda x: x['date'])

    timeline_items_html = ""
    for idx, event in enumerate(all_events):
        item_class = "left-item" if idx % 2 == 0 else "right-item"
        
        timeline_items_html += f"""
        <div class="timeline-item {item_class}">
            <div class="timeline-content">
                <div class="timeline-date">{event['date']}</div>
                <div class="timeline-title">{event['title']}</div>
                <div class="polaroid-popup-down">
                    <div class="polaroid-img">{event['img_html']}</div>
                    <div class="polaroid-caption">{event['title']}</div>
                </div>
            </div>
        </div>
        """

    components.html(f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
    * {{ font-family: 'DM Sans', sans-serif; box-sizing: border-box; }}
    body {{ background: transparent; margin: 0; padding: 20px 20px 100px 20px; overflow: visible; }}
    .scrapbook-timeline {{
        position: relative;
        max-width: 800px;
        margin: 0 auto;
        padding: 0;
    }}
    .scrapbook-timeline::after {{
        content: '';
        position: absolute;
        width: 3px;
        background: linear-gradient(to bottom, #00F5D4, #7B2CBF, #4CC9F0);
        top: 20px;
        bottom: 20px;
        left: 50%;
        margin-left: -1.5px;
        border-radius: 2px;
    }}
    .timeline-item {{
        padding: 0 40px 60px 40px;
        position: relative;
        background: inherit;
        width: 50%;
    }}
    .timeline-item::after {{
        content: '';
        position: absolute;
        width: 14px;
        height: 14px;
        right: -7px;
        background-color: #FFD166;
        border: 3px solid #1E0B36;
        top: 15px;
        border-radius: 50%;
        z-index: 1;
    }}
    .left-item {{ left: 0; text-align: right; }}
    .right-item {{ left: 50%; text-align: left; }}
    .right-item::after {{ left: -7px; }}
    
    .timeline-content {{
        padding: 12px 18px;
        background: rgba(30, 15, 60, 0.9);
        border: 1px solid rgba(0, 245, 212, 0.4);
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        display: inline-block;
        cursor: pointer;
        position: relative;
        transition: transform 0.2s;
    }}
    .timeline-content:hover {{
        transform: scale(1.05);
        border-color: #FFD166;
    }}
    
    .timeline-date {{
        font-size: 0.65rem;
        color: #FFD166;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-weight: 700;
        margin-bottom: 2px;
    }}
    .timeline-title {{
        font-size: 0.9rem;
        font-weight: 700;
        color: #F0E9FA;
    }}

    .polaroid-popup-down {{
        visibility: hidden;
        opacity: 0;
        position: absolute;
        top: 140%;
        left: 50%;
        transform: translateX(-50%) scale(0.8);
        background: #FAFAFA;
        padding: 10px 10px 18px 10px;
        border-radius: 4px;
        box-shadow: 0 15px 35px rgba(0,0,0,0.6);
        width: 160px;
        text-align: center;
        z-index: 9999;
        transition: all 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        pointer-events: none;
    }}
    .timeline-content:hover .polaroid-popup-down {{
        visibility: visible;
        opacity: 1;
        transform: translateX(-50%) scale(1) rotate(3deg);
    }}

    .polaroid-img {{
        background: #0A041A;
        height: 110px;
        border-radius: 2px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 3rem;
        margin-bottom: 8px;
        overflow: hidden;
    }}
    .polaroid-caption {{
        font-size: 0.75rem;
        font-weight: 700;
        color: #0A041A;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
    }}
    </style>
    </head>
    <body>
        <div class="scrapbook-timeline">
            {timeline_items_html}
        </div>
    </body>
    </html>
    """, height=700, scrolling=True)

# ======== TAB 5: ADD MEMORY ========
with tab_add:
    st.markdown('<div class="section-title">Add a New Memory ➕</div>', unsafe_allow_html=True)
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        mem_title = st.text_input("Title *", placeholder="e.g. Queenstown trip")
        mem_date = st.date_input("Date", value=date.today())
    with col_f2:
        mem_category = st.selectbox("Category", ["Date Night", "Travel", "Milestone", "Everyday", "Food", "Army Life", "Other"])
        mem_emoji = st.selectbox("Emoji", ["💜", "🥰", "✈️", "🍜", "🎉", "🪖", "🏔️", "🌸", "⭐", "🎂", "🏖️"])
    
    uploaded_image = st.file_uploader("Upload Polaroid Photo (Optional)", type=["jpg", "jpeg", "png"])
    
    mem_desc = st.text_area("Description (English)", placeholder="Write something sweet in English...", height=60)
    
    if st.button("Save Memory 💜", use_container_width=True):
        if mem_title:
            img_base64 = None
            if uploaded_image is not None:
                bytes_data = uploaded_image.getvalue()
                img_base64 = base64.b64encode(bytes_data).decode('utf-8')
            
            add_memory(mem_title, mem_desc, mem_date, mem_category, mem_emoji, img_base64)
            st.success("Memory saved successfully!")
            st.rerun()
        else:
            st.error("Please add a title!")
