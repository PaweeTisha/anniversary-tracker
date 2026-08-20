# ... (ส่วนบนสุดเหมือนเดิม จนถึงช่วง Tab 3)

# ======== TAB 3: TIMELINE (Polaroid Clickable Style) ========
with tab3:
    st.markdown('<div class="section-title">Our Timeline Scrapbook 📸</div>', unsafe_allow_html=True)
    milestones_df = get_milestones()
    memories_df = get_memories()
    
    all_events = []
    for _, row in milestones_df.iterrows():
        all_events.append({'date': row['date'], 'title': row['title'], 'desc': row['description'], 'emoji': '⭐', 'cat': 'Milestone'})
    for _, row in memories_df.iterrows():
        all_events.append({'date': row['date'], 'title': row['title'], 'desc': row['description'], 'emoji': row['emoji'], 'cat': row['category']})
    
    all_events = sorted(all_events, key=lambda x: x['date'])

    st.markdown('<div class="scrapbook-container">', unsafe_allow_html=True)
    for idx, event in enumerate(all_events):
        # ใช้ expander แทนการคลิกที่รูป เพื่อความเสถียรครับ
        with st.expander(f"{event['date']} — {event['title']} {event['emoji']}"):
            st.markdown(f"""
            <div style="background: rgba(255,255,255,0.05); padding: 10px; border-radius: 8px;">
                <p style="color:#B08FD4; font-size: 0.9rem;"><strong>Category:</strong> {event['cat']}</p>
                <p style="color:#FAFAFA;">{event['desc'] or 'Just a lovely moment together 💜'}</p>
            </div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ======== TAB 4: ADD MEMORY (English Version) ========
with tab4:
    st.markdown('<div class="section-title">Add a New Memory ➕</div>', unsafe_allow_html=True)
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        mem_title = st.text_input("Title *", placeholder="e.g. Our first date")
        mem_date = st.date_input("Date", value=date.today())
    with col_f2:
        mem_category = st.selectbox("Category", ["Date Night", "Travel", "Milestone", "Everyday", "Food", "Army Life"])
        mem_emoji = st.selectbox("Emoji", ["💜", "🥰", "✈️", "🍜", "🎉", "🪖", "🏔️"])
    mem_desc = st.text_area("Description (Eng)", placeholder="Write something sweet in English...", height=60)
    if st.button("Save Memory 💜", use_container_width=True):
        if mem_title:
            add_memory(mem_title, mem_desc, mem_date, mem_category, mem_emoji)
            st.success("Memory added successfully!")
            st.rerun()
