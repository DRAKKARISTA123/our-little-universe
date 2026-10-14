from datetime import datetime
import html
import sqlite3
from pathlib import Path

import streamlit as st

try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False


# ------------------------------------------------------------
# CONFIGURATION + PERSISTENT STORAGE
# ------------------------------------------------------------
st.set_page_config(
    page_title="Our Shared Universe",
    page_icon="🌸",
    layout="centered",
)

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "our_shared_universe.db"


def db_connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with db_connect() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS recipes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                added_by TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS songs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                artist TEXT NOT NULL DEFAULT '',
                note TEXT NOT NULL DEFAULT '',
                added_by TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                memory_date TEXT NOT NULL,
                added_by TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS chats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                author TEXT NOT NULL,
                role TEXT NOT NULL,
                text TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)
        # Add a few gentle starter items only once.
        count = conn.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        if count == 0:
            conn.execute(
                "INSERT INTO notes(author, text, created_at) VALUES (?, ?, ?)",
                ("Youssef", "High school crush turned into my favorite reality. Respect and empathy, always.", "Foundation"),
            )
        count = conn.execute("SELECT COUNT(*) FROM recipes").fetchone()[0]
        if count == 0:
            conn.execute(
                "INSERT INTO recipes(title, description, added_by, created_at) VALUES (?, ?, ?, ?)",
                ("A little recovery smoothie", "Banana, yogurt or a milk alternative, oats, and berries. Adjust ingredients to your preferences.", "Lina", "Foundation"),
            )
        count = conn.execute("SELECT COUNT(*) FROM songs").fetchone()[0]
        if count == 0:
            conn.execute(
                "INSERT INTO songs(title, artist, note, added_by, created_at) VALUES (?, ?, ?, ?, ?)",
                ("Our Song of the Universe", "Timeless", "A placeholder for a song that means something to us.", "Youssef", "Foundation"),
            )
        count = conn.execute("SELECT COUNT(*) FROM memories").fetchone()[0]
        if count == 0:
            conn.execute(
                "INSERT INTO memories(title, description, memory_date, added_by, created_at) VALUES (?, ?, ?, ?, ?)",
                ("The Beginning", "Back in high school when I first noticed you.", "The Origin", "Youssef", "Foundation"),
            )


def now_text():
    return datetime.now().strftime("%Y-%m-%d %H:%M")


def rows(query, params=()):
    with db_connect() as conn:
        return conn.execute(query, params).fetchall()


def run(query, params=()):
    with db_connect() as conn:
        conn.execute(query, params)
        conn.commit()


init_db()


# ------------------------------------------------------------
# STYLING
# ------------------------------------------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(180deg, #fff8fb 0%, #f8f4fa 100%);
    color: #302936;
    font-family: 'Helvetica Neue', sans-serif;
}
h1, h2, h3 { color: #573c63 !important; }
.lily-card {
    background: rgba(255,255,255,.94);
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #f1dce8;
    border-left: 5px solid #e5a4c5;
    box-shadow: 0 4px 14px rgba(75, 43, 74, .06);
    margin-bottom: 18px;
}
.soft-card {
    background: white;
    padding: 16px;
    border-radius: 12px;
    border: 1px solid #eee2eb;
    margin-bottom: 10px;
}
.small-muted { color: #786d7c; font-size: .88rem; }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------
# SHARED HELPERS
# ------------------------------------------------------------
if "who" not in st.session_state:
    st.session_state.who = None

def safe_text(value):
    return html.escape(str(value or ""))

def display_card(title, body, meta=""):
    st.markdown(
        f'<div class="soft-card"><strong>{safe_text(title)}</strong>'
        + (f'<div class="small-muted">{safe_text(meta)}</div>' if meta else "")
        + f'<p style="white-space:pre-wrap;margin-bottom:0">{safe_text(body)}</p></div>',
        unsafe_allow_html=True,
    )


# ------------------------------------------------------------
# ENTRANCE
# ------------------------------------------------------------
if st.session_state.who is None:
    st.markdown("""
    <div style="text-align:center;padding:35px 10px 20px">
      <div style="font-size:2.5rem">🌸 🌿</div>
      <h1>Our Shared Universe</h1>
      <p style="color:#766979;font-size:1.08rem">
        A small private sanctuary for curiosity, care, memories, and meaning.
      </p>
      <p>Built on mutual respect, empathy, and choosing to understand one another.</p>
    </div>
    """, unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            '<div style="background:#fff0f7;padding:22px;border-radius:16px;text-align:center;border:1px solid #f3c6dd">'
            '<h2 style="color:#b64d88!important">🌸 Lina</h2><p>Soft pinks, lilies, and nutritional care.</p></div>',
            unsafe_allow_html=True,
        )
        if st.button("Enter as Lina 🌸", use_container_width=True):
            st.session_state.who = "Lina"
            st.rerun()
    with c2:
        st.markdown(
            '<div style="background:#eef7f0;padding:22px;border-radius:16px;text-align:center;border:1px solid #c7e2cd">'
            '<h2 style="color:#36734f!important">🌿 Youssef</h2><p>Curiosity, engineering, philosophy, and quiet depth.</p></div>',
            unsafe_allow_html=True,
        )
        if st.button("Enter as Youssef 🌿", use_container_width=True):
            st.session_state.who = "Youssef"
            st.rerun()
    st.caption("Note: this is a profile selector, not a secure login. Anyone with access to the app can choose either profile.")
    st.stop()


# ------------------------------------------------------------
# HEADER + NAVIGATION
# ------------------------------------------------------------
c_head, c_switch = st.columns([4, 1])
with c_head:
    st.markdown(f"### {'🌸' if st.session_state.who == 'Lina' else '🌿'} Welcome back, {st.session_state.who}")
with c_switch:
    if st.button("Switch", use_container_width=True):
        st.session_state.who = None
        st.rerun()

tab_core, tab_nutrition, tab_solver, tab_media, tab_chat = st.tabs([
    "✨ Our Core & Notes",
    "🥗 Nutrition & Care",
    "🕊️ Philosophy Lab",
    "🎶 Songs & Memories",
    "💬 Shared Chat",
])


# ------------------------------------------------------------
# TAB 1: NOTES
# ------------------------------------------------------------
with tab_core:
    st.markdown('<div class="lily-card"><h3>Our Core Pillars</h3><p>Respect, empathy, curiosity, honest communication, and creating meaning together.</p></div>', unsafe_allow_html=True)
    st.subheader("💌 Leave a note")
    with st.form("note_form", clear_on_submit=True):
        note_text = st.text_area("Write a thought, a little reminder, or something sweet.")
        note_submit = st.form_submit_button("Save note")
    if note_submit:
        if note_text.strip():
            run(
                "INSERT INTO notes(author, text, created_at) VALUES (?, ?, ?)",
                (st.session_state.who, note_text.strip(), now_text()),
            )
            st.success("Saved for your shared universe.")
            st.rerun()
        else:
            st.warning("Write a note first.")
    st.subheader("Recent notes")
    for note in rows("SELECT * FROM notes ORDER BY id DESC LIMIT 100"):
        display_card(note["author"], note["text"], note["created_at"])


# ------------------------------------------------------------
# TAB 2: NUTRITION & CARE
# ------------------------------------------------------------
with tab_nutrition:
    st.markdown('<div class="lily-card"><h3>🥗 Nourish & Care Hub</h3><p>Gentle, general ideas for everyday wellbeing. Food and self-care suggestions are not medical treatment.</p></div>', unsafe_allow_html=True)
    topic = st.selectbox("What kind of support are you looking for?", [
        "Choose a topic...",
        "Period cramps & muscle tension",
        "Exhaustion & brain fog",
        "Stress & feeling overwhelmed",
        "Sleep & recovery",
        "Everyday balanced meals",
    ])
    tips = {
        "Period cramps & muscle tension": [
            "A warm pack or hot-water bottle may help ease cramps.",
            "Try regular meals and fluids; foods containing magnesium (such as nuts, seeds, legumes, and leafy greens) can be part of a balanced diet.",
            "Gentle movement may help some people, but rest is valid too. Seek medical advice if pain is severe, new, worsening, or disrupts daily life.",
        ],
        "Exhaustion & brain fog": [
            "Consider whether you have eaten regularly, had enough fluids, and slept enough.",
            "A snack combining carbohydrate and protein may be practical, such as fruit with yogurt or toast with eggs.",
            "Persistent or unexplained fatigue deserves medical assessment rather than assuming it is a nutrient deficiency.",
        ],
        "Stress & feeling overwhelmed": [
            "Try a slow, comfortable breathing rhythm or a short grounding exercise.",
            "Break the next task into a very small step and take a short screen break if helpful.",
            "Herbal products and supplements can have side effects or interactions; do not treat them as automatically safe.",
        ],
        "Sleep & recovery": [
            "Keep a reasonably consistent sleep and wake time where practical.",
            "A calmer wind-down routine and a darker, quieter room may help.",
            "If sleep problems persist or significantly affect daily life, consider speaking with a healthcare professional.",
        ],
        "Everyday balanced meals": [
            "Aim for variety across vegetables and fruit, carbohydrate sources, protein foods, and fats.",
            "Convenience foods can fit into a balanced diet; perfection is not required.",
            "Needs vary by person, activity, health, culture, and budget. Avoid rigid rules that create unnecessary stress.",
        ],
    }
    if topic in tips:
        for tip in tips[topic]:
            st.markdown(f"- {tip}")
    st.divider()
    st.subheader("🍲 Shared recipe vault")
    with st.form("recipe_form", clear_on_submit=True):
        recipe_title = st.text_input("Recipe or meal name")
        recipe_desc = st.text_area("Ingredients, method, or care notes")
        recipe_submit = st.form_submit_button("Save recipe")
    if recipe_submit:
        if recipe_title.strip():
            run(
                "INSERT INTO recipes(title, description, added_by, created_at) VALUES (?, ?, ?, ?)",
                (recipe_title.strip(), recipe_desc.strip(), st.session_state.who, now_text()),
            )
            st.success("Recipe saved.")
            st.rerun()
        else:
            st.warning("Add a recipe name first.")
    for recipe in rows("SELECT * FROM recipes ORDER BY id DESC LIMIT 100"):
        display_card(recipe["title"], recipe["description"], f"Added by {recipe['added_by']} · {recipe['created_at']}")


# ------------------------------------------------------------
# TAB 3: STRUCTURED AI ENGINE
# ------------------------------------------------------------
with tab_solver:
    st.markdown('<div class="lily-card"><h3>🕊️ Philosophy & Human Understanding Lab</h3><p>Explore a question through philosophy, psychology, and sociology without pretending uncertainty is certainty.</p></div>', unsafe_allow_html=True)
    question = st.text_area(
        "What question, dilemma, or situation are we examining?",
        placeholder="Example: Can love exist without possession?",
        height=130,
        key="philosophy_question",
    )
    lens_col, tone_col = st.columns(2)
    with lens_col:
        lens = st.selectbox("Primary philosophical lens", [
            "Integrated (choose relevant perspectives)",
            "Existentialism — meaning, freedom, responsibility",
            "Stoicism — judgment, virtue, what we control",
            "Aristotelian ethics — character and flourishing",
            "Utilitarianism — consequences and wellbeing",
            "Deontology — duties, principles, and respect",
            "Buddhist philosophy — suffering, impermanence, attachment",
            "Taoism — balance, change, and non-forcing",
        ])
    with tone_col:
        tone = st.selectbox("Style", [
            "Deep & Reflective", "Grounding & Practical",
            "Poetic & Warm", "Analytical & Precise",
        ])
    use_psychology = st.checkbox("Include psychology", value=True)
    use_sociology = st.checkbox("Include sociology", value=True)
    st.caption("The engine should examine possibilities, not diagnose people or invent motives.")
    if st.button("Explore the question 🌿", type="primary", use_container_width=True):
        if not question.strip():
            st.warning("Write a question first.")
        elif not HAS_GENAI:
            st.error("Google GenAI is not installed. Install dependencies from requirements.txt.")
        else:
            try:
                api_key = st.secrets.get("GEMINI_API_KEY", "")
            except Exception:
                api_key = ""
            if not api_key or api_key == "your_actual_gemini_api_key_here":
                st.error("API key missing. Add your real key to .streamlit/secrets.toml using the provided example.")
            else:
                system_rules = """
You are a careful, intellectually honest guide to philosophy, psychology,
sociology, and relationships. Reason from the actual question rather than
producing generic inspirational text.

Rules:
- Explain philosophical traditions accurately and apply them to the question.
- Never invent quotations, studies, statistics, sources, or citations.
- Separate facts, interpretations, and unknowns.
- If context is limited, give multiple plausible explanations and say what
  additional information would matter.
- Do not claim to know what either person thinks, feels, intends, or needs.
- Psychology concepts are lenses, not diagnoses. Do not diagnose or infer a
  person's attachment style or unconscious motives from a short description.
- Sociology may consider norms, culture, family expectations, institutions,
  gender roles, power, class, and belonging when relevant, without stereotyping.
- Respect autonomy, consent, and boundaries. Never recommend guilt or coercion.
- Do not force every discipline into every answer.
- Avoid clichés, repetition, false certainty, and empty profundity.
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
