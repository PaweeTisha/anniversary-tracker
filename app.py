import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date
import plotly.graph_objects as go
import base64

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Tisha & Dawis 💜", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

# ---- CUSTOM CSS ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&display=swap');

:root {
    --purple-deep: #3D1A6E;
    --purple-mid: #6B3FA0;
    --purple-light: #B08FD4;
    --purple-pale: #F0E9FA;
    --army-green: #4A5C3A;
    --army-light: #7A8C6A;
    --gold: #C9A84C;
}

* { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #1A0A2E 0%, #2D1854 40%, #1E3A2A 100%);
    min-height: 100vh;
}

.block-container {
    padding-top: 3.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1250px !important;
}

.hero-section {
    background: linear-gradient(135deg, rgba(61,26,110,0.9), rgba(74,92,58,0.8));
    border-radius: 16px;
    padding: 1.2rem 1.5rem;
    text-align: center;
    border: 1px solid rgba(176,143,212,0.3);
    backdrop-filter: blur(10px);
    margin-bottom: 1rem;
}

.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2rem;
    font-weight: 700;
    color: #F0E9FA;
    margin: 0;
}

.hero-subtitle {
    font-size: 0.8rem;
    color: #B08FD4;
    margin-top: 0.2rem;
    letter-spacing: 1.5px;
    text-transform: uppercase;
}

.metric-card {
    background: linear-gradient(135deg, rgba(61,26,110,0.7), rgba(74,92,58,0.5));
    border: 1px solid rgba(176,143,212,0.25);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    backdrop-filter: blur(8px);
}

.metric-number {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2.4rem;
    font-weight: 700;
    color: #C9A84C;
    line-height: 1;
}

.metric-label {
    font-size: 0.75rem;
    color: #B08FD4;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin-top: 0.3rem;
}

.section-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #F0E9FA;
    margin-bottom: 0.6rem;
    border-bottom: 1px solid rgba(176,143,212,0.3);
    padding-bottom: 0.2rem;
}

.memory-card {
    background: rgba(61,26,110,0.5);
    border: 1px solid rgba(176,143,212,0.2);
    border-radius: 10px;
    padding: 0.8rem 1rem;
    margin-bottom: 0.5rem;
}

.army-badge {
    background: linear-gradient(135deg, rgba(74,92,58,0.8), rgba(122,140,106,0.4));
    border: 1px solid rgba(122,140,106,0.5);
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    color: #E8EDE4;
}

.stTextInput input, .stTextArea textarea, .stSelectbox select {
    background: rgba(61,26,110,0.5) !important;
    border: 1px solid rgba(176,143,212,0.3) !important;
    color: #F0E9FA !important;
    border-radius: 8px !important;
}

.stButton button {
    background: linear-gradient(135deg, #6B3FA0, #4A5C3A) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    padding: 0.4rem 1.2rem !important;
}

.stTabs [data-baseweb="tab"] { color: #B08FD4 !important; }
.stTabs [aria-selected="true"] { color: #F0E9FA !important; border-bottom: 2px solid #C9A84C !important; }
</style>
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

# ---- PASSWORD LOGIN ----
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        st.markdown("""
        <style>
        .block-container {
            padding-top: 1rem !important;
            padding-bottom: 1rem !important;
            max-width: 100% !important;
        }
        div[data-testid="stTextInput"] {
            position: absolute !important;
            width: 0px !important;
            height: 0px !important;
            overflow: hidden !important;
            opacity: 0 !important;
            z-index: -9999 !important;
            pointer-events: none !important;
        }
        </style>
        """, unsafe_allow_html=True)

        components.html("""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    background: transparent;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    text-align: center;
    padding: 1rem;
}
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
    background: linear-gradient(135deg, #B08FD4, #C9A84C);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: float 3s ease-in-out infinite;
    line-height: 1.1;
}
.and { font-family: 'Pacifico', cursive; font-size: 1.5rem; color: #C9A84C; margin: 0.1rem 0; }
.subtitle { font-size: 0.75rem; color: #B08FD4; letter-spacing: 2.5px; text-transform: uppercase; margin-top: 0.8rem; animation: shimmer 2s ease-in-out infinite; }
.stars { font-size: 1.2rem; letter-spacing: 0.4rem; margin: 0.5rem 0; animation: shimmer 2s ease-in-out infinite; }

.pin-section {
    margin-top: 1.5rem;
    background: rgba(61,26,110,0.6);
    border: 1px solid rgba(176,143,212,0.3);
    border-radius: 20px;
    padding: 1.5rem 2rem;
    max-width: 400px;
    width: 100%;
    backdrop-filter: blur(10px);
}
.pin-title { font-family: 'Pacifico', cursive; font-size: 1.2rem; color: #C9A84C; margin-bottom: 0.3rem; }
.pin-hint { font-size: 0.75rem; color: rgba(176,143,212,0.6); margin-bottom: 1.2rem; font-style: italic; }
.pin-boxes { display: flex; justify-content: center; gap: 0.6rem; margin-bottom: 1.2rem; }
.pin-box {
    width: 46px;
    height: 56px;
    border: 2px solid rgba(176,143,212,0.4);
    border-radius: 10px;
    background: rgba(61,26,110,0.5);
    font-size: 1.6rem;
    color: #C9A84C;
    text-align: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    outline: none;
    transition: all 0.2s;
    caret-color: transparent;
}
.pin-box:focus { border-color: #B08FD4; background: rgba(107,63,160,0.4); box-shadow: 0 0 10px rgba(176,143,212,0.3); transform: scale(1.05); }
.pin-box.filled { border-color: #C9A84C; animation: pop 0.2s ease; }
.pin-box.error { border-color: #E24B4A; animation: shake 0.4s ease; }
.enter-btn {
    background: linear-gradient(135deg, #6B3FA0, #4A5C3A);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 0.75rem 2.5rem;
    font-size: 0.9rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    transition: all 0.2s;
    letter-spacing: 0.5px;
}
.enter-btn:hover { background: linear-gradient(135deg, #8B5CC0, #5A7048); transform: translateY(-2px); box-shadow: 0 4px 15px rgba(107,63,160,0.4); }
.error-msg { color: #E24B4A; font-size: 0.8rem; margin-top: 0.8rem; display: none; }
.lock-icon { font-size: 1.8rem; margin-bottom: 0.5rem; animation: float 2.5s ease-in-out infinite; display: block; }
</style>
<style>
.floating-emoji { position: fixed; font-size: 1.5rem; animation: floatUp linear infinite; pointer-events: none; z-index: 0; opacity: 0.7; }
@keyframes floatUp { 0% { transform: translateY(100vh) rotate(0deg); opacity: 0; } 10% { opacity: 0.7; } 90% { opacity: 0.7; } 100% { transform: translateY(-10vh) rotate(360deg); opacity: 0; } }
</style>
</head>
<body>
    <div id="floaters"></div>
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
    </div>
    <script>
    const emojis = ['💐','🍀','🪐','🌜','🌹','🌻','☃️','🌟','💜','💚','🌷','🌹','💙','❄️','⭐','🤍','☃️','💛','🧡','❤️','🌻','🍀','🌷','🌐','🌻','💻','📡','🛜','🍀','💜','🤍','❄️'];
    const container = document.getElementById('floaters');
    for (let i = 0; i < 25; i++) {
        const el = document.createElement('div');
        el.className = 'floating-emoji';
        el.textContent = emojis[Math.floor(Math.random() * emojis.length)];
        el.style.left = Math.random() * 100 + 'vw';
        el.style.animationDuration = (5 + Math.random() * 8) + 's';
        el.style.animationDelay = (Math.random() * 8) + 's';
        el.style.fontSize = (1 + Math.random() * 1.5) + 'rem';
        container.appendChild(el);
    }
    </script>
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
""", height=720, scrolling=False)

        password = st.text_input("hidden_pin", type="password", key="pwd_backup", label_visibility="collapsed")
        if password == "220825":
            st.session_state.authenticated = True
            st.rerun()
        return False
    return True

if not check_password():
    st.stop()

# ---- INIT & STATS ----
init_db()
stats = calculate_stats()

# ---- TABS ----
tab_capsule, tab_battle, tab_stats, tab_memories, tab_timeline, tab_add = st.tabs(["💌 Love Capsule", "⚔️ Battle Phase", "📊 Our Stats", "💜 Memories", "📸 Timeline", "➕ Add Memory"])

# ======== TAB 0: LOVE CAPSULE ========
with tab_capsule:
    st.markdown('<div class="section-title">Love Capsule — Open a Secret Note 💌</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #B08FD4; font-size: 0.9rem; margin-bottom: 1.5rem;">Pick a letter to reveal a supportive message or a playful tease from your favorite rival! ✨</div>', unsafe_allow_html=True)
    
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
    <style>
    body { background: transparent; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: 'DM Sans', sans-serif; }
    .capsule-container { text-align: center; max-width: 360px; width: 100%; background: linear-gradient(135deg, rgba(61,26,110,0.7), rgba(74,92,58,0.5)); border: 1px solid rgba(176,143,212,0.3); border-radius: 24px; padding: 2rem; backdrop-filter: blur(12px); box-shadow: 0 15px 35px rgba(0,0,0,0.5); }
    .letter-icon { font-size: 4.5rem; animation: floatLetter 2.5s ease-in-out infinite; margin-bottom: 0.8rem; filter: drop-shadow(0 5px 15px rgba(201,168,76,0.3)); }
    @keyframes floatLetter { 0%, 100% { transform: translateY(0); } 50% { transform: translateY(-8px); } }
    .open-btn { background: linear-gradient(135deg, #6B3FA0, #C9A84C); color: white; border: none; border-radius: 14px; padding: 0.8rem 2rem; font-size: 1rem; font-weight: 700; cursor: pointer; box-shadow: 0 4px 15px rgba(107,63,160,0.5); transition: all 0.2s; }
    .open-btn:hover { transform: scale(1.06); background: linear-gradient(135deg, #7B4FB0, #D9B85C); }
    
    .modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(26, 10, 46, 0.25); backdrop-filter: blur(4px); justify-content: center; align-items: center; z-index: 999; }
    .modal-content { background: #FFFFFF; color: #3D1A6E; padding: 2.4rem 2rem; border-radius: 24px; text-align: center; max-width: 330px; width: 90%; box-shadow: 0 25px 50px rgba(61, 26, 110, 0.3); border: 1px solid rgba(176, 143, 212, 0.3); animation: popUp 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275); position: relative; }
    @keyframes popUp { 0% { transform: scale(0.6); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
    .msg-box { font-size: 1.05rem; font-weight: 700; color: #3D1A6E; margin: 1.2rem 0; line-height: 1.5; }
    .close-btn { background: #6B3FA0; color: white; border: none; border-radius: 12px; padding: 0.65rem 2rem; font-weight: 600; font-size: 0.95rem; cursor: pointer; transition: transform 0.2s; box-shadow: 0 4px 12px rgba(107,63,160,0.3); }
    .close-btn:hover { transform: scale(1.05); background: #5A3088; }
    </style>
    </head>
    <body>
    <div class="capsule-container">
        <div class="letter-icon">✉️</div>
        <div style="font-family:'Plus Jakarta Sans',sans-serif; color:#F0E9FA; font-size:1.3rem; font-weight:700; margin-bottom:0.3rem;">Love Capsule Letter</div>
        <div style="color:#B08FD4; font-size:0.75rem; margin-bottom:1.5rem; letter-spacing:0.5px;">Open a note from me ✨</div>
        <button class="open-btn" onclick="openLetter()">Open Letter 💌</button>
    </div>

    <div class="modal" id="modal">
        <div class="modal-content">
            <div style="font-size: 2.2rem;">💌</div>
            <div style="font-size:0.7rem; color:#6B3FA0; text-transform:uppercase; font-weight:700; letter-spacing:1.5px; margin-top:0.4rem;" id="modalSub">Secret Note Unlocked</div>
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

# ======== TAB 1: BATTLE PHASE (2-Player Hand & Spell Deck Duel) ========
with tab_battle:
    st.markdown('<div class="section-title">Battle Phase: 2-Player Spell Card Duel ⚔️🃏</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #B08FD4; font-size: 0.9rem; margin-bottom: 1.0rem;">Draw and choose spells from your hand to attack or heal. Take turns to win the duel! ✨</div>', unsafe_allow_html=True)
    
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@700&family=DM+Sans:wght@400;500&display=swap" rel="stylesheet">
    <style>
    body { background: transparent; display: flex; flex-direction: column; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: 'DM Sans', sans-serif; }
    .duel-arena { text-align: center; background: rgba(61,26,110,0.6); border: 1px solid rgba(176,143,212,0.3); border-radius: 20px; padding: 1.2rem 1.5rem; backdrop-filter: blur(10px); box-shadow: 0 10px 30px rgba(0,0,0,0.4); max-width: 500px; width: 100%; }
    
    .hp-container { display: flex; justify-content: space-around; margin-bottom: 0.8rem; font-size: 0.85rem; color: #F0E9FA; font-weight: 700; }
    .hp-box { background: rgba(26,10,46,0.6); padding: 0.4rem 0.9rem; border-radius: 8px; border: 1px solid rgba(176,143,212,0.3); }
    
    .turn-indicator { font-size: 0.95rem; color: #C9A84C; font-weight: 700; margin-bottom: 0.6rem; font-family: 'Plus Jakarta Sans', sans-serif; }
    
    .hand-container { display: flex; justify-content: center; gap: 10px; margin-bottom: 0.8rem; min-height: 130px; }
    .spell-card {
        width: 110px; height: 135px;
        background: linear-gradient(135deg, #3D1A6E, #6B3FA0);
        border: 2px solid #C9A84C;
        border-radius: 10px;
        display: flex; flex-direction: column; align-items: center; justify-content: space-between;
        cursor: pointer; transition: transform 0.2s, box-shadow 0.2s;
        padding: 8px; text-align: center;
        box-shadow: 0 4px 15px rgba(0,0,0,0.4);
    }
    .spell-card:hover { transform: translateY(-8px) scale(1.05); border-color: #F0E9FA; box-shadow: 0 8px 20px rgba(201,168,76,0.5); }
    .card-title { font-size: 0.7rem; color: #C9A84C; font-weight: 700; }
    .card-emoji { font-size: 2rem; }
    .card-effect { font-size: 0.55rem; color: #F0E9FA; line-height: 1.1; }
    
    .action-btn { background: linear-gradient(135deg, #6B3FA0, #C9A84C); color: white; border: none; border-radius: 10px; padding: 0.5rem 1.5rem; font-size: 0.85rem; font-weight: 700; cursor: pointer; box-shadow: 0 4px 12px rgba(107,63,160,0.4); transition: transform 0.2s; }
    .action-btn:hover { transform: scale(1.05); }
    
    .battle-log { font-size: 0.75rem; color: #B08FD4; margin-top: 0.6rem; min-height: 30px; font-style: italic; }
    </style>
    </head>
    <body>
    <div class="duel-arena">
        <div class="turn-indicator" id="turnText">Turn: Player 1 (Tisha 💻) — Draw your cards!</div>
        
        <div class="hp-container">
            <div class="hp-box">P1 HP: <span id="p1Hp">20</span> ❤️</div>
            <div class="hp-box">P2 HP: <span id="p2Hp">20</span> ❤️</div>
        </div>
        
        <div style="font-size: 0.75rem; color: #F0E9FA; font-weight: 600; text-align: left; margin-bottom: 4px;">Your Hand (Click a card to play):</div>
        <div class="hand-container" id="handContainer">
            <!-- Cards will be injected by JS -->
        </div>
        
        <div>
            <button class="action-btn" onclick="drawCards()">Draw Hand 🎴</button>
        </div>
        
        <div class="battle-log" id="battleLog">Click 'Draw Hand' to get your spells and start fighting! ✨</div>
    </div>

    <script>
    let p1Hp = 20;
    let p2Hp = 20;
    let currentTurn = 1; // 1 = Tisha, 2 = Dawis

    const deck = [
        { name: "Support Wave", emoji: "💖", type: "heal", val: 5, desc: "Restores 5 HP" },
        { name: "Army Strike", emoji: "🪖", type: "attack", val: 6, desc: "Deals 6 Damage" },
        { name: "Tease Burst", emoji: "😜", type: "attack", val: 8, desc: "Deals 8 Damage" },
        { name: "Shield Buff", emoji: "🛡️", type: "heal", val: 4, desc: "Restores 4 HP" },
        { name: "Ultimate Love", emoji: "🏆", type: "attack", val: 10, desc: "Deals 10 Damage" }
    ];

    function drawCards() {
        renderHand();
        document.getElementById('battleLog').innerText = `Player ${currentTurn} drew 3 spell cards! Choose one to play. 🃏`;
    }

    function getRandomCards() {
        let hand = [];
        for(let i=0; i<3; i++) {
            let randCard = deck[Math.floor(Math.random() * deck.length)];
            hand.push(randCard);
        }
        return hand;
    }

    function renderHand() {
        const container = document.getElementById('handContainer');
        container.innerHTML = "";
        let hand = getRandomCards();

        hand.forEach(card => {
            let cardEl = document.createElement('div');
            cardEl.className = 'spell-card';
            cardEl.innerHTML = `
                <div class="card-title">${card.name}</div>
                <div class="card-emoji">${card.emoji}</div>
                <div class="card-effect">${card.desc}</div>
            `;
            cardEl.onclick = () => playSpell(card);
            container.appendChild(cardEl);
        });
    }

    function playSpell(card) {
        if (p1Hp <= 0 || p2Hp <= 0) return;

        let logText = "";
        if (currentTurn === 1) {
            if (card.type === 'attack') {
                p2Hp = Math.max(0, p2Hp - card.val);
                logText = `P1 played ${card.name}! P2 takes ${card.val} damage! 💥`;
            } else {
                p1Hp = Math.min(20, p1Hp + card.val);
                logText = `P1 played ${card.name}! Restored ${card.val} HP! 💖`;
            }
            currentTurn = 2;
        } else {
            if (card.type === 'attack') {
                p1Hp = Math.max(0, p1Hp - card.val);
                logText = `P2 played ${card.name}! P1 takes ${card.val} damage! 💥`;
            } else {
                p2Hp = Math.min(20, p2Hp + card.val);
                logText = `P2 played ${card.name}! Restored ${card.val} HP! 💖`;
            }
            currentTurn = 1;
        }

        document.getElementById('p1Hp').innerText = p1Hp;
        document.getElementById('p2Hp').innerText = p2Hp;
        document.getElementById('turnText').innerText = `Turn: Player ${currentTurn} (${currentTurn === 1 ? 'Tisha 💻' : 'Dawis 🪖'})`;
        
        if (p1Hp <= 0 || p2Hp <= 0) {
            const winner = p1Hp <= 0 ? "Player 2 (Dawis 🪖)" : "Player 1 (Tisha 💻)";
            document.getElementById('battleLog').innerText = `🏆 Game Over! ${winner} wins the duel! 🎉`;
            document.getElementById('handContainer').innerHTML = "<div style='color:#C9A84C; font-weight:700; margin:auto;'>Victory! Refresh to play again.</div>";
        } else {
            document.getElementById('battleLog').innerText = `${logText} Click 'Draw Hand' for Player ${currentTurn}'s turn! ⏭️`;
            document.getElementById('handContainer').innerHTML = "<div style='color:#B08FD4; font-size:0.8rem; margin:auto; font-style:italic;'>Turn ended. Click 'Draw Hand' below!</div>";
        }
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
        <div style="margin-top:0.5rem; color:#C9A84C; font-family:'DM Sans',sans-serif; font-size:0.9rem; font-style:italic;">
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
        background: linear-gradient(135deg, rgba(61,26,110,0.7), rgba(74,92,58,0.5));
        border: 1px solid rgba(176,143,212,0.25);
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        text-align: center;
        backdrop-filter: blur(8px);
        width: 100%;
        max-width: 1000px;
    }
    .main-title { font-size: 0.75rem; color: #B08FD4; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.3rem; font-weight: 500; }
    .main-number { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 2.8rem; font-weight: 700; color: #C9A84C; line-height: 1; margin-bottom: 0.2rem; }
    .main-unit { font-size: 0.9rem; color: #F0E9FA; margin-bottom: 1rem; font-weight: 500; }
    .sub-grid { display: flex; justify-content: center; gap: 10px; }
    .sub-box {
        background: rgba(61,26,110,0.5);
        border: 1px solid rgba(176,143,212,0.3);
        border-radius: 8px;
        padding: 0.5rem 0.8rem;
        min-width: 80px;
        text-align: center;
    }
    .sub-num { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.3rem; font-weight: 700; color: #F0E9FA; line-height: 1.1; }
    .sub-lbl { font-size: 0.7rem; color: #B08FD4; text-transform: uppercase; letter-spacing: 1px; margin-top: 0.2rem; }
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
                    <div class="sub-num" id="secsNum" style="color: #C9A84C;">0</div>
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
            <div style="font-size:1.4rem; font-family:'Playfair Display',serif; color:#C9A84C; font-weight:700;">{stats['days_since_army']}</div>
            <div style="font-size:0.7rem; letter-spacing:1px; text-transform:uppercase; color:#7A8C6A;">Days in Service</div>
            <div style="font-size:0.8rem; margin-top:0.2rem; color:#E8EDE4;">Dawis in Australian Army (20 Apr 2026)</div>
        </div>""", unsafe_allow_html=True)

    with col_b:
        milestones_df = get_milestones()
        if not milestones_df.empty:
            milestones_df['date'] = pd.to_datetime(milestones_df['date'])
            fig = go.Figure()
            colors = ['#C9A84C', '#B08FD4', '#7A8C6A']
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
                line=dict(color='rgba(176,143,212,0.5)', width=2))

            fig.update_layout(
                title=dict(text='Our Journey Together', font=dict(color='#F0E9FA', size=11)),
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(visible=False, range=[0.3, 1.7]), xaxis=dict(showgrid=False, color='#B08FD4'),
                height=150, margin=dict(l=10, r=10, t=30, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)

    progress = max(0, min(1, 1 - (stats['days_to_anniversary'] / 365)))
    st.progress(progress)
    st.markdown(f'<div style="color:#B08FD4; font-size:0.75rem; text-align:center; margin-top:0.3rem;">{stats["days_to_anniversary"]} days until 22 August {stats["next_anniversary"].year}</div>', unsafe_allow_html=True)

# ======== TAB 3: MEMORIES ========
with tab_memories:
    st.markdown('<div class="section-title">Our Memories 💜</div>', unsafe_allow_html=True)
    memories_df = get_memories()
    if memories_df.empty:
        st.markdown('<div style="text-align:center; color:#B08FD4; padding:1.5rem;">No memories yet — add your first one!</div>', unsafe_allow_html=True)
    else:
        categories = ['All'] + list(memories_df['category'].unique())
        selected_cat = st.selectbox("Filter by category", categories, label_visibility="collapsed")
        filtered_df = memories_df[memories_df['category'] == selected_cat] if selected_cat != 'All' else memories_df
        for _, row in filtered_df.iterrows():
            col_mem, col_del = st.columns([11, 1])
            with col_mem:
                st.markdown(f'<div class="memory-card"><span style="color:#C9A84C; font-size:0.7rem;">{row["date"]}</span> <b style="font-size:0.95rem;">{row["emoji"]} {row["title"]}</b> — <span style="color:#B08FD4">{row["description"] or ""}</span></div>', unsafe_allow_html=True)
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
        background: linear-gradient(to bottom, #C9A84C, #B08FD4, #7A8C6A);
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
        background-color: #C9A84C;
        border: 3px solid #3D1A6E;
        top: 15px;
        border-radius: 50%;
        z-index: 1;
    }}
    .left-item {{ left: 0; text-align: right; }}
    .right-item {{ left: 50%; text-align: left; }}
    .right-item::after {{ left: -7px; }}
    
    .timeline-content {{
        padding: 12px 18px;
        background: rgba(61, 26, 110, 0.85);
        border: 1px solid rgba(176, 143, 212, 0.3);
        border-radius: 12px;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        display: inline-block;
        cursor: pointer;
        position: relative;
        transition: transform 0.2s;
    }}
    .timeline-content:hover {{
        transform: scale(1.05);
        border-color: #C9A84C;
    }}
    
    .timeline-date {{
        font-size: 0.65rem;
        color: #C9A84C;
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
        background: #2D1854;
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
        color: #1A1A2E;
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
