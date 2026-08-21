import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date
import plotly.graph_objects as go
import base64

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Paweetida & Dawis 💜", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

# ---- CUSTOM CSS (MODERN MINIMALIST TYPOGRAPHY) ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {
    --aurora-purple: #4A154B;
    --aurora-violet: #7B2CBF;
    --aurora-green: #00F5D4;
    --aurora-cyan: #4CC9F0;
    --aurora-dark: #0A041A;
    --gold: #FFD166;
}

* { font-family: 'Outfit', sans-serif !important; }

h1, h2, h3, .hero-title, .metric-number {
    font-family: 'Outfit', sans-serif !important;
    font-weight: 700 !important;
    letter-spacing: -0.5px;
}

/* Modern & Clean Top Navigation Buttons */
.stButton button {
    background: linear-gradient(135deg, rgba(123,44,191,0.7), rgba(0,245,212,0.4)) !important;
    color: #FFFFFF !important;
    border: 1px solid rgba(0,245,212,0.5) !important;
    border-radius: 16px !important;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1rem !important;
    padding: 0.8rem 1rem !important;
    width: 100% !important;
    box-shadow: 0 4px 20px rgba(0,245,212,0.15);
    backdrop-filter: blur(10px);
    transition: all 0.25s ease;
}
.stButton button:hover {
    transform: translateY(-2px);
    border-color: #FFD166 !important;
    box-shadow: 0 6px 25px rgba(255,209,102,0.3);
    background: linear-gradient(135deg, rgba(123,44,191,0.9), rgba(0,245,212,0.6)) !important;
}

/* Hide system text inputs */
div[data-testid="stTextInput"]:has(input[aria-label="hidden_welcome"]),
div[data-testid="stTextInput"]:has(input[aria-label="hidden_pin"]) {
    display: none !important;
    height: 0px !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}

/* AURORA LIGHTS DYNAMIC BACKGROUND ANIMATION */
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
    font-weight: 600;
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
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 1px;
    white-space: nowrap;
    animation: pulse 1.5s infinite;
}
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }

.hero-section {
    background: linear-gradient(135deg, rgba(123,44,191,0.6), rgba(0,245,212,0.25));
    border-radius: 20px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(76,201,240,0.4);
    backdrop-filter: blur(12px);
    margin-bottom: 1rem;
    box-shadow: 0 0 35px rgba(0,245,212,0.25);
    position: relative;
    z-index: 2;
}

.hero-title { font-size: 2rem; font-weight: 700; color: #F0E9FA; margin: 0; }
.hero-subtitle { font-size: 0.8rem; color: #4CC9F0; margin-top: 0.2rem; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 600; }

.metric-card {
    background: linear-gradient(135deg, rgba(123,44,191,0.5), rgba(76,201,240,0.25));
    border: 1px solid rgba(0,245,212,0.3);
    border-radius: 16px;
    padding: 1rem;
    text-align: center;
    backdrop-filter: blur(8px);
    position: relative;
    z-index: 2;
    box-shadow: 0 0 15px rgba(123,44,191,0.2);
}

.metric-number { font-size: 2.4rem; font-weight: 700; color: #FFD166; line-height: 1; }
.metric-label { font-size: 0.75rem; color: #4CC9F0; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.3rem; font-weight: 600; }

.section-title {
    font-size: 1.1rem;
    font-weight: 600;
    color: #F0E9FA;
    margin-bottom: 0.6rem;
    border-bottom: 1px solid rgba(0,245,212,0.4);
    padding-bottom: 0.2rem;
    position: relative;
    z-index: 2;
}

.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: rgba(30, 15, 60, 0.85) !important;
    border: 1px solid rgba(76,201,240,0.5) !important;
    color: #F0E9FA !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
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

# ---- DATABASE & STATS ----
def init_db():
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS milestones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        type TEXT DEFAULT 'milestone'
    )''')
    
    c.execute("DROP TABLE IF EXISTS milestones")
    c.execute('''CREATE TABLE IF NOT EXISTS milestones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        type TEXT DEFAULT 'milestone'
    )''')
    
    default_milestones = [
        ("First Liked Story ✨", "2025-07-27", "The day you first liked my IG story", "start"),
        ("First Date 🍿", "2025-08-15", "Our first movie and food date", "date"),
        ("Official Anniversary 2025 🎉", "2025-08-22", "The day we became official couple", "anniversary"),
        ("NZ 1st Trip 🏔️", "2026-03-29", "1st trip together in NZ", "trip"),
        ("Dawis Enlists Army 🪖", "2026-04-20", "Dawis joined the Australian Army", "milestone"),
        ("Dawis HBD 🎂", "2026-06-29", "Happy Birthday Dawis", "hbd"),
        ("Paweetida HBD 🎂", "2026-07-16", "Happy Birthday Paweetida", "hbd"),
        ("1st Anniversary 2026 🎉", "2026-08-22", "Celebrating 1 year together", "anniversary"),
    ]
    c.executemany("INSERT INTO milestones (title, date, description, type) VALUES (?,?,?,?)", default_milestones)
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

# ---- PASSWORD LOGIN & WELCOME SCREEN FOR DAWIS ----
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "welcomed" not in st.session_state:
        st.session_state.welcomed = False

    if not st.session_state.authenticated:
        components.html("""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@400;600;700&family=Pacifico&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Outfit', sans-serif; }
body {
    background: transparent;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 1rem;
    overflow: hidden;
}
@keyframes shootingStar {
    0% { transform: translateX(0) translateY(0); opacity: 1; }
    100% { transform: translateX(-500px) translateY(500px); opacity: 0; }
}
.login-shooting-star {
    position: fixed; width: 2px; height: 2px; background: #00F5D4; border-radius: 50%;
    box-shadow: 0 0 8px 2px #00F5D4, 0 0 20px 4px #4CC9F0;
    animation: shootingStar linear infinite; z-index: 0; pointer-events: none;
}
.floating-emoji { position: fixed; font-size: 1.5rem; animation: floatUp linear infinite; pointer-events: none; z-index: 0; opacity: 0.7; }
@keyframes floatUp { 0% { transform: translateY(100vh) rotate(0deg); opacity: 0; } 10% { opacity: 0.7; } 90% { opacity: 0.7; } 100% { transform: translateY(-10vh) rotate(360deg); opacity: 0; } }

@keyframes bounce { 0%, 100% { transform: translateY(0px) rotate(-3deg); } 25% { transform: translateY(-15px) rotate(3deg); } 50% { transform: translateY(-8px) rotate(-2deg); } 75% { transform: translateY(-20px) rotate(4deg); } }
@keyframes bounce2 { 0%, 100% { transform: translateY(0px) rotate(3deg); } 25% { transform: translateY(-20px) rotate(-3deg); } 50% { transform: translateY(-10px) rotate(2deg); } 75% { transform: translateY(-15px) rotate(-4deg); } }
@keyframes heartbeat { 0%, 100% { transform: scale(1); } 15% { transform: scale(1.3); } 30% { transform: scale(1); } 45% { transform: scale(1.2); } 60% { transform: scale(1); } }
@keyframes float { 0%, 100% { transform: translateY(0px); } 50% { transform: translateY(-8px); } }
@keyframes shimmer { 0%, 100% { opacity: 0.6; } 50% { opacity: 1; } }
@keyframes shake { 0%, 100% { transform: translateX(0); } 20% { transform: translateX(-8px); } 40% { transform: translateX(8px); } 60% { transform: translateX(-6px); } 80% { transform: translateX(6px); } }
@keyframes pop { 0% { transform: scale(1); } 50% { transform: scale(1.15); } 100% { transform: scale(1); } }

.chars { display: flex; justify-content: center; align-items: center; gap: 1.5rem; margin-bottom: 1rem; }
.girl { font-size: 4rem; animation: bounce 1.4s ease-in-out infinite; display: inline-block; }
.heart { font-size: 2.8rem; animation: heartbeat 1.2s ease-in-out infinite; display: inline-block; }
.soldier { font-size: 4rem; animation: bounce2 1.6s ease-in-out infinite; display: inline-block; }
.title {
    font-family: 'Pacifico', cursive;
    font-size: 3.2rem;
    background: linear-gradient(135deg, #00F5D4, #FFD166);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: float 3s ease-in-out infinite;
    line-height: 1.1;
}
.and { font-family: 'Pacifico', cursive; font-size: 1.5rem; color: #4CC9F0; margin: 0.1rem 0; }
.subtitle { font-size: 0.75rem; color: #00F5D4; letter-spacing: 2px; text-transform: uppercase; margin-top: 0.8rem; animation: shimmer 2s ease-in-out infinite; font-weight: 600; }
.moon-quote { font-size: 0.85rem; color: #FFD166; font-style: italic; margin-top: 0.4rem; font-weight: 500; }
.stars { font-size: 1.2rem; letter-spacing: 0.4rem; margin: 0.5rem 0; animation: shimmer 2s ease-in-out infinite; }

.pin-section {
    margin-top: 1.5rem;
    background: rgba(30, 15, 60, 0.75);
    border: 1px solid rgba(0, 245, 212, 0.4);
    border-radius: 20px;
    padding: 1.5rem 2rem;
    max-width: 400px;
    width: 100%;
    backdrop-filter: blur(10px);
    box-shadow: 0 0 25px rgba(123, 44, 191, 0.3);
    position: relative;
    z-index: 1;
}
.pin-title { font-family: 'Outfit', sans-serif; font-size: 1.1rem; color: #00F5D4; margin-bottom: 0.3rem; font-weight: 600; }
.pin-hint { font-size: 0.75rem; color: rgba(76, 201, 240, 0.7); margin-bottom: 1.2rem; font-style: italic; }
.pin-boxes { display: flex; justify-content: center; gap: 0.6rem; margin-bottom: 1.2rem; }
.pin-box {
    width: 46px;
    height: 56px;
    border: 2px solid rgba(0, 245, 212, 0.4);
    border-radius: 10px;
    background: rgba(10, 4, 26, 0.6);
    font-size: 1.6rem;
    color: #FFD166;
    text-align: center;
    font-weight: 600;
    outline: none;
    transition: all 0.2s;
    caret-color: transparent;
}
.pin-box:focus { border-color: #00F5D4; background: rgba(123, 44, 191, 0.4); box-shadow: 0 0 15px rgba(0, 245, 212, 0.5); transform: scale(1.05); }
.pin-box.filled { border-color: #FFD166; animation: pop 0.2s ease; }
.pin-box.error { border-color: #FF6B6B; animation: shake 0.4s ease; }
.enter-btn {
    background: linear-gradient(135deg, #7B2CBF, #00F5D4);
    color: #0A041A;
    border: none;
    border-radius: 10px;
    padding: 0.75rem 2.5rem;
    font-size: 0.9rem;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    transition: all 0.2s;
    letter-spacing: 0.5px;
    box-shadow: 0 0 15px rgba(0,245,212,0.4);
}
.enter-btn:hover { background: linear-gradient(135deg, #9D4EDD, #4CC9F0); transform: translateY(-2px); box-shadow: 0 4px 20px rgba(0,245,212,0.6); }
.error-msg { color: #FF6B6B; font-size: 0.8rem; margin-top: 0.8rem; display: none; }
.lock-icon { font-size: 1.8rem; margin-bottom: 0.5rem; animation: float 2.5s ease-in-out infinite; display: block; }
</style>
</head>
<body>
    <script>
    for (let i = 0; i < 12; i++) {
        let star = document.createElement('div');
        star.className = 'login-shooting-star';
        star.style.top = Math.random() * 60 + 'vh';
        star.style.left = Math.random() * 100 + 'vw';
        star.style.animationDuration = (2 + Math.random() * 3) + 's';
        star.style.animationDelay = (Math.random() * 4) + 's';
        document.body.appendChild(star);
    }
    const emojis = ['💐','🍀','🪐','🌜','🌹','🌻','☃️','🌟','💜','💚','🌷','🌹','💙','❄️','⭐','🤍','☃️','💛','🧡','❤️','🌻','🍀','🌷','🌐','🌻','💻','📡','🛜','🍀','💜','🤍','❄️'];
    for (let i = 0; i < 20; i++) {
        let el = document.createElement('div');
        el.className = 'floating-emoji';
        el.textContent = emojis[Math.floor(Math.random() * emojis.length)];
        el.style.left = Math.random() * 100 + 'vw';
        el.style.animationDuration = (5 + Math.random() * 8) + 's';
        el.style.animationDelay = (Math.random() * 8) + 's';
        el.style.fontSize = (1 + Math.random() * 1.5) + 'rem';
        document.body.appendChild(el);
    }
    </script>
    <div style="position:relative; z-index:1;">
    <div class="chars">
        <span class="girl">💻</span>
        <span class="heart">💜</span>
        <span class="soldier">🪖</span>
    </div>
    <div class="stars">☃️🪐 🌙 🌟 ❄️</div>
    <div class="title">Paweetida</div>
    <div class="and">&amp;</div>
    <div class="title">Dawis</div>
    <div class="subtitle">Our Private Little World 💜</div>
    <div class="moon-quote">🌙 "The moon is beautiful, isn't it?" ✨</div>
    </div>
    <div class="pin-section">
        <span class="lock-icon">🔐</span>
        <div class="pin-title">Enter our secret code</div>
        <div class="pin-hint">hint: our special date 💜</div>
        <div class="pin-boxes">
            <input class="pin-box" maxlength="1" type="password" id="p0" inputmode="numeric">
            <input class="pin-box" maxlength="1" type="password" id="p1" inputmode="numeric">
            <input class="pin-box" maxlength="1" type="password" id="p2" inputmode="numeric">
            <input class="pin-box" maxlength="1" type="password" id="p3" inputmode="numeric">
            <input class="pin-box" maxlength="1" type="password" id="p4" inputmode="numeric">
            <input class="pin-box" maxlength="1" type="password" id="p5" inputmode="numeric">
        </div>
        <button class="enter-btn" onclick="checkPin()">Enter Our World 💜</button>
        <div class="error-msg" id="errMsg">Hmm, that's not right... 💔 Try again!</div>
    </div>
    <script>
    const boxes = document.querySelectorAll('.pin-box');
    boxes[0].focus();
    boxes.forEach((box, i) => {
        box.addEventListener('input', (e) => {
            if (box.value) {
                box.classList.add('filled');
                box.classList.remove('error');
                if (i < 5) boxes[i+1].focus();
            }
        });
        box.addEventListener('keydown', (e) => {
            if (e.key === 'Backspace' && !box.value && i > 0) {
                boxes[i-1].focus();
                boxes[i-1].value = '';
                boxes[i-1].classList.remove('filled');
            }
            if (e.key === 'Enter') checkPin();
        });
    });
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
        } else {
            boxes.forEach(b => { b.classList.add('error'); b.classList.remove('filled'); });
            setTimeout(() => { boxes.forEach(b => b.classList.remove('error')); }, 500);
            document.getElementById('errMsg').style.display = 'block';
            boxes.forEach(b => b.value = '');
            boxes[0].focus();
        }
    }
    </script>
</body>
</html>
""", height=740, scrolling=False)

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
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600&family=Pacifico&display=swap" rel="stylesheet">
        <style>
        body { background: transparent; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: 'Outfit', sans-serif; }
        .welcome-card {
            background: linear-gradient(135deg, rgba(123,44,191,0.85), rgba(0,245,212,0.6));
            border: 2px solid #FFD166;
            border-radius: 28px;
            padding: 2.8rem 2.2rem;
            text-align: center;
            max-width: 460px;
            width: 90%;
            box-shadow: 0 0 50px rgba(0,245,212,0.5);
            animation: popUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            color: #FFFFFF;
        }
        @keyframes popUp { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
        .welcome-title { font-family: 'Pacifico', cursive; font-size: 2.6rem; color: #FFD166; margin-bottom: 0.4rem; text-shadow: 0 0 15px rgba(255,209,102,0.6); }
        .welcome-sub { font-size: 0.95rem; font-weight: 600; margin-bottom: 1.2rem; color: #FF6B6B; letter-spacing: 0.5px; }
        .welcome-desc { font-size: 0.92rem; line-height: 1.7; margin-bottom: 2rem; color: #F0E9FA; font-weight: 500; }
        .highlight-text { color: #FFD166; font-weight: 600; }
        .explore-btn {
            background: linear-gradient(135deg, #FFD166, #00F5D4);
            color: #0A041A;
            border: none;
            border-radius: 14px;
            padding: 0.85rem 2.2rem;
            font-size: 1.02rem;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(0,245,212,0.6);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        .explore-btn:hover { transform: scale(1.06); box-shadow: 0 0 25px rgba(255,209,102,0.8); background: linear-gradient(135deg, #FFE188, #2EE8CC); }
        </style>
        </head>
        <body>
            <div class="welcome-card">
                <div style="font-size: 3.2rem; margin-bottom: 0.4rem;">🚨💻😏</div>
                <div class="welcome-title">¡Buenos, Dawis!</div>
                <div class="welcome-sub">⚠️ Watch out for potential scammers if you click randomly! 💸</div>
                <div class="welcome-desc">
                    Just to be clear... I didn't build this website because I love you so much or anything! 
                    <br><br>
                    I just wanted to level up my IT and Data Engineering skills, you know? 55555
                    <br><br>
                    Anyway, luv u tho 💜
                    <br><br>
                    <span class="highlight-text">Curious to know what's next? Proceed at your own risk! 🤫👇</span>
                </div>
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
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600&display=swap" rel="stylesheet">
<style>
.news-overlay { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(10,4,26,0.85); backdrop-filter: blur(8px); display: flex; justify-content: center; align-items: center; z-index: 99999; }
.news-modal { background: linear-gradient(135deg, #8B0000, #1E0B36); border: 3px solid #00F5D4; border-radius: 20px; padding: 2rem; max-width: 420px; width: 90%; text-align: center; color: #FFFFFF; box-shadow: 0 0 40px rgba(0,245,212,0.4); animation: popUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); font-family: 'Outfit', sans-serif; }
@keyframes popUp { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
.news-header { background: #00F5D4; color: #0A041A; font-size: 0.7rem; font-weight: 600; padding: 0.3rem 0.8rem; border-radius: 4px; display: inline-block; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 0.6rem; white-space: nowrap; }
.news-title { font-size: 1.3rem; font-weight: 600; margin-bottom: 0.5rem; color: #FFD166; }
.news-desc { font-size: 0.9rem; line-height: 1.4; margin-bottom: 1.2rem; color: #F0E9FA; font-weight: 500; }
.warning-box { background: rgba(0, 245, 212, 0.15); border: 2px dashed #00F5D4; border-radius: 10px; padding: 0.7rem; margin-bottom: 1.2rem; color: #00F5D4; font-weight: 600; font-size: 0.85rem; }
.ack-btn { background: linear-gradient(135deg, #7B2CBF, #00F5D4); color: #0A041A; border: none; border-radius: 10px; padding: 0.6rem 1.8rem; font-weight: 600; font-size: 0.9rem; cursor: pointer; box-shadow: 0 0 15px rgba(0,245,212,0.4); transition: transform 0.2s; }
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
    <div style="white-space: nowrap; overflow: hidden; text-overflow: ellipsis; color: #FFFFFF; font-weight: 600;">
        ⚠️ WARNING: DO NOT FORGET OUR SPECIAL ANNIVERSARY! Stay tuned for card duels and memories! 💜🪖
    </div>
</div>
""", unsafe_allow_html=True)

# ---- NAVIGATION BUTTON BOXES ----
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "💐 Get Flowers"

nav_tabs = ["💐 Get Flowers", "💌 Love Capsule", "⚔️ Battle Phase", "📊 Our Stats"]

cols = st.columns(len(nav_tabs))
for i, tab_name in enumerate(nav_tabs):
    with cols[i]:
        if st.button(tab_name, use_container_width=True, key=f"nav_btn_{i}_{tab_name}"):
            st.session_state.active_tab = tab_name
            st.rerun()

st.markdown("<hr style='border: 0.5px solid rgba(0,245,212,0.3); margin: 1rem 0 1.5rem 0;'>", unsafe_allow_html=True)

# ======== TAB 0: GET FLOWERS & INTERACTIVE BOUQUET ========
if st.session_state.active_tab == "💐 Get Flowers":
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem 0;">
        <h1 style="color: #FFD166; font-size: 2.8rem; font-weight: 700; margin-bottom: 0.2rem; text-shadow: 0 0 20px rgba(255,209,102,0.5);">Get Flowers! 🌷</h1>
        <p style="color: #4CC9F0; font-size: 1.05rem; font-weight: 600; letter-spacing: 0.5px;">Well done! A bouquet for my favorite enemy. 😜</p>
    </div>
    """, unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns([1, 2, 1])
    with col_f2:
        # Interactive bouquet with floating hearts & click-to-change tease message
        components.html("""
        <!DOCTYPE html>
        <html>
        <head>
        <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&display=swap" rel="stylesheet">
        <style>
        body { background: transparent; display: flex; justify-content: center; align-items: center; margin: 0; font-family: 'Outfit', sans-serif; overflow: visible; }
        .flower-card {
            background: linear-gradient(135deg, rgba(123,44,191,0.5), rgba(255,182,193,0.25));
            border: 2px solid rgba(255,192,203,0.7);
            border-radius: 28px;
            padding: 2rem;
            text-align: center;
            box-shadow: 0 0 40px rgba(255,182,193,0.35);
            backdrop-filter: blur(12px);
            position: relative;
            max-width: 420px;
            width: 100%;
        }
        .img-container {
            position: relative;
            display: inline-block;
            cursor: pointer;
        }
        .flower-img {
            width: 180px;
            height: 180px;
            object-fit: cover;
            border-radius: 50%;
            border: 4px solid #FFD166;
            box-shadow: 0 0 25px rgba(255,209,102,0.5);
            animation: float 3s ease-in-out infinite;
            transition: transform 0.3s ease;
        }
        .flower-img:hover {
            transform: scale(1.08) rotate(3deg);
        }
        @keyframes float {
            0%, 100% { transform: translateY(0px); }
            50% { transform: translateY(-8px); }
        }
        .floating-heart {
            position: absolute;
            font-size: 1.4rem;
            animation: floatHeart 2.2s ease-in-out infinite;
            pointer-events: none;
            opacity: 0;
        }
        @keyframes floatHeart {
            0% { transform: translateY(0) scale(0.6); opacity: 1; }
            100% { transform: translateY(-70px) scale(1.3); opacity: 0; }
        }
        .heart-1 { top: 10px; left: 10px; animation-delay: 0s; }
        .heart-2 { top: 0px; right: 20px; animation-delay: 0.7s; }
        .heart-3 { bottom: 20px; left: 0px; animation-delay: 1.4s; }
        
        .rival-title { font-size: 1.3rem; color: #FFD166; font-weight: 700; margin: 1rem 0 0.5rem 0; }
        .rival-desc { font-size: 0.95rem; color: #F0E9FA; line-height: 1.6; font-weight: 500; }
        .click-hint { font-size: 0.7rem; color: #4CC9F0; margin-top: 0.6rem; font-style: italic; }
        </style>
        </head>
        <body>
            <div class="flower-card">
                <div class="img-container" onclick="changeTease()" title="Click me! ✨">
                    <span class="floating-heart heart-1">💜</span>
                    <span class="floating-heart heart-2">✨</span>
                    <span class="floating-heart heart-3">💖</span>
                    <img src="https://images.unsplash.com/photo-1561181286-d3fee7d55364?auto=format&fit=crop&w=600&q=80" class="flower-img">
                </div>
                <div class="rival-title">For My Favorite Rival 😈</div>
                <div class="rival-desc" id="teaseText">
                    Thanks for sticking around, even when I'm super moody and don't want to talk! 555. Let's keep supporting and driving each other crazy for a long, long time. 💜
                </div>
                <div class="click-hint">(Click the bouquet for a surprise message 🌷)</div>
            </div>
            <script>
            const teases = [
                "Thanks for sticking around, even when I'm super moody and don't want to talk! 555. Let's keep supporting and driving each other crazy for a long, long time. 💜",
                "Warning: Clicking these flowers too much won't make me less stubborn! 😤 But okay, luv u 💜",
                "You're lucky you're my favorite rival. Otherwise, no flowers for you! 😜🌷",
                "Teasing you is my full-time job, but loving you is my favorite hobby. ✨"
            ];
            let index = 0;
            function changeTease() {
                index = (index + 1) % teases.length;
                document.getElementById('teaseText').innerText = teases[index];
            }
            </script>
        </body>
        </html>
        """, height=410, scrolling=False)

    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-title" style="text-align: center;">💖 Select Our Memory Menu 💖</div>', unsafe_allow_html=True)
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)

    # 3 Streamlined Menu Buttons
    mcol1, mcol2, mcol3 = st.columns(3)
    with mcol1:
        if st.button("🍒 Our Time Together\n\nCheck our live counter & journey 💜", use_container_width=True, key="menu_btn_1"):
            st.session_state.active_tab = "📊 Our Stats"
            st.rerun()
    with mcol2:
        if st.button("💌 Love Capsule\n\nOpen a secret note from me ✉️", use_container_width=True, key="menu_btn_2"):
            st.session_state.active_tab = "💌 Love Capsule"
            st.rerun()
    with mcol3:
        if st.button("⚔️ Card Duel Arena\n\nTest our teamwork & stats 🌟", use_container_width=True, key="menu_btn_3"):
            st.session_state.active_tab = "⚔️ Battle Phase"
            st.rerun()

# ======== TAB 1: LOVE CAPSULE ========
elif st.session_state.active_tab == "💌 Love Capsule":
    st.markdown('<div class="section-title">Love Capsule — Open a Secret Note 💌</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #4CC9F0; font-size: 0.95rem; font-weight: 600; margin-bottom: 1.5rem;">Pick a letter to reveal a supportive message or a playful tease from your favorite rival! ✨</div>', unsafe_allow_html=True)
    
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
    body { background: transparent; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: 'Outfit', sans-serif; }
    .capsule-container { text-align: center; max-width: 360px; width: 100%; background: linear-gradient(135deg, rgba(123,44,191,0.6), rgba(0,245,212,0.2)); border: 1px solid rgba(0,245,212,0.4); border-radius: 24px; padding: 2rem; backdrop-filter: blur(12px); box-shadow: 0 0 30px rgba(123,44,191,0.3); }
    .letter-icon { font-size: 4.5rem; animation: floatLetter 2.5s ease-in-out infinite; margin-bottom: 0.8rem; filter: drop-shadow(0 0 15px rgba(0,245,212,0.5)); }
    @keyframes floatLetter { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
    .open-btn { background: linear-gradient(135deg, #7B2CBF, #00F5D4); color: #0A041A; border: none; border-radius: 14px; padding: 0.8rem 2rem; font-size: 1rem; font-weight: 600; cursor: pointer; box-shadow: 0 0 15px rgba(0,245,212,0.4); transition: all 0.2s; }
    .open-btn:hover { transform: scale(1.06); background: linear-gradient(135deg, #9D4EDD, #4CC9F0); }
    
    .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(10,4,26,0.5); backdrop-filter: blur(4px); justify-content: center; align-items: center; z-index: 999; }
    .modal-content { background: #1E0B36; color: #00F5D4; padding: 2.4rem 2rem; border-radius: 24px; text-align: center; max-width: 330px; width: 90%; box-shadow: 0 0 40px rgba(0,245,212,0.4); border: 2px solid #00F5D4; animation: popUp 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); position: relative; }
    @keyframes popUp { 0% { transform: scale(0.6); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
    .msg-box { font-size: 1.1rem; font-weight: 600; color: #F0E9FA; margin: 1.2rem 0; line-height: 1.5; }
    .close-btn { background: linear-gradient(135deg, #7B2CBF, #00F5D4); color: #0A041A; border: none; border-radius: 12px; padding: 0.65rem 2rem; font-weight: 600; font-size: 0.95rem; cursor: pointer; transition: transform 0.2s; box-shadow: 0 0 15px rgba(0,245,212,0.4); }
    .close-btn:hover { transform: scale(1.05); }
    </style>
    </head>
    <body>
    <div class="capsule-container">
        <div class="letter-icon">✉️</div>
        <div style="color:#FFD166; font-size:1.3rem; font-weight:700; margin-bottom:0.3rem;">Love Capsule Letter</div>
        <div style="color:#4CC9F0; font-size:0.75rem; font-weight:600; margin-bottom:1.5rem; letter-spacing:0.5px;">Open a note from me ✨</div>
        <button class="open-btn" onclick="openLetter()">Open Letter 💌</button>
    </div>

    <div class="modal" id="modal">
        <div class="modal-content">
            <div style="font-size: 2.2rem;">💌</div>
            <div style="font-size:0.7rem; color:#4CC9F0; text-transform:uppercase; font-weight:600; letter-spacing:1.5px; margin-top:0.4rem;" id="modalSub">Secret Note Unlocked</div>
            <div class="msg-box" id="secretMsg">...</div>
            <button class="close-btn" onclick="closeModal()">Got it</button>
        </div>
    </div>

    <script>
    const messages = [
        "The moon is beautiful, isn't it? I love you so much, my favorite rival!",
        "Keep crushing your goals today. I am so proud of you!",
        "You and me make an unstoppable team. Let us conquer everything!",
        "Sending you the biggest hug and all my energy today!",
        "No matter how tough it gets, I have your back forever.",
        "You are my favorite distraction and my greatest motivation.",
        "Go get them, soldier! Make me proud today and always.",
        "Everything is going to be amazing. I believe in you!",
        "So proud of the hard worker you are. You're truly incredible!"
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

# ======== TAB 2: BATTLE PHASE ========
elif st.session_state.active_tab == "⚔️ Battle Phase":
    st.markdown('<div class="section-title">Battle Phase: 5 Cards Choice & Tap/Untap ⚔️🃏</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #4CC9F0; font-size: 0.95rem; font-weight: 600; margin-bottom: 1.0rem;">Pick one of 5 cards every turn, then Tap to attack/heal! First to 0 HP loses. ✨</div>', unsafe_allow_html=True)
    
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
    body { background: transparent; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: 'Outfit', sans-serif; }
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
        box-shadow: 0 0 10px rgba(0,245,212,0.2); font-weight: 600;
    }
    .option-card:hover { transform: translateY(-5px) scale(1.05); border-color: #FFD166; box-shadow: 0 0 15px rgba(255,209,102,0.4); }
    
    /* Battle Phase */
    #battlePhase { display: none; }
    .players-container { display: flex; justify-content: space-around; align-items: center; gap: 15px; margin-bottom: 0.8rem; }
    .player-box { background: rgba(10,4,26,0.7); border: 2px solid rgba(0,245,212,0.3); border-radius: 14px; padding: 0.8rem; width: 48%; text-align: center; transition: all 0.3s; }
    .player-box.active-turn { border-color: #FFD166; box-shadow: 0 0 20px rgba(255,209,102,0.6); background: rgba(123,44,191,0.4); }
    
    .player-name { font-size: 0.85rem; color: #FFD166; font-weight: 700; margin-bottom: 0.3rem; }
    .hp-text { font-size: 0.8rem; color: #F0E9FA; font-weight: 600; margin-bottom: 0.6rem; }
    
    .card-container { perspective: 1000px; display: inline-block; cursor: pointer; }
    .mtg-card { 
        width: 110px; height: 150px; 
        background: linear-gradient(135deg, #7B2CBF, #1E0B36); 
        border: 2px solid #00F5D4; border-radius: 10px; 
        display: flex; flex-direction: column; align-items: center; justify-content: center; 
        transition: transform 0.4s cubic-bezier(0.34, 1.56, 0.64, 1), box-shadow 0.3s; 
        box-shadow: 0 0 15px rgba(0,245,212,0.3); user-select: none; margin: 0 auto; font-weight: 600;
    }
    .mtg-card.tapped { transform: rotate(90deg) scale(1.03); border-color: #FF6B6B; box-shadow: -12px 8px 20px rgba(0,0,0,0.6); }
    
    .turn-indicator { font-size: 0.95rem; color: #FFD166; font-weight: 700; margin-bottom: 0.5rem; }
    .action-btn { background: linear-gradient(135deg, #7B2CBF, #00F5D4); color: #0A041A; border: none; border-radius: 10px; padding: 0.5rem 1.5rem; font-size: 0.85rem; font-weight: 600; cursor: pointer; box-shadow: 0 0 15px rgba(0,245,212,0.4); transition: transform 0.2s; margin-top: 0.4rem; }
    .action-btn:hover { transform: scale(1.05); }
    .game-log { font-size: 0.75rem; color: #4CC9F0; margin-top: 0.6rem; font-style: italic; min-height: 30px; font-weight: 500; }
    
    /* CONGRATULATIONS WIN MODAL */
    .win-modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(10,4,26,0.85); backdrop-filter: blur(6px); justify-content: center; align-items: center; z-index: 9999; }
    .win-content { background: linear-gradient(135deg, #7B2CBF, #1E0B36); color: #F0E9FA; padding: 2.5rem 2rem; border-radius: 24px; text-align: center; max-width: 380px; width: 90%; box-shadow: 0 0 50px rgba(0,245,212,0.6); border: 3px solid #00F5D4; animation: popUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); }
    .win-title { font-size: 1.6rem; font-weight: 700; color: #FFD166; margin-bottom: 0.5rem; text-shadow: 0 0 15px rgba(255,209,102,0.6); }
    .win-msg { font-size: 1rem; font-weight: 600; margin-bottom: 1.5rem; color: #F0E9FA; line-height: 1.4; }
    .restart-btn { background: linear-gradient(135deg, #7B2CBF, #00F5D4); color: #0A041A; border: none; border-radius: 12px; padding: 0.7rem 2rem; font-weight: 600; font-size: 1rem; cursor: pointer; box-shadow: 0 0 15px rgba(0,245,212,0.4); transition: transform 0.2s; }
    .restart-btn:hover { transform: scale(1.06); }
    </style>
    </head>
    <body>
    <div class="duel-arena">
        <!-- PICKER PHASE (5 Cards including Matcha Boost) -->
        <div id="pickerPhase">
            <div style="color:#FFD166; font-size:1.1rem; font-weight:700; margin-bottom:0.3rem;" id="pickerTitle">Player 1 (Paweetida): Choose your Card! 🎴</div>
            <div style="font-size:0.75rem; color:#4CC9F0; margin-bottom:0.8rem; font-weight:600;">Select 1 of 5 cards to summon for this turn.</div>
            <div class="card-options">
                <div class="option-card" onclick="pickCard('💻', 'Coder Tech', 5)">
                    <div style="font-size:1.8rem;">💻</div>
                    <div style="font-size:0.65rem; font-weight:600; margin-top:3px;">Coder Tech</div>
                    <div style="font-size:0.5rem; color:#FFD166;">Attack: 5</div>
                </div>
                <div class="option-card" onclick="pickCard('🪖', 'Army Scout', 6)">
                    <div style="font-size:1.8rem;">🪖</div>
                    <div style="font-size:0.65rem; font-weight:600; margin-top:3px;">Army Scout</div>
                    <div style="font-size:0.5rem; color:#FFD166;">Attack: 6</div>
                </div>
                <div class="option-card" onclick="pickCard('👑', 'Rival Queen', 8)">
                    <div style="font-size:1.8rem;">👑</div>
                    <div style="font-size:0.65rem; font-weight:600; margin-top:3px;">Rival Queen</div>
                    <div style="font-size:0.5rem; color:#FFD166;">Attack: 8</div>
                </div>
                <div class="option-card" style="border-color: #00F5D4;" onclick="pickCard('🍵', 'Matcha Boost', 3)">
                    <div style="font-size:1.8rem;">🍵</div>
                    <div style="font-size:0.65rem; font-weight:600; margin-top:3px;">Matcha Boost</div>
                    <div style="font-size:0.5rem; color:#00F5D4;">Atk 3 & Heal 2</div>
                </div>
                <div class="option-card" style="border-color: #00F5D4;" onclick="pickCard('💖', 'Love Buff', -5)">
                    <div style="font-size:1.8rem;">💖</div>
                    <div style="font-size:0.65rem; font-weight:600; margin-top:3px;">Love Buff</div>
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
                            <div style="font-size: 0.6rem; color: #FFD166; font-weight: 600;" id="p1CardName">Ready</div>
                            <div style="font-size: 2.2rem;" id="p1Art">💻</div>
                            <div style="font-size: 0.55rem; color: #F0E9FA; font-weight: 500;" id="p1Status">Untapped</div>
                        </div>
                    </div>
                </div>
                
                <!-- Player 2 -->
                <div class="player-box" id="p2Box">
                    <div class="player-name">Player 2 (Dawis)</div>
                    <div class="hp-text">HP: <span id="p2Hp">20</span> ❤️</div>
                    <div class="card-container" onclick="playerTap(2)">
                        <div class="mtg-card" id="p2Card">
                            <div style="font-size: 0.6rem; color: #FFD166; font-weight: 600;" id="p2CardName">Ready</div>
                            <div style="font-size: 2.2rem;" id="p2Art">🪖</div>
                            <div style="font-size: 0.55rem; color: #F0E9FA; font-weight: 500;" id="p2Status">Untapped</div>
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

# ======== TAB 3: STATS ========
elif st.session_state.active_tab == "📊 Our Stats":
    st.markdown(f"""
    <div class="hero-section">
        <div style="font-size:2.2rem; margin-bottom:0.2rem">💜 🪖</div>
        <div class="hero-title">Paweetida & Dawis</div>
        <div class="hero-subtitle">OUR STORY · SINCE 27 JULY 2025 (first liked my IG story ✨)</div>
        <div style="margin-top:0.5rem; color:#FFD166; font-size:0.95rem; font-style:italic; font-weight:600;">
            "{stats['days_together']} days of loving you — and counting."
        </div>
    </div>
    """, unsafe_allow_html=True)

    components.html(f"""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700&display=swap" rel="stylesheet">
    <style>
    body {{ background: transparent; margin: 0; font-family: 'Outfit', sans-serif; display: flex; justify-content: center; align-items: center; width: 100%; padding: 0; }}
    .live-card {{
        background: linear-gradient(135deg, rgba(123,44,191,0.6), rgba(0,245,212,0.25));
        border: 1px solid rgba(76,201,240,0.4);
        border-radius: 20px;
        padding: 1.5rem 1rem;
        text-align: center;
        backdrop-filter: blur(12px);
        width: 100%;
        box-sizing: border-box;
        box-shadow: 0 0 35px rgba(0,245,212,0.25);
    }}
    .main-title {{ font-size: 0.75rem; color: #4CC9F0; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 0.3rem; font-weight: 600; }}
    .main-number {{ font-size: 3rem; font-weight: 700; color: #FFD166; line-height: 1; margin-bottom: 0.2rem; }}
    .main-unit {{ font-size: 0.95rem; color: #F0E9FA; margin-bottom: 1.2rem; font-weight: 600; }}
    .sub-grid {{ display: flex; justify-content: center; gap: 15px; }}
    .sub-box {{
        background: rgba(10,4,26,0.6);
        border: 1px solid rgba(0,245,212,0.3);
        border-radius: 12px;
        padding: 0.6rem 1.2rem;
        min-width: 90px;
        text-align: center;
    }}
    .sub-num {{ font-size: 1.4rem; font-weight: 700; color: #F0E9FA; line-height: 1.1; }}
    .sub-lbl {{ font-size: 0.7rem; color: #4CC9F0; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.2rem; font-weight: 600; }}
    </style>
    </head>
    <body>
        <div class="live-card">
            <div class="main-title">Since Day One (Official Couple) 💜</div>
            <div class="main-number">{stats['days_together']}</div>
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
        function updateCounter() {{
            const now = new Date();
            const diff = now - startDate;
            if (diff > 0) {{
                const hours = Math.floor((diff / (1000 * 60 * 60)) % 24);
                const mins = Math.floor((diff / 1000 / 60) % 60);
                const secs = Math.floor((diff / 1000) % 60);

                const hEl = document.getElementById("hoursNum");
                const mEl = document.getElementById("minsNum");
                const sEl = document.getElementById("secsNum");
                if (hEl) hEl.innerText = hours;
                if (mEl) mEl.innerText = mins;
                if (sEl) sEl.innerText = secs;
            }}
        }}
        setInterval(updateCounter, 1000);
        updateCounter();
        </script>
    </body>
    </html>
    """, height=205, scrolling=False)

    st.markdown("<div style='margin-top:0.4rem'></div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f'<div class="metric-card"><div class="metric-number">{stats["weeks_together"]}</div><div class="metric-label">Weeks Together</div><div style="font-size:0.8rem; color:#F0E9FA; font-weight:600; margin-top:0.3rem;">{stats["months_together"]} months of us 🌙</div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-number">{stats["days_to_anniversary"]}</div><div class="metric-label">Days to Anniversary</div><div style="font-size:0.8rem; color:#F0E9FA; font-weight:600; margin-top:0.3rem;">22 Aug {stats["next_anniversary"].year} 🎉</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-number">{stats["days_since_first"]}</div><div class="metric-label">Days Since We Met</div><div style="font-size:0.8rem; color:#F0E9FA; font-weight:600; margin-top:0.3rem;">27 Jul 2025 ✨</div></div>', unsafe_allow_html=True)
    with col4:
        st.markdown(f'<div class="metric-card"><div class="metric-number">{stats["days_since_army"]}</div><div class="metric-label">Days in Army Service</div><div style="font-size:0.8rem; color:#F0E9FA; font-weight:600; margin-top:0.3rem;">Dawis in Army 🪖</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='margin-top:0.8rem'></div>", unsafe_allow_html=True)

    milestones_df = get_milestones()
    if not milestones_df.empty:
        milestones_df['date'] = pd.to_datetime(milestones_df['date'])
        fig = go.Figure()
        
        positions = []
        y_values = []
        pos_options = ['top center', 'bottom center', 'top center', 'bottom center', 'top center', 'bottom center']
        y_options = [1.4, 0.6, 1.7, 0.3, 2.0, 0.0]
        
        for i in range(len(milestones_df)):
            positions.append(pos_options[i % len(pos_options)])
            y_values.append(y_options[i % len(y_options)])
            
        colors = ['#FFD166', '#00F5D4', '#4CC9F0', '#FF6B6B', '#C77DFF', '#FFE188', '#2EE8CC', '#FF9F1C']
        
        for i, row in milestones_df.iterrows():
            fig.add_trace(go.Scatter(
                x=[row['date']], y=[y_values[i]],
                mode='markers+text',
                marker=dict(size=14, color=colors[i % len(colors)], symbol='diamond'),
                text=[f"<b>{row['title']}</b><br>({row['date'].strftime('%d %b %Y')})"], 
                textposition=positions[i],
                textfont=dict(color='#F0E9FA', size=9, family='Outfit'),
                showlegend=False
            ))
            fig.add_shape(type='line',
                x0=row['date'], x1=row['date'],
                y0=1.0, y1=y_values[i],
                line=dict(color='rgba(0,245,212,0.3)', width=1, dash='dot'))
        
        fig.add_shape(type='line',
            x0=milestones_df['date'].min() - pd.Timedelta(days=25), 
            x1=milestones_df['date'].max() + pd.Timedelta(days=25),
            y0=1.0, y1=1.0,
            line=dict(color='rgba(0,245,212,0.8)', width=3))

        fig.update_layout(
            title=dict(text='Our Journey Together Timeline 🗺️', font=dict(color='#FFD166', size=13, family='Outfit')),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(visible=False, range=[-0.5, 2.5]), 
            xaxis=dict(showgrid=False, color='#4CC9F0', tickfont=dict(size=10)),
            height=320, margin=dict(l=20, r=20, t=40, b=15)
        )
        st.plotly_chart(fig, use_container_width=True)

    progress = max(0, min(1, 1 - (stats['days_to_anniversary'] / 365)))
    st.progress(progress)
    st.markdown(f'<div style="color:#4CC9F0; font-size:0.75rem; text-align:center; margin-top:0.3rem; font-weight:600;">{stats["days_to_anniversary"]} days until 22 August {stats["next_anniversary"].year}</div>', unsafe_allow_html=True)
