import streamlit as st
import streamlit.components.v1 as components
import sqlite3
import pandas as pd
from datetime import date
import plotly.graph_objects as go

st.set_page_config(page_title="Paweetida & Dawis 💜", page_icon="💜", layout="wide", initial_sidebar_state="collapsed")

# CSS สวยๆ ที่เคยทำไว้
st.markdown("""
<style>
.stApp { background: linear-gradient(135deg, #050210 0%, #10072B 30%, #031B26 70%, #020C1B 100%); color: #F0E9FA; }
.hero-card { background: linear-gradient(135deg, rgba(123,44,191,0.6), rgba(0,245,212,0.25)); border-radius: 20px; padding: 2rem; text-align: center; border: 1px solid rgba(76,201,240,0.4); box-shadow: 0 0 35px rgba(0,245,212,0.25); margin-bottom: 1.5rem; }
.stButton button { background: linear-gradient(135deg, #7B2CBF, #00F5D4) !important; color: #0A041A !important; border-radius: 12px !important; font-weight: 800 !important; padding: 1rem !important; width: 100% !important; border: none !important; }
</style>
""", unsafe_allow_html=True)

# สถานะหน้าจอ
if "auth" not in st.session_state: st.session_state.auth = False
if "view" not in st.session_state: st.session_state.view = "login"

# ---- หน้า LOGIN (หน้าสวยๆ เดิม) ----
if st.session_state.view == "login":
    components.html("""
    <div style="text-align:center; padding:100px; color:white; font-family:sans-serif;">
        <h1>Enter Secret Code</h1>
        <input type="password" id="p" style="padding:10px; border-radius:10px; border:none; width:300px;"><br><br>
        <button onclick="
            if(document.getElementById('p').value=='220825') { 
                const p=window.parent.document; 
                const btn=p.querySelector('button[kind=primary]'); 
                const i=p.querySelector('input[type=password]'); 
                i.value='220825'; i.dispatchEvent(new Event('input', {bubbles:true})); 
            }" style="padding:10px 30px; border-radius:10px; cursor:pointer;">Enter</button>
    </div>
    """, height=400)
    if st.text_input("code", type="password", label_visibility="collapsed") == "220825":
        st.session_state.auth = True; st.session_state.view = "welcome"; st.rerun()

# ---- หน้า WELCOME ----
elif st.session_state.view == "welcome":
    st.markdown("<h1 style='text-align:center;'>Welcome back, my favorite rival! 💜</h1>", unsafe_allow_html=True)
    if st.button("💐 Get Flowers & Enter"): st.session_state.view = "menu"; st.rerun()

# ---- หน้าเมนู (รวมทุกอย่างไว้ที่นี่) ----
elif st.session_state.view == "menu":
    st.markdown("<h1 style='text-align:center;'>Get Flowers! 🌷</h1>", unsafe_allow_html=True)
    st.markdown("""<div class='hero-card'>🌷🌻💐<br><br><b>For My Favorite Rival 😈</b><br><br>Thanks for sticking around, even when I'm moody! Let's keep supporting each other. 💜</div>""", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🍒 Journey & Stats"): st.session_state.view = "stats"; st.rerun()
    with col2:
        if st.button("💌 Love Capsule"): st.session_state.view = "capsule"; st.rerun()
    with col3:
        if st.button("⚔️ Battle Arena"): st.session_state.view = "battle"; st.rerun()

# ---- หน้าฟีเจอร์ต่างๆ (ก๊อปปี้โค้ดเดิมของคุณมาใส่ที่นี่ได้เลยครับ) ----
elif st.session_state.view == "stats":
    st.write("## 📊 Our Journey & Stats")
    if st.button("← Back to Menu"): st.session_state.view = "menu"; st.rerun()

elif st.session_state.view == "capsule":
    st.write("## 💌 Love Capsule")
    if st.button("← Back to Menu"): st.session_state.view = "menu"; st.rerun()

elif st.session_state.view == "battle":
    st.write("## ⚔️ Battle Arena")
    if st.button("← Back to Menu"): st.session_state.view = "menu"; st.rerun()
