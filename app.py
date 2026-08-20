import sqlite3
from datetime import date
from html import escape

import pandas as pd
import plotly.graph_objects as go
import streamlit as st


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Tisha & Dawis 💜",
    page_icon="💜",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# =========================================================
# CONSTANTS
# =========================================================

DB_FILE = "anniversary.db"
SECRET_PIN = "220825"


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Pacifico&display=swap');

:root {
    --purple-deep: #3D1A6E;
    --purple-mid: #6B3FA0;
    --purple-light: #B08FD4;
    --purple-pale: #F0E9FA;
    --army-green: #4A5C3A;
    --army-light: #7A8C6A;
    --gold: #C9A84C;
}

* {
    font-family: 'DM Sans', sans-serif;
}

.stApp {
    background: linear-gradient(
        135deg,
        #1A0A2E 0%,
        #2D1854 42%,
        #1E3A2A 100%
    );
    min-height: 100vh;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* ================= LOGIN ================= */

.login-page {
    min-height: 620px;
    display: flex;
    justify-content: center;
    align-items: center;
    text-align: center;
    padding: 2rem 1rem;
}

.login-content {
    width: 100%;
    max-width: 520px;
    margin: auto;
}

.login-chars {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 2rem;
    margin-bottom: 1rem;
}

.login-char {
    font-size: 4.5rem;
    display: inline-block;
    animation: float 2.5s ease-in-out infinite;
}

.login-heart {
    font-size: 3.2rem;
    display: inline-block;
    animation: heartbeat 1.2s ease-in-out infinite;
}

.login-title {
    font-family: 'Pacifico', cursive;
    font-size: 3.4rem;
    line-height: 1.3;
    background: linear-gradient(135deg, #B08FD4, #C9A84C);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.login-and {
    color: #C9A84C;
    font-family: 'Pacifico', cursive;
    font-size: 1.8rem;
    margin: 0.2rem 0;
}

.login-subtitle {
    color: #B08FD4;
    font-size: 0.75rem;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 0.8rem;
}

.login-stars {
    font-size: 1.3rem;
    letter-spacing: 0.4rem;
    margin: 1rem 0;
}

.login-card {
    background: rgba(61, 26, 110, 0.65);
    border: 1px solid rgba(176, 143, 212, 0.35);
    border-radius: 24px;
    padding: 1.8rem 2rem 2rem;
    margin: 2rem auto 0;
    backdrop-filter: blur(12px);
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.login-lock {
    font-size:
