import streamlit as st
import sqlite3
import pandas as pd
from datetime import date
import plotly.graph_objects as go
from html import escape


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
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=DM+Sans:wght@300;400;500;600;700&family=Pacifico&display=swap');

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
    --red: #E24B4A;
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


/* ---------------- LOGIN PAGE ---------------- */

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
}

.login-heart {
    font-size: 3.2rem;
    display: inline-block;
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
    font-size: 2rem;
    margin-bottom: 0.5rem;
}

.login-card-title {
    color: #C9A84C;
    font-family: 'Pacifico', cursive;
    font-size: 1.25rem;
}

.login-hint {
    color: rgba(176, 143, 212, 0.75);
    font-size: 0.78rem;
    font-style: italic;
    margin: 0.4rem 0 1.2rem;
}

/* PIN boxes */
div[data-testid="stTextInput"] input {
    background: rgba(61, 26, 110, 0.55) !important;
    border: 1px solid rgba(176, 143, 212, 0.35) !important;
    color: #F0E9FA !important;
    border-radius: 10px !important;
}

.login-pin-area div[data-testid="stTextInput"] input {
    height: 58px !important;
    text-align: center !important;
    font-size: 1.8rem !important;
    font-weight: 700 !important;
    color: #C9A84C !important;
    padding: 0 !important;
}

.login-pin-area div[data-testid="stTextInput"] input:focus {
    border-color: #C9A84C !important;
    box-shadow: 0 0 14px rgba(201, 168, 76, 0.35) !important;
}

.login-submit button {
    width: 100% !important;
    margin-top: 0.8rem !important;
    background: linear-gradient(135deg, #6B3FA0, #4A5C3A) !important;
    color: white !important;
    border: none !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    padding: 0.75rem 1rem !important;
}

.login-submit button:hover {
    background: linear-gradient(135deg, #8B5CC0, #5A7048) !important;
    transform: translateY(-2px) !important;
}


/* ---------------- MAIN APP ---------------- */

.hero-section {
    background: linear-gradient(
        135deg,
        rgba(61, 26, 110, 0.9),
        rgba(74, 92, 58, 0.8)
    );
    border-radius: 20px;
    padding: 3rem 2rem;
    text-align: center;
    border: 1px solid rgba(176, 143, 212, 0.3);
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
    background: linear-gradient(
        135deg,
        rgba(61, 26, 110, 0.7),
        rgba(74, 92, 58, 0.5)
    );
    border: 1px solid rgba(176, 143, 212, 0.25);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    backdrop-filter: blur(8px);
    transition: transform 0.2s;
}

.metric-card:hover {
    transform: translateY(-4px);
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
    border-bottom: 1px solid rgba(176, 143, 212, 0.3);
    padding-bottom: 0.5rem;
    letter-spacing: -0.3px;
}

.memory-card {
    background: rgba(61, 26, 110, 0.5);
    border: 1px solid rgba(176, 143, 212, 0.2);
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

.army-badge {
    background: linear-gradient(
        135deg,
        rgba(74, 92, 58, 0.8),
        rgba(122, 140, 106, 0.4)
    );
    border: 1px solid rgba(122, 140, 106, 0.5);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    text-align: center;
    color: #E8EDE4;
}

.stTextInput input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] {
    background: rgba(61, 26, 110, 0.5) !important;
    border: 1px solid rgba(176, 143, 212, 0.3) !important;
    color: #F0E9FA !important;
    border-radius: 8px !important;
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder {
    color: rgba(240, 233, 250, 0.55) !important;
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

div[data-testid="stMetricValue"] {
    color: #C9A84C !important;
}

@media screen and (max-width: 768px) {
    .hero-title {
        font-size: 2rem;
    }

    .hero-subtitle {
        font-size: 0.7rem;
        letter-spacing: 1px;
    }

    .login-title {
        font-size: 2.6rem;
    }

    .login-chars {
        gap: 1rem;
    }

    .login-char {
        font-size: 3.5rem;
    }

    .login-heart {
        font-size: 2.5rem;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# DATABASE
# =========================================================

DB_FILE = "anniversary.db"
SECRET_PIN = "220825"


def get_connection():
    return sqlite3.connect(DB_FILE)


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            date TEXT NOT NULL,
            category TEXT DEFAULT 'memory',
            emoji TEXT DEFAULT '💜',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS milestones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            type TEXT DEFAULT 'milestone'
        )
    """)

    cursor.execute("SELECT COUNT(*) FROM milestones")

    if cursor.fetchone()[0] == 0:
        default_milestones = [
            (
                "First Like on Story 🚌",
                "2025-07-27",
                "กดไลค์สตอรี่ครั้งแรก — บนรถบัส",
                "start"
            ),
            (
                "Official Couple 💜",
                "2025-08-22",
                "วันที่เป็นแฟนกันอย่างเป็นทางการ",
                "anniversary"
            ),
            (
                "Dawis Enlists Army 🪖",
                "2026-04-20",
                "วันที่ Dawis เข้า Australian Army",
                "milestone"
            )
        ]

        cursor.executemany(
            """
            INSERT INTO milestones
            (title, date, description, type)
            VALUES (?, ?, ?, ?)
            """,
            default_milestones
        )

    conn.commit()
    conn.close()


def get_memories():
    conn = get_connection()

    dataframe = pd.read_sql_query(
        """
        SELECT *
        FROM memories
        ORDER BY date DESC
        """,
        conn
    )

    conn.close()
    return dataframe


def add_memory(title, description, date_value, category, emoji):
    conn = get_connection()
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
            str(date_value),
            category,
            emoji
        )
    )

    conn.commit()
    conn.close()


def delete_memory(memory_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM memories WHERE id = ?",
        (memory_id,)
    )

    conn.commit()
    conn.close()


def get_milestones():
    conn = get_connection()

    dataframe = pd.read_sql_query(
        """
        SELECT *
        FROM milestones
        ORDER BY date ASC
        """,
        conn
    )

    conn.close()
    return dataframe


# =========================================================
# CALCULATIONS
# =========================================================

def calculate_stats():
    today = date.today()

    start_date = date(2025, 7, 27)
    official_date = date(2025, 8, 22)
    army_date = date(2026, 4, 20)

    next_anniversary = date(today.year, 8, 22)

    if today > next_anniversary:
        next_anniversary = date(today.year + 1, 8, 22)

    days_since_first = (today - start_date).days
    days_together = (today - official_date).days
    days_to_anniversary = (next_anniversary - today).days

    if today >= army_date:
        days_since_army = (today - army_date).days
    else:
        days_since_army = 0

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
        "official_date": official_date
    }


# =========================================================
# LOGIN
# =========================================================

def check_password():
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if st.session_state.authenticated:
        return True

    st.markdown("""
    <div class="login-page">
        <div class="login-content">
            <div class="login-chars">
                <span class="login-char">💻</span>
                <span class="login-heart">💜</span>
                <span class="login-char">🪖</span>
            </div>

            <div class="login-stars">🍀 💜 🍀 💚 🍀</div>

            <div class="login-title">Paweetida</div>
            <div class="login-and">&amp;</div>
            <div class="login-title">Mr. Dawis</div>

            <div class="login-subtitle">
                Our Private Little World 💜
            </div>

            <div class="login-card">
                <div class="login-lock">🔐</div>

                <div class="login-card-title">
                    Enter our secret code
                </div>

                <div class="login-hint">
                    hint: our special date 💜
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    center_left, center, center_right = st.columns([1, 2, 1])

    with center:
        with st.form("login_form", clear_on_submit=False):
            st.markdown(
                '<div class="login-pin-area">',
                unsafe_allow_html=True
            )

            pin_columns = st.columns(6)
            pin_values = []

            for index, pin_column in enumerate(pin_columns):
                with pin_column:
                    value = st.text_input(
                        f"PIN digit {index + 1}",
                        max_chars=1,
                        type="password",
                        key=f"pin_digit_{index}",
                        label_visibility="collapsed"
                    )
                    pin_values.append(value)

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

            st.markdown(
                '<div class="login-submit">',
                unsafe_allow_html=True
            )

            submitted = st.form_submit_button(
                "Enter Our World 💜",
                use_container_width=True
            )

            st.markdown(
                '</div>',
                unsafe_allow_html=True
            )

        if submitted:
            entered_pin = "".join(pin_values)

            if entered_pin == SECRET_PIN:
                st.session_state.authenticated = True
                st.rerun()
            else:
                st.error("Hmm, that's not right... 💔 Try again!")

    return False


# =========================================================
# START APPLICATION
# =========================================================

if not check_password():
    st.stop()

init_db()
stats = calculate_stats()


# =========================================================
# HERO
# =========================================================

st.markdown(f"""
<div class="hero-section">
    <div style="font-size:3rem; margin-bottom:0.5rem;">
        💜 🪖
    </div>

    <div class="hero-title">
        Paweetida &amp; Mr. Dawis
    </div>

    <div class="hero-subtitle">
        Our Story · Since 27 July 2025
        <br>
        <span style="font-size:0.75rem;">
            the day you liked my story 🚌
        </span>
    </div>

    <div style="
        margin-top:1.5rem;
        color:#C9A84C;
        font-size:1.1rem;
        font-style:italic;
        font-weight:300;
        letter-spacing:0.3px;
    ">
        "{stats['days_together']} days of loving you — and counting."
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# TABS
# =========================================================

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Our Stats",
    "💜 Memories",
    "🗓️ Timeline",
    "➕ Add Memory"
])


# =========================================================
# TAB 1: STATS
# =========================================================

with tab1:
    st.markdown(
        '<div class="section-title">Our Story in Numbers</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">
                {stats['days_together']}
            </div>
            <div class="metric-label">
                Days Together
            </div>
            <div class="metric-desc">
                Since 22 Aug 2025 💜
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">
                {stats['weeks_together']}
            </div>
            <div class="metric-label">
                Weeks Together
            </div>
            <div class="metric-desc">
                {stats['months_together']} months of us 🌙
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">
                {stats['days_to_anniversary']}
            </div>
            <div class="metric-label">
                Days to Anniversary
            </div>
            <div class="metric-desc">
                22 Aug {stats['next_anniversary'].year} 🎉
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-number">
                {stats['days_since_first']}
            </div>
            <div class="metric-label">
                Days Since We Met
            </div>
            <div class="metric-desc">
                27 Jul 2025 on the bus 🚌
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    col_army, col_chart = st.columns([1, 2])

    with col_army:
        st.markdown(f"""
        <div class="army-badge">
            <div style="font-size:2.5rem;">
                🪖
            </div>

            <div style="
                font-size:1.8rem;
                color:#C9A84C;
                font-weight:700;
            ">
                {stats['days_since_army']}
            </div>

            <div style="
                font-size:0.8rem;
                letter-spacing:1.5px;
                text-transform:uppercase;
                color:#B4C2A6;
                margin-top:0.3rem;
            ">
                Days in Service
            </div>

            <div style="
                font-size:0.85rem;
                margin-top:0.5rem;
                color:#E8EDE4;
            ">
                Dawis joined Australian Army
                <br>
                20 April 2026
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col_chart:
        milestones_df = get_milestones()

        if not milestones_df.empty:
            milestones_df["date"] = pd.to_datetime(
                milestones_df["date"]
            )

            y_positions = [
                1.0,
                1.15,
                0.85,
                1.2,
                0.8
            ]

            text_positions = [
                "top center",
                "top center",
                "bottom center",
                "top center",
                "bottom center"
            ]

            colors = [
                "#C9A84C",
                "#B08FD4",
                "#7A8C6A"
            ]

            figure = go.Figure()

            for index, row in milestones_df.iterrows():
                color = colors[index % len(colors)]
                y_position = y_positions[index % len(y_positions)]
                text_position = text_positions[
                    index % len(text_positions)
                ]

                figure.add_trace(
                    go.Scatter(
                        x=[row["date"]],
                        y=[y_position],
                        mode="markers+text",
                        marker={
                            "size": 16,
                            "color": color,
                            "symbol": "diamond"
                        },
                        text=[row["title"]],
                        textposition=text_position,
                        textfont={
                            "color": "#F0E9FA",
                            "size": 10
                        },
                        hovertemplate=(
                            f"<b>{escape(str(row['title']))}</b>"
                            f"<br>{escape(str(row['description']))}"
                            "<extra></extra>"
                        ),
                        showlegend=False
                    )
                )

                figure.add_shape(
                    type="line",
                    x0=row["date"],
                    x1=row["date"],
                    y0=1.0,
                    y1=y_position,
                    line={
                        "color": color,
