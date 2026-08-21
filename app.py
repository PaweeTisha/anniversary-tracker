if not st.session_state.welcomed:
        components.html("""
        <!DOCTYPE html>
        <html>
        <head>
        <link href="https://fonts.googleapis.com/css2?family=Pacifico&family=Plus+Jakarta+Sans:wght@500;600;700&display=swap" rel="stylesheet">
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
            animation: popUp 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
            color: #FFFFFF;
        }
        @keyframes popUp { 0% { transform: scale(0.5); opacity: 0; } 100% { transform: scale(1); opacity: 1; } }
        .welcome-title { font-family: 'Pacifico', cursive; font-size: 2.6rem; color: #FFD166; margin-bottom: 0.4rem; text-shadow: 0 0 15px rgba(255,209,102,0.6); }
        .welcome-sub { font-size: 0.95rem; font-weight: 700; margin-bottom: 1.2rem; color: #FF6B6B; letter-spacing: 0.5px; }
        .welcome-desc { font-size: 0.92rem; line-height: 1.7; margin-bottom: 2rem; color: #F0E9FA; font-weight: 500; }
        .highlight-text { color: #FFD166; font-weight: 600; }
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
