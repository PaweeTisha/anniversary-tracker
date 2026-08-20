import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date
import plotly.graph_objects as go
import plotly.express as px
import os

# ---- PAGE CONFIG ----
st.set_page_config(
    page_title="Tisha & Dawis 💜",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---- CUSTOM CSS ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=Inter:wght@300;400;500;600&display=swap');

:root {
    --purple-deep: #3D1A6E;
    --purple-mid: #6B3FA0;
    --purple-light: #B08FD4;
    --purple-pale: #F0E9FA;
    --army-green: #4A5C3A;
    --army-light: #7A8C6A;
    --army-pale: #E8EDE4;
    --gold: #C9A84C;
    --white: #FAFAFA;
    --text-dark: #1A1A2E;
}

* { font-family: 'DM Sans', sans-serif; }

.stApp {
    background: linear-gradient(135deg, #1A0A2E 0%, #2D1854 40%, #1E3A2A 100%);
    min-height: 100vh;
}

.hero-section {
    background: linear-gradient(135deg, rgba(61,26,110,0.9), rgba(74,92,58,0.8));
    border-radius: 20px;
    padding: 3rem 2rem;
    text-align: center;
    border: 1px solid rgba(176,143,212,0.3);
    backdrop-filter: blur(10px);
    margin-bottom: 2rem;
}

.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 3rem;
    font-weight: 700;
    color: #F0E9FA;
    margin: 0;
    letter-spacing: -1px;
}

.hero-subtitle {
    font-size: 1rem;
    color: #B08FD4;
    margin-top: 0.5rem;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.metric-card {
    background: linear-gradient(135deg, rgba(61,26,110,0.7), rgba(74,92,58,0.5));
    border: 1px solid rgba(176,143,212,0.25);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    backdrop-filter: blur(8px);
    transition: transform 0.2s;
}

.metric-card:hover { transform: translateY(-4px); }

.metric-number {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 3.5rem;
    font-weight: 700;
    color: #C9A84C;
    line-height: 1;
}

.metric-label {
    font-size: 0.8rem;
    color: #B08FD4;
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 0.5rem;
}

.metric-desc {
    font-size: 0.85rem;
    color: #E0D4F5;
    margin-top: 0.3rem;
}

.section-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.4rem;
    font-weight: 600;
    color: #F0E9FA;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(176,143,212,0.3);
    padding-bottom: 0.5rem;
    letter-spacing: -0.3px;
}

.memory-card {
    background: rgba(61,26,110,0.5);
    border: 1px solid rgba(176,143,212,0.2);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    backdrop-filter: blur(6px);
}

.memory-date {
    font-size: 0.75rem;
    color: #C9A84C;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.memory-title {
    font-size: 1rem;
    font-weight: 600;
    color: #F0E9FA;
    margin: 0.25rem 0;
}

.memory-desc {
    font-size: 0.85rem;
    color: #B08FD4;
}

.emoji-tag {
    font-size: 1.2rem;
    margin-right: 0.5rem;
}

.countdown-box {
    background: linear-gradient(135deg, rgba(201,168,76,0.15), rgba(176,143,212,0.1));
    border: 1px solid rgba(201,168,76,0.4);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
}

.countdown-number {
    font-family: 'Playfair Display', serif;
    font-size: 2.5rem;
    color: #C9A84C;
    font-weight: 700;
}

.countdown-label {
    font-size: 0.8rem;
    color: #B08FD4;
    text-transform: uppercase;
    letter-spacing: 1.5px;
}

.army-badge {
    background: linear-gradient(135deg, rgba(74,92,58,0.8), rgba(122,140,106,0.4));
    border: 1px solid rgba(122,140,106,0.5);
    border-radius: 12px;
    padding: 1rem 1.5rem;
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
    padding: 0.5rem 1.5rem !important;
}

.stButton button:hover {
    background: linear-gradient(135deg, #8B5CC0, #5A7048) !important;
    transform: translateY(-1px) !important;
}

div[data-testid="stMetricValue"] {
    color: #C9A84C !important;
    font-family: 'Playfair Display', serif !important;
}

.stTabs [data-baseweb="tab"] {
    color: #B08FD4 !important;
}

.stTabs [aria-selected="true"] {
    color: #F0E9FA !important;
    border-bottom: 2px solid #C9A84C !important;
}
</style>
""", unsafe_allow_html=True)

# ---- DATABASE ----
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
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS milestones (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT,
        type TEXT DEFAULT 'milestone'
    )''')
    # Insert default milestones if empty
    c.execute("SELECT COUNT(*) FROM milestones")
    if c.fetchone()[0] == 0:
        default_milestones = [
            ("First Like on Story 🚌", "2025-07-27", "กดไลค์สตอรี่ครั้งแรก — บนรถบัส", "start"),
            ("Official Couple 💜", "2025-08-22", "วันที่เป็นแฟนกันอย่างเป็นทางการ", "anniversary"),
            ("Dawis Enlists Army 🪖", "2026-04-20", "วันที่ Dawis เข้า Australian Army", "milestone"),
        ]
        c.executemany("INSERT INTO milestones (title, date, description, type) VALUES (?,?,?,?)", default_milestones)
    conn.commit()
    conn.close()

def get_memories():
    conn = sqlite3.connect('anniversary.db')
    df = pd.read_sql_query("SELECT * FROM memories ORDER BY date DESC", conn)
    conn.close()
    return df

def add_memory(title, description, date_val, category, emoji):
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute("INSERT INTO memories (title, description, date, category, emoji) VALUES (?,?,?,?,?)",
              (title, description, str(date_val), category, emoji))
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

# ---- CALCULATIONS ----
def calculate_stats():
    today = date.today()
    start_date = date(2025, 7, 27)
    official_date = date(2025, 8, 22)
    army_date = date(2026, 4, 20)
    next_anniversary = date(2026, 8, 22)
    if today > next_anniversary:
        next_anniversary = date(today.year + 1, 8, 22)

    days_since_first = (today - start_date).days
    days_together = (today - official_date).days
    days_to_anniversary = (next_anniversary - today).days
    days_since_army = (today - army_date).days if today >= army_date else 0

    weeks_together = days_together // 7
    months_together = days_together // 30

    return {
        "days_since_first": days_since_first,
        "days_together": days_together,
        "weeks_together": weeks_together,
        "months_together": months_together,
        "days_to_anniversary": days_to_anniversary,
        "days_since_army": days_since_army,
        "next_anniversary": next_anniversary,
        "official_date": official_date,
    }

# ---- PASSWORD LOGIN ----
def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if not st.session_state.authenticated:
        components.html("""
<!DOCTYPE html>
<html>
<head>
<link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Plus+Jakarta+Sans:wght@300;400;600;700&display=swap" rel="stylesheet">
<style>
* { margin: 0; padding: 0; box-sizing: border-box; }
body {
    background: linear-gradient(135deg, #1A0A2E 0%, #2D1854 40%, #1E3A2A 100%);
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    text-align: center;
    padding: 2rem;
}
@keyframes bounce {
    0%, 100% { transform: translateY(0px) rotate(-3deg); }
    25% { transform: translateY(-20px) rotate(3deg); }
    50% { transform: translateY(-10px) rotate(-2deg); }
    75% { transform: translateY(-25px) rotate(4deg); }
}
@keyframes bounce2 {
    0%, 100% { transform: translateY(0px) rotate(3deg); }
    25% { transform: translateY(-25px) rotate(-3deg); }
    50% { transform: translateY(-12px) rotate(2deg); }
    75% { transform: translateY(-18px) rotate(-4deg); }
}
@keyframes heartbeat {
    0%, 100% { transform: scale(1); }
    15% { transform: scale(1.3); }
    30% { transform: scale(1); }
    45% { transform: scale(1.2); }
    60% { transform: scale(1); }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}
@keyframes shimmer {
    0%, 100% { opacity: 0.6; }
    50% { opacity: 1; }
}
@keyframes shake {
    0%, 100% { transform: translateX(0); }
    20% { transform: translateX(-10px); }
    40% { transform: translateX(10px); }
    60% { transform: translateX(-8px); }
    80% { transform: translateX(8px); }
}
@keyframes pop {
    0% { transform: scale(1); }
    50% { transform: scale(1.2); }
    100% { transform: scale(1); }
}
.chars { display: flex; justify-content: center; align-items: center; gap: 2rem; margin-bottom: 1.5rem; }
.girl { font-size: 5rem; animation: bounce 1.4s ease-in-out infinite; display: inline-block; }
.heart { font-size: 3.5rem; animation: heartbeat 1.2s ease-in-out infinite; display: inline-block; }
.soldier { font-size: 5rem; animation: bounce2 1.6s ease-in-out infinite; display: inline-block; }
.title {
    font-family: 'Pacifico', cursive;
    font-size: 4rem;
    background: linear-gradient(135deg, #B08FD4, #C9A84C);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: float 3s ease-in-out infinite;
    line-height: 1.2;
}
.and { font-family: 'Pacifico', cursive; font-size: 2rem; color: #C9A84C; margin: 0.3rem 0; }
.subtitle {
    font-size: 0.85rem;
    color: #B08FD4;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 1rem;
    animation: shimmer 2s ease-in-out infinite;
}
.stars { font-size: 1.5rem; letter-spacing: 0.5rem; margin: 1rem 0; animation: shimmer 2s ease-in-out infinite; }

.pin-section {
    margin-top: 2rem;
    background: rgba(61,26,110,0.6);
    border: 1px solid rgba(176,143,212,0.3);
    border-radius: 24px;
    padding: 2rem 2.5rem;
    max-width: 420px;
    width: 100%;
    backdrop-filter: blur(10px);
}
.pin-title {
    font-family: 'Pacifico', cursive;
    font-size: 1.4rem;
    color: #C9A84C;
    margin-bottom: 0.5rem;
}
.pin-hint {
    font-size: 0.8rem;
    color: rgba(176,143,212,0.6);
    margin-bottom: 1.5rem;
    font-style: italic;
}
.pin-boxes {
    display: flex;
    justify-content: center;
    gap: 0.75rem;
    margin-bottom: 1.5rem;
}
.pin-box {
    width: 52px;
    height: 62px;
    border: 2px solid rgba(176,143,212,0.4);
    border-radius: 12px;
    background: rgba(61,26,110,0.5);
    font-size: 1.8rem;
    color: #C9A84C;
    text-align: center;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 700;
    outline: none;
    transition: all 0.2s;
    caret-color: transparent;
}
.pin-box:focus {
    border-color: #B08FD4;
    background: rgba(107,63,160,0.4);
    box-shadow: 0 0 12px rgba(176,143,212,0.3);
    transform: scale(1.05);
}
.pin-box.filled {
    border-color: #C9A84C;
    animation: pop 0.2s ease;
}
.pin-box.error {
    border-color: #E24B4A;
    animation: shake 0.4s ease;
}
.enter-btn {
    background: linear-gradient(135deg, #6B3FA0, #4A5C3A);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 0.85rem 3rem;
    font-size: 1rem;
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-weight: 600;
    cursor: pointer;
    width: 100%;
    transition: all 0.2s;
    letter-spacing: 0.5px;
}
.enter-btn:hover {
    background: linear-gradient(135deg, #8B5CC0, #5A7048);
    transform: translateY(-2px);
    box-shadow: 0 4px 20px rgba(107,63,160,0.4);
}
.error-msg {
    color: #E24B4A;
    font-size: 0.85rem;
    margin-top: 1rem;
    display: none;
}
.lock-icon { font-size: 2rem; margin-bottom: 1rem; animation: float 2.5s ease-in-out infinite; display: block; }
</style>
</head>
<style>
.floating-emoji {
    position: fixed;
    font-size: 1.5rem;
    animation: floatUp linear infinite;
    pointer-events: none;
    z-index: 0;
    opacity: 0.7;
}
@keyframes floatUp {
    0% { transform: translateY(100vh) rotate(0deg); opacity: 0; }
    10% { opacity: 0.7; }
    90% { opacity: 0.7; }
    100% { transform: translateY(-10vh) rotate(360deg); opacity: 0; }
}
</style>
<body>
    <!-- Floating emojis background -->
    <div id="floaters"></div>

    <div style="position:relative; z-index:1;">
    <div class="chars">
        <span class="girl">💻</span>
        <span class="heart">💜</span>
        <span class="soldier">🪖</span>
    </div>
    <div class="stars">🍀 💜 🍀 💚 🍀</div>
    <div class="title">Paweetida</div>
    <div class="and">&amp;</div>
    <div class="title">Mr. Dawis</div>
    <div class="subtitle">Our Private Little World 💜</div>
    </div>

    <script>
    const emojis = ['💜','💚','💙','🤍','💛','🧡','❤️','🍀','🌐','💻','📡','🛜','🍀','💜','💚'];
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
            window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'correct'}, '*');
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
""", height=680, scrolling=False)

        # รับ value จาก component
        if "pin_submitted" not in st.session_state:
            st.session_state.pin_submitted = False

        # fallback input ซ่อนไว้
        password = st.text_input("backup", type="password", key="pwd_backup", label_visibility="collapsed")
        if password == "220825":
            st.session_state.authenticated = True
            st.rerun()

        return False
    return True

if not check_password():
    st.stop()

# ---- INIT ----
init_db()
stats = calculate_stats()

# ---- HERO ----
st.markdown(f"""
<div class="hero-section">
    <div style="font-size:3rem; margin-bottom:0.5rem">💜 🪖</div>
    <div class="hero-title">Paweetida & Mr. Dawis</div>
    <div class="hero-subtitle">OUR STORY · SINCE 27 JULY 2025 (the day you liked my story 🚌)</div>
    <div style="margin-top:1.5rem; color:#C9A84C; font-family:'DM Sans',sans-serif; font-size:1.1rem; font-style:italic; font-weight:300; letter-spacing:0.3px;">
        "{stats['days_together']} days of loving you — and counting."
    </div>
</div>
""", unsafe_allow_html=True)

# ---- TABS ----
tab1, tab2, tab3, tab4 = st.tabs(["📊 Our Stats", "💜 Memories", "🗓️ Timeline", "➕ Add Memory"])

# ======== TAB 1: STATS ========
with tab1:
    st.markdown('<div class="section-title">Our Story in Numbers</div>', unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{stats['days_together']}</div>
            <div class="metric-label">Days Together</div>
            <div class="metric-desc">Since 22 Aug 2025 💜</div>
        </div>""", unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{stats['weeks_together']}</div>
            <div class="metric-label">Weeks Together</div>
            <div class="metric-desc">{stats['months_together']} months of us 🌙</div>
        </div>""", unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{stats['days_to_anniversary']}</div>
            <div class="metric-label">Days to Anniversary</div>
            <div class="metric-desc">22 Aug {stats['next_anniversary'].year} 🎉</div>
        </div>""", unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">{stats['days_since_first']}</div>
            <div class="metric-label">Days Since We Met</div>
            <div class="metric-desc">27 Jul 2025 on the bus 🚌</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Army section
    col_a, col_b = st.columns([1, 2])
    with col_a:
        st.markdown(f"""
        <div class="army-badge">
            <div style="font-size:2.5rem">🪖</div>
            <div style="font-size:1.8rem; font-family:'Playfair Display',serif; color:#C9A84C; font-weight:700;">{stats['days_since_army']}</div>
            <div style="font-size:0.8rem; letter-spacing:1.5px; text-transform:uppercase; color:#7A8C6A; margin-top:0.3rem;">Days in Service</div>
            <div style="font-size:0.85rem; margin-top:0.5rem; color:#E8EDE4;">Dawis joined Australian Army<br>20 April 2026</div>
        </div>""", unsafe_allow_html=True)

    with col_b:
        # Timeline chart
        milestones_df = get_milestones()
        if not milestones_df.empty:
            milestones_df['date'] = pd.to_datetime(milestones_df['date'])
            milestones_df['y'] = 1

            fig = go.Figure()
            colors = ['#C9A84C', '#B08FD4', '#7A8C6A']
            # สลับ y position และ text position เพื่อไม่ให้ซ้อนทับกัน
            y_positions = [1.0, 1.15, 0.85, 1.2, 0.8]
            text_positions = ['top center', 'top center', 'bottom center', 'top center', 'bottom center']
            
            for i, row in milestones_df.iterrows():
                color = colors[i % len(colors)]
                y_pos = y_positions[i % len(y_positions)]
                txt_pos = text_positions[i % len(text_positions)]
                fig.add_trace(go.Scatter(
                    x=[row['date']], y=[y_pos],
                    mode='markers+text',
                    marker=dict(size=16, color=color, symbol='diamond'),
                    text=[row['title']],
                    textposition=txt_pos,
                    textfont=dict(color='#F0E9FA', size=10),
                    hovertemplate=f"<b>{row['title']}</b><br>{row['description']}<extra></extra>",
                    showlegend=False
                ))
                # เส้นเชื่อมจาก marker ลงมาที่ baseline
                fig.add_shape(type='line',
                    x0=row['date'], x1=row['date'],
                    y0=1.0, y1=y_pos,
                    line=dict(color=color, width=1, dash='dot'))

            fig.add_shape(type='line',
                x0=milestones_df['date'].min(), x1=date.today(),
                y0=1, y1=1,
                line=dict(color='rgba(176,143,212,0.4)', width=2))

            fig.update_layout(
                title=dict(text='Our Journey Together', font=dict(color='#F0E9FA', size=14, family='Plus Jakarta Sans')),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                yaxis=dict(visible=False, range=[0.6, 1.5]),
                xaxis=dict(showgrid=False, color='#B08FD4'),
                height=260,
                margin=dict(l=10, r=10, t=40, b=10)
            )
            st.plotly_chart(fig, use_container_width=True)

    # Progress to next anniversary
    st.markdown('<div class="section-title" style="margin-top:1rem">Countdown to Anniversary 🎉</div>', unsafe_allow_html=True)
    progress = max(0, min(1, 1 - (stats['days_to_anniversary'] / 365)))
    st.progress(progress)
    st.markdown(f'<div style="color:#B08FD4; font-size:0.85rem; text-align:center;">{stats["days_to_anniversary"]} days until 22 August {stats["next_anniversary"].year}</div>', unsafe_allow_html=True)

# ======== TAB 2: MEMORIES ========
with tab2:
    st.markdown('<div class="section-title">Our Memories 💜</div>', unsafe_allow_html=True)
    memories_df = get_memories()

    if memories_df.empty:
        st.markdown("""
        <div style="text-align:center; color:#B08FD4; padding:3rem;">
            <div style="font-size:3rem">💜</div>
            <div style="font-size:1.1rem; margin-top:1rem;">No memories yet — add your first one!</div>
        </div>""", unsafe_allow_html=True)
    else:
        # Filter by category
        categories = ['All'] + list(memories_df['category'].unique())
        selected_cat = st.selectbox("Filter by category", categories)
        if selected_cat != 'All':
            filtered_df = memories_df[memories_df['category'] == selected_cat]
        else:
            filtered_df = memories_df

        for _, row in filtered_df.iterrows():
            col_mem, col_del = st.columns([10, 1])
            with col_mem:
                st.markdown(f"""
                <div class="memory-card">
                    <div class="memory-date">{row['date']}</div>
                    <div class="memory-title"><span class="emoji-tag">{row['emoji']}</span>{row['title']}</div>
                    <div class="memory-desc">{row['description'] or ''}</div>
                    <div style="margin-top:0.5rem; display:inline-block; background:rgba(176,143,212,0.2); border-radius:20px; padding:2px 10px; font-size:0.75rem; color:#B08FD4;">{row['category']}</div>
                </div>""", unsafe_allow_html=True)
            with col_del:
                if st.button("🗑️", key=f"del_{row['id']}", help="Delete this memory"):
                    delete_memory(row['id'])
                    st.rerun()

# ======== TAB 3: TIMELINE ========
with tab3:
    st.markdown('<div class="section-title">Our Timeline 🗓️</div>', unsafe_allow_html=True)
    milestones_df = get_milestones()
    memories_df = get_memories()

    all_events = []
    for _, row in milestones_df.iterrows():
        all_events.append({
            'date': row['date'],
            'title': row['title'],
            'desc': row['description'],
            'type': 'milestone',
            'color': '#C9A84C'
        })

    for _, row in memories_df.iterrows():
        all_events.append({
            'date': row['date'],
            'title': f"{row['emoji']} {row['title']}",
            'desc': row['description'],
            'type': row['category'],
            'color': '#B08FD4'
        })

    all_events = sorted(all_events, key=lambda x: x['date'], reverse=True)

    for event in all_events:
        border_color = event['color']
        st.markdown(f"""
        <div style="border-left: 3px solid {border_color}; padding: 0.75rem 1rem; margin-bottom: 1rem; background: rgba(61,26,110,0.3); border-radius: 0 12px 12px 0;">
            <div style="font-size:0.75rem; color:{border_color}; text-transform:uppercase; letter-spacing:1px;">{event['date']} · {event['type']}</div>
            <div style="font-size:1rem; font-weight:600; color:#F0E9FA; margin-top:0.2rem;">{event['title']}</div>
            <div style="font-size:0.85rem; color:#B08FD4; margin-top:0.2rem;">{event['desc'] or ''}</div>
        </div>""", unsafe_allow_html=True)

# ======== TAB 4: ADD MEMORY ========
with tab4:
    st.markdown('<div class="section-title">Add a New Memory ➕</div>', unsafe_allow_html=True)

    col_form1, col_form2 = st.columns([3, 2])
    with col_form1:
        mem_title = st.text_input("Memory title *", placeholder="e.g. First trip to Queenstown")
        mem_desc = st.text_area("Description", placeholder="Tell the story...", height=100)
        mem_date = st.date_input("Date", value=date.today())

    with col_form2:
        mem_category = st.selectbox("Category", [
            "date night", "travel", "milestone", "everyday",
            "food", "special occasion", "army life", "other"
        ])
        mem_emoji = st.selectbox("Emoji", [
            "💜", "🥰", "✈️", "🍜", "🎉", "🌙", "🪖", "🏔️", "🌸", "⭐", "🎂", "🏖️"
        ])
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("Save Memory 💜", use_container_width=True):
            if mem_title:
                add_memory(mem_title, mem_desc, mem_date, mem_category, mem_emoji)
                st.success("Memory saved! 💜")
                st.balloons()
                st.rerun()
            else:
                st.error("Please add a title!")

    # Quick memory suggestions
    st.markdown('<div class="section-title" style="margin-top:1.5rem">Quick Add Suggestions</div>', unsafe_allow_html=True)
    suggestions = [
        ("🚌", "Met on the bus", "date night"),
        ("💜", "First date", "date night"),
        ("🏔️", "Queenstown trip", "travel"),
        ("🪖", "Saying goodbye before Army", "army life"),
        ("🇨🇳", "Yunnan trip", "travel"),
    ]
    cols = st.columns(len(suggestions))
    for i, (emoji, title, cat) in enumerate(suggestions):
        with cols[i]:
            if st.button(f"{emoji} {title}", key=f"quick_{i}", use_container_width=True):
                add_memory(title, "", date.today(), cat, emoji)
                st.success(f"Added: {title}!")
                st.rerun()
