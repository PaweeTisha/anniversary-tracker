import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import datetime, date
import plotly.graph_objects as go
import base64

# ---- PAGE CONFIG ----
st.set_page_config(page_title="Paweetida & Dawis 💜", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

# ---- CUSTOM CSS ----
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&family=DM+Sans:ital,wght@0,300;0,400;0,500;0,600;0,700;1,300;1,400&display=swap');

.stApp { background: linear-gradient(135deg, #050210 0%, #10072B 30%, #031B26 70%, #020C1B 100%); min-height: 100vh; }
div[data-testid="stTextInput"]:has(input[aria-label="hidden_welcome"]),
div[data-testid="stTextInput"]:has(input[aria-label="hidden_pin"]) { display: none !important; }

.section-title { font-family: 'Plus Jakarta Sans', sans-serif; font-size: 1.3rem; font-weight: 700; color: #FFD166; margin-bottom: 1rem; border-left: 4px solid #00F5D4; padding-left: 10px; }
.memory-card { background: rgba(30, 15, 60, 0.6); border: 1px solid rgba(76,201,240,0.3); border-radius: 12px; padding: 1rem; margin-bottom: 0.8rem; color: #F0E9FA; }
</style>
""", unsafe_allow_html=True)

# ---- DATABASE FUNCTIONS ----
def init_db():
    conn = sqlite3.connect('anniversary.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS memories (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, description TEXT, date TEXT, category TEXT, emoji TEXT, image_data TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS milestones (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, date TEXT, description TEXT, type TEXT, image_data TEXT)''')
    
    # Add sample data if empty
    c.execute("SELECT COUNT(*) FROM milestones")
    if c.fetchone()[0] == 0:
        c.executemany("INSERT INTO milestones (title, date, description, type) VALUES (?,?,?,?)", [
            ("First Like 🚌", "2025-07-27", "The start", "start"),
            ("Official 💜", "2025-08-22", "Official", "anniversary"),
            ("Army 🪖", "2026-04-20", "Army", "milestone")
        ])
    conn.commit()
    conn.close()

def get_memories():
    conn = sqlite3.connect('anniversary.db')
    df = pd.read_sql_query("SELECT * FROM memories ORDER BY date DESC", conn)
    conn.close()
    return df

def get_milestones():
    conn = sqlite3.connect('anniversary.db')
    df = pd.read_sql_query("SELECT * FROM milestones ORDER BY date ASC", conn)
    conn.close()
    return df

# ---- APP LOGIC ----
init_db()
tab1, tab2, tab3, tab4 = st.tabs(["💜 Memories", "📸 Timeline", "➕ Add Memory", "📊 Stats"])

with tab1:
    st.markdown('<div class="section-title">Our Memories</div>', unsafe_allow_html=True)
    df = get_memories()
    for _, row in df.iterrows():
        st.markdown(f'<div class="memory-card"><b>{row["emoji"]} {row["title"]}</b> ({row["date"]})<br>{row["description"]}</div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-title">Timeline Scrapbook</div>', unsafe_allow_html=True)
    milestones = get_milestones()
    memories = get_memories()
    
    # รวม event ทั้งหมด
    events = []
    for _, row in milestones.iterrows():
        events.append({'date': row['date'], 'title': row['title'], 'img': row['image_data']})
    for _, row in memories.iterrows():
        events.append({'date': row['date'], 'title': row['title'], 'img': row['image_data']})
    events = sorted(events, key=lambda x: x['date'])

    for e in events:
        col1, col2 = st.columns([1, 4])
        with col1:
            st.markdown(f"**{e['date']}**")
        with col2:
            if e['img']:
                try:
                    st.image(base64.b64decode(e['img']), width=150, caption=e['title'])
                except:
                    st.write(e['title'])
            else:
                st.write(f"✨ {e['title']}")

with tab3:
    st.markdown('<div class="section-title">Add Memory</div>', unsafe_allow_html=True)
    title = st.text_input("Title")
    desc = st.text_area("Description")
    date_val = st.date_input("Date")
    img = st.file_uploader("Photo")
    if st.button("Save"):
        img_b64 = base64.b64encode(img.getvalue()).decode() if img else None
        add_memory(title, desc, date_val, "memory", "💜", img_b64)
        st.rerun()

with tab4:
    st.write("Stats dashboard here...")
