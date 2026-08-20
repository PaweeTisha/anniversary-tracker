import sqlite3
from datetime import date
from html import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# CONFIG
# =========================================================

st.set_page_config(
    page_title="Tisha & Dawis 💜",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="collapsed",
)

DB_FILE = "anniversary.db"
SECRET_PIN = "220825"


# =========================================================
# CSS
# =========================================================

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Pacifico&display=swap');

* {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #1A0A2E 0%, #2D1854 42%, #1E3A2A 100%);
    min-height: 100vh;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
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
}

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
}

.memory-card {
    background: rgba(61,26,110,0.5);
    border: 1px solid rgba(176,143,212,0.2);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
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

.army-badge {
    background: linear-gradient(135deg, rgba(74,92,58,0.8), rgba(122,140,106,0.4));
    border: 1px solid rgba(122,140,106,0.5);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    text-align: center;
    color: #E8EDE4;
}

.stTextInput input,
.stTextArea textarea {
    background: rgba(61,26,110,0.5) !important;
    border: 1px solid rgba(176,143,212,0.3) !important;
    color: #F0E9FA !important;
    border-radius: 8px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: rgba(240,233,250,0.55) !important;
}

.stButton button {
    background: linear-gradient(135deg, #6B3FA0, #4A5C3A) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}

.stButton button:hover {
    background: linear-gradient(135deg, #8B5CC0, #5A7048) !important;
    transform: translateY(-1px) !important;
}

.stTabs [data-baseweb="tab"] {
    color: #B08FD4 !important;
}

.stTabs [aria-selected="true"] {
    color: #F0E9FA !important;
    border-bottom: 2px solid #C9A84C !important;
}

.stProgress > div > div > div > div {
    background-color: #C9A84C !important;
}

.login-title {
    font-family: 'Pacifico', cursive;
    font-size: 3.2rem;
    text-align: center;
    line-height: 1.25;
    background: linear-gradient(135deg, #B08FD4, #C9A84C);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.login-card {
    background: rgba(61,26,110,0.7);
    border: 1px solid rgba(176,143,212,0.35);
    border-radius: 24px;
    padding: 2rem;
    text-align: center;
    margin: 2rem auto 1rem;
    max-width: 520px;
}

.login-pin input {
    height: 58px !important;
    text-align: center !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #C9A84C !important;
    padding: 0 !important;
}

.login-submit button {
    width: 100% !important;
    margin-top: 1rem !important;
}

@media screen and (max-width: 768px) {
    .hero-title {
        font-size: 2rem;
    }

    .login-title {
        font-size: 2.5rem;
    }
}
</style>
"""

st.markdown(CSS, unsafe_allow_html=True)


# =========================================================
# DATABASE
# =========================================================

def connection():
    return sqlite3.connect(DB_FILE)


def init_db():
    conn = connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            category TEXT DEFAULT 'memory',
            emoji TEXT DEFAULT '💜',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            type TEXT DEFAULT 'milestone'
        )
        """
    )

    cursor.execute("SELECT COUNT(*) FROM milestones")
    count = cursor.fetchone()[0]

    if count == 0:
        milestones = [
            (
                "First Like on Story 🚌",
                "2025-07-27",
                "กดไลค์สตอรี่ครั้งแรก — บนรถบัส",
                "start",
            ),
            (
                "Official Couple 💜",
                "2025-08-22",
                "วันที่เป็นแฟนกันอย่างเป็นทางการ",
                "anniversary",
            ),
            (
                "Dawis Enlists Army 🪖",
                "2026-04-20",
                "วันที่ Dawis เข้า Australian Army",
                "milestone",
            ),
        ]

        cursor.executemany(
            """
            INSERT INTO milestones
            (title, date, description, type)
            VALUES (?, ?, ?, ?)
            """,
            milestones,
        )

    conn.commit()
    conn.close()


def get_memories():
    conn = connection()

    data = pd.read_sql_query(
        """
        SELECT *
        FROM memories
        ORDER BY date DESC
        """,
        conn,
    )

    conn.close()
    return data


def add_memory(title, description, memory_date, category, emoji):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        INSERT INTO memories
        (title, description, date, category, emoji)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            title,
            description,
            str(memory_date),
            category,
            emoji,
        ),
    )

    conn.commit()
    conn.close()


def delete_memory(memory_id):
    conn = connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM memories WHERE id = ?",
        (memory_id,),
    )

    conn.commit()
    conn.close()


def get_milestones():
    conn = connection()

    data = pd.read_sql_query(
        """
        SELECT *
        FROM milestones
        ORDER BY date ASC
        """,
        conn,
    )

    conn.close()
    return data


# =========================================================
# CALCULATIONS
# =========================================================

def calculate_stats():
    today = date.today()

    first_date = date(2025, 7, 27)
    official_date = date(2025, 8, 22)
    army_date = date(2026, 4, 20)

    next_anniversary = date(today.year, 8, 22)

    if today > next_anniversary:
        next_anniversary = date(today.year + 1, 8, 22)

    days_since_first = (today - first_date).days
    days_together = (today - official_date).days
    days_to_anniversary = (next_anniversary - today).days

    if today >= army_date:
        days_since_army = (today - army_date).days
    else:
        days_since_army = 0

    return {
        "days_since_first": days_since_first,
        "days_together": days_together,
        "weeks_together": days_together // 7,
        "months_together": days_together // 30,
        "days_to_anniversary": days_to_anniversary,
        "days_since_army": days_since_army,
        "next_anniversary": next_anniversary,
    }


# =========================================================
# LOGIN
# =========================================================

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    left, center, right = st.columns([1, 2, 1])

    with center:
        st.markdown(
            """
            <div style="
                text-align:center;
                padding-top:3rem;
            ">
                <div style="
                    font-size:4rem;
                    margin-bottom:1rem;
                ">
                    💻 💜 🪖
                </div>

                <div style="
                    font-size:1.4rem;
                    color:#B08FD4;
                    margin-bottom:0.5rem;
                ">
                    🍀 💜 🍀 💚
