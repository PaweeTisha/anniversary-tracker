# [โค้ดเดิมด้านบน...]

if not check_password():
    st.stop()

# ==========================================
# ---- JIGSAW PUZZLE MINI-GAME ----
# ==========================================
if "puzzle_solved" not in st.session_state:
    st.session_state.puzzle_solved = False

if not st.session_state.puzzle_solved:
    # ซ่อนช่อง input สำหรับรับค่าจากจิ๊กซอว์
    st.markdown("""
    <style>
    div[data-testid="stTextInput"] {
        position: absolute !important;
        width: 0px !important;
        height: 0px !important;
        overflow: hidden !important;
        opacity: 0 !important;
        z-index: -9999 !important;
        pointer-events: none !important;
    }
    /* ปรับแต่งปุ่มข้าม */
    .stButton button {
        background: transparent !important;
        color: #B08FD4 !important;
        border: 1px solid #B08FD4 !important;
        margin-top: 1rem;
    }
    .stButton button:hover {
        background: rgba(176,143,212,0.2) !important;
    }
    </style>
    """, unsafe_allow_html=True)

    components.html("""
    <!DOCTYPE html>
    <html>
    <head>
    <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            background: transparent;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            font-family: 'Plus Jakarta Sans', sans-serif;
            color: #F0E9FA;
            margin: 0;
            padding-top: 2rem;
        }
        h3 { color: #C9A84C; margin-bottom: 0.5rem; font-size: 1.5rem; }
        p { color: #B08FD4; font-size: 0.9rem; margin-bottom: 1.5rem; text-align: center; }
        
        #puzzle-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 2px;
            width: 300px;
            height: 300px;
            background: rgba(176,143,212,0.2);
            padding: 4px;
            border-radius: 12px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        .piece {
            width: 100%;
            height: 100%;
            background-size: 300px 300px;
            cursor: pointer;
            border-radius: 4px;
            transition: transform 0.1s, border 0.1s;
        }
        .piece:hover { opacity: 0.9; }
        .piece.selected {
            border: 3px solid #C9A84C;
            transform: scale(0.95);
        }
    </style>
    </head>
    <body>
        <h3>Just one more step! 🧩</h3>
        <p>แตะสลับชิ้นส่วนจิ๊กซอว์ให้ภาพสมบูรณ์<br>เพื่อปลดล็อกความทรงจำของเรา 💜</p>
        
        <div id="puzzle-container"></div>

        <script>
        // 🌟 เปลี่ยน URL รูปภาพตรงนี้เป็นรูปรวมของคุณสองคนได้เลยค่ะ แนะนำเป็นรูปสี่เหลี่ยมจัตุรัสนะคะ
        const imageUrl = "https://images.unsplash.com/photo-1518199268839-49f242d559bc?q=80&w=300&h=300&fit=crop"; 
        
        const container = document.getElementById('puzzle-container');
        let order = [0, 1, 2, 3, 4, 5, 6, 7, 8];
        
        // สุ่มตำแหน่งชิ้นส่วน
        order.sort(() => Math.random() - 0.5);
        let selected = null;

        function render() {
            container.innerHTML = '';
            order.forEach((pieceIdx, domIdx) => {
                const div = document.createElement('div');
                div.className = 'piece';
                if(selected === domIdx) div.classList.add('selected');
                
                const row = Math.floor(pieceIdx / 3);
                const col = pieceIdx % 3;
                
                div.style.backgroundImage = `url(${imageUrl})`;
                div.style.backgroundPosition = `-${col * 97}px -${row * 97}px`;
                
                div.onclick = () => handlePieceClick(domIdx);
                container.appendChild(div);
            });
            checkWin();
        }

        function handlePieceClick(idx) {
            if (selected === null) {
                selected = idx;
            } else {
                // สลับตำแหน่ง
                let temp = order[selected];
                order[selected] = order[idx];
                order[idx] = temp;
                selected = null;
            }
            render();
        }

        function checkWin() {
            if (order.every((val, index) => val === index)) {
                // ทายถูกแล้ว! ส่งสัญญาณกลับไปที่ Python
                setTimeout(() => {
                    const parentDoc = window.parent.document;
                    const hiddenInput = parentDoc.querySelector('input[aria-label="puzzle_signal"]');
                    if (hiddenInput) {
                        let nativeSetter = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype, 'value').set;
                        nativeSetter.call(hiddenInput, 'solved');
                        hiddenInput.dispatchEvent(new Event('input', { bubbles: true }));
                        hiddenInput.dispatchEvent(new KeyboardEvent('keydown', { key: 'Enter', code: 'Enter', bubbles: true }));
                    }
                }, 500); // รอครึ่งวิให้เห็นภาพเต็มก่อนค่อยเด้งเข้าแอป
            }
        }
        
        render();
        </script>
    </body>
    </html>
    """, height=500, scrolling=False)

    # รับสัญญาณจาก JavaScript
    puzzle_signal = st.text_input("puzzle_signal", label_visibility="collapsed")
    
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        # มีปุ่มข้ามให้เผื่อว่าต่อไม่ผ่านจริงๆ หรือขี้เกียจเล่นค่ะ
        if puzzle_signal == "solved" or st.button("ข้ามไปดูความทรงจำเลย ⏩", use_container_width=True):
            st.session_state.puzzle_solved = True
            st.rerun()

    st.stop() # หยุดการทำงานตรงนี้จนกว่าจะต่อจิ๊กซอว์เสร็จ

# ==========================================
# ---- INIT (เริ่มแสดงเว็บหลัก) ----
# ==========================================
init_db()
stats = calculate_stats()

# [โค้ดเดิมด้านล่าง...]
