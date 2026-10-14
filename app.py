"""
                sections = [
                    "## 1. The core question\nRestate the issue precisely and identify key unknowns.",
                    f"## 2. Philosophical analysis\nApply the selected lens ({lens}) accurately. Explain tensions and trade-offs.",
                ]
                if use_psychology:
                    sections.append("## 3. Psychology\nDiscuss relevant concepts and plausible explanations, distinguishing evidence from hypotheses.")
                if use_sociology:
                    sections.append("## 4. Sociology\nDiscuss relevant social context without stereotyping or assuming details.")
                sections.extend([
                    "## 5. Integrated understanding\nConnect perspectives, noting where they agree, differ, or cannot establish a conclusion.",
                    "## 6. Grounded way forward\nOffer two or three practical options or reflection prompts suited to the question.",
                    "## 7. One question worth sitting with\nEnd with one specific, open-ended question.",
                ])
                prompt = f"""
QUESTION:
<question>
{question}
</question>

STYLE: {tone}

Write in Markdown, following these sections:
{chr(10).join(sections)}

Be specific to the question. Do not invent facts about the people involved.
"""
                try:
                    with st.spinner("Thinking through the question..."):
                        client = genai.Client(api_key=api_key)
                        response = client.models.generate_content(
                            model="gemini-2.5-flash",
                            contents=prompt,
                            config={
                                "system_instruction": system_rules,
                                "temperature": 0.2,
                            },
                        )
                    answer = getattr(response, "text", None)
                    if answer and answer.strip():
                        st.markdown("---")
                        st.markdown("### 🧠 Analysis")
                        st.markdown(answer)
                        # Save the generated analysis so it remains in the database.
                        run(
                            "INSERT INTO chats(author, role, text, created_at) VALUES (?, ?, ?, ?)",
                            (st.session_state.who, "analysis", "Question: " + question.strip() + "\n\n" + answer.strip(), now_text()),
                        )
                    else:
                        st.error("The model returned an empty response. Please try again.")
                except Exception as exc:
                    st.error("Gemini could not generate the analysis. Check your key, internet connection, and model availability.")
                    with st.expander("Technical details for troubleshooting"):
                        st.code(str(exc))


# ------------------------------------------------------------
# TAB 4: SONGS + MEMORIES
# ------------------------------------------------------------
with tab_media:
    song_col, memory_col = st.columns(2)
    with song_col:
        st.subheader("🎧 Songs")
        with st.form("song_form", clear_on_submit=True):
            song_title = st.text_input("Song title")
            song_artist = st.text_input("Artist")
            song_note = st.text_area("Why does it matter to you?")
            song_submit = st.form_submit_button("Save song")
        if song_submit:
            if song_title.strip():
                run(
                    "INSERT INTO songs(title, artist, note, added_by, created_at) VALUES (?, ?, ?, ?, ?)",
                    (song_title.strip(), song_artist.strip(), song_note.strip(), st.session_state.who, now_text()),
                )
                st.success("Song saved.")
                st.rerun()
            else:
                st.warning("Add a song title first.")
        for song in rows("SELECT * FROM songs ORDER BY id DESC LIMIT 100"):
            body = (f"Artist: {song['artist']}\n" if song["artist"] else "") + song["note"]
            display_card(song["title"], body, f"Added by {song['added_by']} · {song['created_at']}")
        st.caption("This version saves song details, not uploaded audio files.")
    with memory_col:
        st.subheader("📜 Memory timeline")
        with st.form("memory_form", clear_on_submit=True):
            memory_title = st.text_input("Memory or milestone")
            memory_desc = st.text_area("What happened?")
            memory_date = st.text_input("Date or label", placeholder="e.g. Summer 2024")
            memory_submit = st.form_submit_button("Save memory")
        if memory_submit:
            if memory_title.strip():
                run(
                    "INSERT INTO memories(title, description, memory_date, added_by, created_at) VALUES (?, ?, ?, ?, ?)",
                    (memory_title.strip(), memory_desc.strip(), memory_date.strip() or "A moment to remember", st.session_state.who, now_text()),
                )
                st.success("Memory saved.")
                st.rerun()
            else:
                st.warning("Add a memory title first.")
        for memory in rows("SELECT * FROM memories ORDER BY id DESC LIMIT 100"):
            display_card(memory["title"], memory["description"], f"{memory['memory_date']} · Added by {memory['added_by']}")


# ------------------------------------------------------------
# TAB 5: PERSISTENT SHARED CHAT
# ------------------------------------------------------------
with tab_chat:
    st.markdown('<div class="lily-card"><h3>💬 Shared Chat</h3><p>Messages are saved in a local SQLite database, so they survive normal page refreshes and app reruns.</p></div>', unsafe_allow_html=True)
    chat_rows = rows("SELECT * FROM chats WHERE role = 'message' ORDER BY id DESC LIMIT 100")
    for item in reversed(chat_rows):
        st.chat_message("user" if item["author"] == st.session_state.who else "assistant").write(
            f"**{item['author']} · {item['created_at']}**\n\n{item['text']}"
        )
    with st.form("chat_form", clear_on_submit=True):
        message = st.text_area("Write a message for each other", height=90)
        send = st.form_submit_button("Send message 💌")
    if send:
        if message.strip():
            run(
                "INSERT INTO chats(author, role, text, created_at) VALUES (?, ?, ?, ?)",
                (st.session_state.who, "message", message.strip(), now_text()),
            )
            st.rerun()
        else:
            st.warning("Write a message first.")

st.divider()
st.caption("Our Shared Universe · Built with care. Back up the file our_shared_universe.db regularly; local storage is not a cloud sync service.")
