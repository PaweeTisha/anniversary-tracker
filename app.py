import streamlit as st
import streamlit.components.v1 as components
from datetime import datetime, date

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Paweetida & Dawis 💜", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

# ---- CUSTOM CSS ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@600;700&family=DM+Sans:wght@400;500&display=swap');

.stApp {
    background: linear-gradient(135deg, #050210 0%, #10072B 30%, #031B26 70%, #020C1B 100%);
    min-height: 100vh;
}
div[data-testid="stTextInput"]:has(input[aria-label="hidden_welcome"]),
div[data-testid="stTextInput"]:has(input[aria-label="hidden_pin"]) {
    display: none !important;
    height: 0px !important;
    visibility: hidden !important;
}

.hero-section {
    background: linear-gradient(135deg, rgba(123,44,191,0.6), rgba(0,245,212,0.25));
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    border: 1px solid rgba(76,201,240,0.4);
    backdrop-filter: blur(12px);
    margin-bottom: 1.5rem;
    box-shadow: 0 0 35px rgba(0,245,212,0.25);
}

.hero-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #FFD166;
}

.section-title {
    font-family: 'Plus Jakarta Sans', sans-serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: #F0E9FA;
    margin-bottom: 0.8rem;
    border-bottom: 1px solid rgba(0,245,212,0.4);
    padding-bottom: 0.3rem;
}
</style>
""", unsafe_allow_html=True)

# ---- STATS LOGIC ----
def calculate_stats():
    today = date.today()
    start_date = date(2025, 7, 27)
    official_date = date(2025, 8, 22)
    army_date = date(2026, 4, 20)
    return {
        "days_since_first": (today - start_date).days,
        "days_together": (today - official_date).days,
        "weeks_together": (today - official_date).days // 7,
        "months_together": (today - official_date).days // 30,
        "days_since_army": (today - army_date).days if today >= army_date else 0,
    }

# ---- PASSWORD LOGIN & WELCOME SCREEN ----
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
        <link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Plus+Jakarta+Sans:wght@700&display=swap" rel="stylesheet">
        <style>
        body { background: transparent; display: flex; flex-direction: column; align-items: center; justify-content: center; height: 100vh; margin: 0; font-family: 'Plus Jakarta Sans', sans-serif; text-align: center; color: white; }
        .title { font-family: 'Pacifico', cursive; font-size: 3rem; color: #00F5D4; text-shadow: 0 0 15px rgba(0,245,212,0.5); }
        .pin-box { width: 45px; height: 55px; border: 2px solid #00F5D4; border-radius: 10px; background: rgba(10,4,26,0.8); font-size: 1.5rem; color: #FFD166; text-align: center; font-weight: 700; outline: none; margin: 0 4px; }
        .enter-btn { background: linear-gradient(135deg, #7B2CBF, #00F5D4); color: #0A041A; border: none; border-radius: 10px; padding: 0.7rem 2rem; font-weight: 700; cursor: pointer; margin-top: 1rem; box-shadow: 0 0 15px rgba(0,245,212,0.4); }
        </style>
        </head>
        <body>
            <div class="title">Paweetida & Dawis</div>
            <div style="font-size:0.8rem; color:#4CC9F0; margin-bottom:1rem; text-transform:uppercase; letter-spacing:2px;">Our Private Little World 💜</div>
            <div style="background: rgba(30,15,60,0.8); padding: 1.5rem; border-radius: 16px; border: 1px solid rgba(0,245,212,0.3);">
                <div style="margin-bottom:0.8rem; font-size:0.9rem; color:#FFD166;">Enter our special date (DDMMYY) 🔐</div>
                <div>
                    <input class="pin-box" maxlength="1" type="password" id="p0">
                    <input class="pin-box" maxlength="1" type="password" id="p1">
                    <input class="pin-box" maxlength="1" type="password" id="p2">
                    <input class="pin-box" maxlength="1" type="password" id="p3">
                    <input class="pin-box" maxlength="1" type="password" id="p4">
                    <input class="pin-box" maxlength="1" type="password" id="p5">
                </div>
                <button class="enter-btn" onclick="checkPin()">Enter World 🚀</button>
            </div>
            <script>
            const boxes = document.querySelectorAll('.pin-box');
            boxes[0].focus();
            boxes.forEach((box, i) => {
                box.addEventListener('input', () => { if(box.value && i<5) boxes[i+1].focus(); });
            });
            function checkPin() {
                let pin = Array.from(boxes).map(b => b.value).join('');
                if (pin === '220825') {
                    const parentDoc = window.parent.document;
                    const hiddenInput = parentDoc.querySelector('input[aria-label="hidden_pin"]');
                    let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                    nativeSetter.call(hiddenInput, pin);
                    hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
                }
            }
            </script>
        </body>
        </html>
        """, height=500, scrolling=False)

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
        .welcome-card {
            background: linear-gradient(135deg, rgba(123,44,191,0.85), rgba(0,245,212,0.6));
            border: 2px solid #FFD166;
            border-radius: 28px;
            padding: 2.8rem 2.2rem;
            text-align: center;
            max-width: 460px;
            width: 90%;
            box-shadow: 0 0 50px rgba(0,245,212,0.5);
            color: #FFFFFF;
        }
        .welcome-title { font-family: 'Pacifico', cursive; font-size: 2.6rem; color: #FFD166; margin-bottom: 0.4rem; }
        .welcome-sub { font-size: 0.95rem; font-weight: 700; margin-bottom: 1.2rem; color: #FF6B6B; }
        .welcome-desc { font-size: 0.92rem; line-height: 1.7; margin-bottom: 2rem; color: #F0E9FA; font-weight: 500; }
        .explore-btn {
            background: linear-gradient(135deg, #FFD166, #00F5D4);
            color: #0A041A;
            border: none;
            border-radius: 14px;
            padding: 0.85rem 2.2rem;
            font-size: 1.02rem;
            font-weight: 700;
            cursor: pointer;
            box-shadow: 0 0 20px rgba(0,245,212,0.6);
        }
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

stats = calculate_stats()

# ---- MAIN TABS (CLEAN 3 TABS) ----
tab_capsule, tab_stats, tab_battle = st.tabs(["💌 Love Capsule", "📊 Our Stats", "⚔️ Battle Phase"])

with tab_capsule:
    st.markdown('<div class="section-title">Love Capsule — Open a Secret Note 💌</div>', unsafe_allow_html=True)
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body { background: transparent; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: sans-serif; text-align: center; color: white; }
    .capsule-box { background: linear-gradient(135deg, rgba(123,44,191,0.6), rgba(0,245,212,0.2)); border: 1px solid rgba(0,245,212,0.4); border-radius: 20px; padding: 2rem; }
    </style>
    </head>
    <body>
        <div class="capsule-box">
            <div style="font-size:3rem;">💌</div>
            <h3>Love Capsule Ready</h3>
            <p style="color:#4CC9F0; font-size:0.9rem;">Tap below to unlock a secret note from your favorite rival!</p>
        </div>
    </body>
    </html>
    """, height=300, scrolling=False)

with tab_stats:
    st.markdown(f"""
    <div class="hero-section">
        <div style="font-size:2.2rem; margin-bottom:0.2rem">💜 🪖</div>
        <div class="hero-title">Paweetida & Dawis</div>
        <div class="hero-subtitle" style="color:#4CC9F0; font-size:0.8rem; letter-spacing:1.5px; text-transform:uppercase;">OUR STORY · SINCE 27 JULY 2025 (first liked my IG story ✨)</div>
        <div style="margin-top:0.5rem; color:#FFD166; font-size:0.9rem; font-style:italic;">
            "{stats['days_together']} days of loving you — and counting."
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="hero-section" style="text-align:center;">
            <div style="font-size:2.5rem; font-weight:700; color:#FFD166;">{stats['days_together']}</div>
            <div style="font-size:0.8rem; color:#4CC9F0; text-transform:uppercase; margin-top:0.3rem;">Days Together (Official)</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="hero-section" style="text-align:center;">
            <div style="font-size:2.5rem; font-weight:700; color:#FFD166;">{stats['days_since_first']}</div>
            <div style="font-size:0.8rem; color:#4CC9F0; text-transform:uppercase; margin-top:0.3rem;">Days Since We Met (27 Jul 2025)</div>
        </div>""", unsafe_allow_html=True)

with tab_battle:
    st.markdown('<div class="section-title">Battle Phase: 5 Cards Choice & Tap/Untap ⚔️🃏</div>', unsafe_allow_html=True)
    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <style>
    body { background: transparent; display: flex; justify-content: center; align-items: center; height: 100vh; margin: 0; font-family: sans-serif; color: white; text-align: center; }
    .duel-card { background: rgba(30,15,60,0.8); border: 2px solid #00F5D4; border-radius: 16px; padding: 2rem; }
    </style>
    </head>
    <body>
        <div class="duel-card">
            <h2>⚔️ Card Duel Arena ⚔️</h2>
            <p>Ready to battle with your favorite rival? Let's go!</p>
        </div>
    </body>
    </html>
    """, height=350, scrolling=False)
