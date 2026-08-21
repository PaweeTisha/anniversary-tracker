import streamlit as st
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
.card { background: linear-gradient(135deg, rgba(123,44,191,0.6), rgba(0,245,212,0.25)); border-radius: 20px; padding: 2rem; text-align: center; border: 1px solid rgba(76,201,240,0.4); box-shadow: 0 0 35px rgba(0,245,212,0.25); margin-bottom: 1.5rem; }
.stButton button { background: linear-gradient(135deg, #7B2CBF, #00F5D4) !important; color: #0A041A !important; border-radius: 16px !important; font-weight: 800 !important; padding: 1rem !important; height: auto !important; width: 100% !important; border: none !important; }
.metric-box { background: rgba(10,4,26,0.6); border: 1px solid rgba(0,245,212,0.3); border-radius: 16px; padding: 1rem; text-align: center; }
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
if "view" not in st.session_state: st.session_state.view = "welcome"

# ---- AUTH ----
if not st.session_state.auth:
    st.markdown("<h1 style='text-align:center; margin-top:100px;'>Enter Secret Code</h1>", unsafe_allow_html=True)
    if st.text_input("code", type="password", label_visibility="collapsed") == "220825":
        st.session_state.auth = True; st.rerun()
    st.stop()

# ---- NAVIGATION ----
if st.session_state.view == "welcome":
    st.markdown("<h1 style='text-align:center; margin-top:100px;'>Welcome back, my favorite rival! 💜</h1>", unsafe_allow_html=True)
    if st.button("💐 Get Flowers & Enter"): st.session_state.view = "menu"; st.rerun()

elif st.session_state.view == "menu":
    st.markdown("<h1 style='text-align:center;'>Get Flowers! 🌷</h1>", unsafe_allow_html=True)
    st.markdown("""<div class='card'>🌷🌻💐<br><br><b>For My Favorite Rival 😈</b><br><br>Thanks for sticking around, even when I'm moody! 555. Let's keep supporting each other for a long time. 💜</div>""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🍒 Our Journey & Stats"): st.session_state.view = "stats"
    with col2:
        if st.button("💌 Love Capsule"): st.session_state.view = "capsule"
    with col3:
        if st.button("⚔️ Battle Arena"): st.session_state.view = "battle"

elif st.session_state.view == "stats":
    st.markdown("<h2 style='text-align:center;'>📊 Our Journey & Stats</h2>", unsafe_allow_html=True)
    today = date.today(); official_date = date(2025, 8, 22); diff = (today - official_date).days
    st.markdown(f"<div class='card'><h1>{diff} Days Together</h1></div>", unsafe_allow_html=True)
    
    df = pd.read_sql_query("SELECT * FROM milestones", sqlite3.connect('anniversary.db'))
    fig = go.Figure(go.Scatter(x=pd.to_datetime(df['date']), y=[1]*len(df), mode='markers+text', text=df['title'], textposition="top center"))
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', font_color="white")
    st.plotly_chart(fig, use_container_width=True)
    if st.button("← Back to Menu"): st.session_state.view = "menu"; st.rerun()

elif st.session_state.view == "capsule":
    st.markdown("<h2 style='text-align:center;'>💌 Love Capsule</h2>", unsafe_allow_html=True)
    if st.button("Open Note"): st.success("The moon is beautiful, isn't it? 💜")
    if st.button("← Back to Menu"): st.session_state.view = "menu"; st.rerun()

elif st.session_state.view == "battle":
    st.markdown("<h2 style='text-align:center;'>⚔️ Battle Arena</h2>", unsafe_allow_html=True)
    st.write("Ready for a card duel? (Battle logic here)")
    if st.button("← Back to Menu"): st.session_state.view = "menu"; st.rerun()
