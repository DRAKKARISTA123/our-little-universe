import streamlit as st
import random
from datetime import datetime

# Optional: Try importing Google GenAI for live AI philosophy & wellness advice
try:
    from google import genai
    HAS_GENAI = True
except ImportError:
    HAS_GENAI = False

# 1. Page Configuration
st.set_page_config(
    page_title="Our Shared Universe",
    page_icon="🌸",
    layout="centered"
)

# 2. Custom Styling (Blending Lina's Pink/Lilies & Youssef's Green/Purple/Blue)
st.markdown("""
    <style>
    .stApp {
        background-color: #faf4f7;
        color: #2b2b2b;
        font-family: 'Helvetica Neue', sans-serif;
    }
    h1, h2, h3 {
        color: #4a2e5d !important; /* Deep Purple */
    }
    .lily-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border-left: 6px solid #e27d60; /* Soft Pink/Coral Accent */
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .youssef-card {
        background-color: #ffffff;
        padding: 24px;
        border-radius: 16px;
        border-left: 6px solid #72a0c1; /* Calm Blue/Green Accent */
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    .quote-box {
        background-color: #f3e8f0;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #e8d7e3;
        font-style: italic;
        color: #4a2e5d;
        margin-bottom: 20px;
    }
    .entrance-container {
        text-align: center;
        padding: 40px 20px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Session State Initialization
if 'who' not in st.session_state:
    st.session_state.who = None
if 'notes' not in st.session_state:
    st.session_state.notes = [
        {"author": "Youssef", "text": "High school crush turned into my favorite reality. Respect & empathy always.", "time": "Foundation"}
    ]
if 'recipes' not in st.session_state:
    st.session_state.recipes = [
        {"title": "Post-Workout Magnesium Smoothie", "desc": "Spinach, banana, almond milk, and dark cocoa for calm energy.", "added_by": "Lina"}
    ]
if 'songs' not in st.session_state:
    st.session_state.songs = [
        {"title": "Our Song of the Universe", "artist": "Timeless", "note": "Plays whenever we talk late at night."}
    ]
if 'memories' not in st.session_state:
    st.session_state.memories = [
        {"title": "The Beginning", "desc": "Back in high school when I first noticed you.", "date": "The Origin"}
    ]

# ==========================================
# 4. ENTRANCE GATE (Pink Cube vs Green Cube)
# ==========================================
if st.session_state.who is None:
    st.markdown("""
        <div class="entrance-container">
            <h1>🌱 Our Shared Universe</h1>
            <p style="color: #666; font-size: 1.1rem;">A private sanctuary built on mutual respect, empathy, and meaning.</p>
            <hr style="width: 50%; margin: 20px auto; border: 0; border-top: 1px solid #ddd;">
            <h3>Who is entering today?</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background-color: #fce8f3; padding: 30px; border-radius: 16px; text-align: center; border: 2px solid #f3a6d2;">
            <h2 style="color: #c75b9b !important;">🌸 Lina</h2>
            <p>Soft pinks, lilies, and nutritional care.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter as Lina 🌸", use_container_width=True):
            st.session_state.who = "Lina"
            st.rerun()
            
    with col2:
        st.markdown("""
        <div style="background-color: #e3f2e6; padding: 30px; border-radius: 16px; text-align: center; border: 2px solid #a3d9a5;">
            <h2 style="color: #3b7a57 !important;">🌿 Youssef</h2>
            <p>Earthy greens, philosophy, and quiet depth.</p>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Enter as Youssef 🌿", use_container_width=True):
            st.session_state.who = "Youssef"
            st.rerun()

else:
    # Header showing who is logged in
    user_color = "#c75b9b" if st.session_state.who == "Lina" else "#3b7a57"
    st.markdown(f"""
        <div style="display: flex; justify-content: space-between; align-items: center; background: white; padding: 10px 20px; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom: 20px;">
            <span style="font-weight: bold; color: {user_color}; font-size: 1.2rem;">Welcome back, {st.session_state.who} 💜</span>
    """, unsafe_allow_html=True)
    if st.button("Switch User"):
        st.session_state.who = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # Main Navigation Tabs
    tab_core, tab_nutrition, tab_solver, tab_media = st.tabs([
        "✨ The Core & Notes", 
        "🥗 Nutrition & Care Alleviation", 
        "🕊️ AI Philosophy Solver", 
        "🎶 Songs & Memories"
    ])

    # ==========================================
    # TAB 1: THE CORE & NOTES
    # ==========================================
    with tab_core:
        st.markdown('<div class="lily-card">', unsafe_allow_html=True)
        st.subheader("Our Core Pillars")
        st.write("Built on mutual respect, deep empathy, and crafting our own meaning in this universe.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### 💭 Leave a Note for Each Other")
        with st.form("note_form"):
            new_note = st.text_area("Write something sweet, a thought, or an existential realization:")
            submitted = st.form_submit_button("Post Note")
            if submitted and new_note:
                st.session_state.notes.insert(0, {
                    "author": st.session_state.who,
                    "text": new_note,
                    "time": datetime.now().strftime("%b %d, %H:%M")
                })
                st.success("Note pinned to our board! 🌸")
                
        st.markdown("### Recent Notes & Messages")
        for note in st.session_state.notes:
            st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #6b4c7a;">
                <strong>{note['author']}</strong> <span style="font-size: 0.8rem; color: #888;">({note['time']})</span>
                <p style="margin-top: 5px;">{note['text']}</p>
            </div>
            """, unsafe_allow_html=True)

    # ==========================================
    # TAB 2: NUTRITION & CARE ALLEVIATION
    # ==========================================
    with tab_nutrition:
        st.markdown('<div class="youssef-card">', unsafe_allow_html=True)
        st.subheader("🥗 Nourish & Care Hub")
        st.write("Tailored nutrition insights, soothing wellness rituals, and gentle strategies for physical and emotional well-being (cramps, fatigue, burnout, or daily energy).")
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown("#### 🩺 Physical & Emotional Relief Guide")
        relief_topic = st.selectbox(
            "What support or alleviation do you need right now?",
            ["Choose a topic...", "Period Cramps & Muscle Tension", "Exhaustion & Brain Fog", "Anxiety / Stress Overload", "Deep Sleep & Recovery"]
        )

        if relief_topic != "Choose a topic...":
            if relief_topic == "Period Cramps & Muscle Tension":
                st.info("🌿 **Nutritional & Care Strategy for Cramps:**")
                st.write("- **Magnesium-rich foods:** Dark chocolate, pumpkin seeds, and spinach help relax uterine muscles.")
                st.write("- **Anti-inflammatory warmth:** Ginger and turmeric tea paired with a warm compress.")
                st.write("- **Gentle Movement:** Light stretching and zero pressure to do heavy tasks today.")
            elif relief_topic == "Exhaustion & Brain Fog":
                st.info("⚡ **Energy & Focus Restoration:**")
                st.write("- **Complex Carbohydrates & Protein:** Pairing berries with Greek yogurt or nuts to stabilize blood sugar.")
                st.write("- **Hydration Check:** Often fatigue stems from electrolyte imbalance—add a pinch of sea salt and lemon to water.")
                st.write("- **The Philosophy Break:** Step away from screens for 15 minutes and breathe.")
            elif relief_topic == "Anxiety / Stress Overload":
                st.info("🧘 **Calming the Nervous System:**")
                st.write("- **Adaptogens / Chamomile:** Chamomile or Ashwagandha tea to lower cortisol.")
                st.write("- **Box Breathing:** 4 seconds in, 4 hold, 4 out, 4 hold.")
            elif relief_topic == "Deep Sleep & Recovery":
                st.info("🌙 **Rest Rituals:**")
                st.write("- **Tart Cherry Juice or Warm Milk:** Natural sources of melatonin and tryptophan.")
                st.write("- **Digital Sunset:** Dimming lights 30 minutes before sleep.")

        st.markdown("---")
        st.markdown("### 🍲 Shared Recipe Vault")
        with st.form("recipe_form"):
            r_title = st.text_input("Recipe / Meal Name")
            r_desc = st.text_area("Ingredients & Care Notes")
            r_submit = st.form_submit_button("Save Recipe")
            if r_submit and r_title:
                st.session_state.recipes.append({"title": r_title, "desc": r_desc, "added_by": st.session_state.who})
                st.success("Recipe saved into our kitchen vault!")

        for r in st.session_state.recipes:
            st.markdown(f"""
            <div style="background: white; padding: 15px; border-radius: 10px; margin-bottom: 10px; border-left: 4px solid #e27d60;">
                <strong>{r['title']}</strong> <span style="font-size: 0.8rem; color: #888;">(Added by {r['added_by']})</span>
                <p style="margin-top: 5px;">{r['desc']}</p>
            </div>
            """, unsafe_allow_html=True)

    # ==========================================
    # TAB 3: DEDICATED PHILOSOPHY ENGINE
    # ==========================================
    with tab_solver:
        st.markdown('<div class="lily-card">', unsafe_allow_html=True)
        st.subheader("🕊️ The Dedicated Philosophy & Existential Engine")
        st.write("An AI prompt-engineered exclusively as a master of philosophy. Enter any tension or question below to break it down through timeless wisdom.")
        st.markdown('</div>', unsafe_allow_html=True)

        philosophy_quotes = [
            {"quote": "We do not encounter ourselves accidentally. We build our meaning through how we care for one another.", "school": "Existentialism (Sartre-inspired)"},
            {"quote": "Between stimulus and response there is a space. In that space is our power to choose our response.", "school": "Stoicism (Viktor Frankl)"},
            {"quote": "The ultimate test of relationship is not agreeing on everything, but walking through disagreement with absolute mutual respect.", "school": "Modern Ethics"},
            {"quote": "Water is fluid, soft, and yielding. Yet water will wear away rock, which is rigid and cannot yield.", "school": "Taoism (Lao Tzu)"},
            {"quote": "To be deeply understood by someone who loves you is a profound anchor in an indifferent universe.", "school": "Philosophical Romanticism"},
            {"quote": "Man is condemned to be free; because once thrown into the world, he is responsible for everything he does.", "school": "Jean-Paul Sartre"}
        ]

        problem_input = st.text_area("What philosophical question, life hurdle, or relationship tension are we examining today?")
        
        col_lens1, col_lens2 = st.columns(2)
        with col_lens1:
            philosopher_focus = st.selectbox(
                "Primary Philosophical Lens",
                ["Integrated (All Schools)", "Existentialism (Sartre / Camus - Creating Meaning)", "Stoicism (Aurelius / Frankl - Inner Calm & Control)", "Eastern Philosophy (Lao Tzu / Balance & Flow)"]
            )
        with col_lens2:
            tone_focus = st.selectbox(
                "Engine Tone",
                ["Deep & Reflective", "Grounding & Practical", "Poetic & Warm"]
            )

        if st.button("Consult the Philosophy AI Engine 🔮", use_container_width=True):
            if problem_input:
                selected_quote = random.choice(philosophy_quotes)
                
                st.markdown(f"""
                <div class="quote-box">
                    "{selected_quote['quote']}"<br>
                    <div style="text-align: right; font-size: 0.85rem; margin-top: 8px; color: #6b4c7a;">— <em>{selected_quote['school']}</em></div>
                </div>
                """, unsafe_allow_html=True)

                ai_analysis = ""
                if HAS_GENAI and "GEMINI_API_KEY" in st.secrets:
                    try:
                        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                        prompt = f"""
                        You are a dedicated Philosophy & Existential AI Engine built specifically for Youssef and Lina (who have been together since high school, value deep mutual respect, empathy, and existentialism). 
                        They are analyzing this situation/tension: "{problem_input}".
                        The selected philosophical lens is: {philosopher_focus}.
                        The desired tone is: {tone_focus}.

                        Provide a brilliant, non-repetitive, deeply engaging breakdown. Do not sound like a generic chatbot. Use real philosophical principles, honor their shared history, and offer actionable, grounded wisdom.
                        """
                        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                        ai_analysis = response.text
                    except Exception:
                        ai_analysis = None

                if not ai_analysis:
                    ai_analysis = f"""
                    **Existential & Philosophical Breakdown:**
                    When looking at '{problem_input}' through the lens of **{philosopher_focus}**, remember that human relationships are the ultimate canvas where we create our own meaning. 
                    - **The Reality:** Friction is proof that two independent minds are colliding and caring enough to communicate.
                    - **The Path Forward:** Lean into your core pillars of absolute respect and empathy. Strip away the ego, remember where you started back in high school, and treat this moment not as a conflict between you two, but as a puzzle for the two of you to solve side-by-side.
                    """

                st.markdown("### 🏛️ Engine Analysis & Guidance")
                st.markdown(f"""
                <div style="background: white; padding: 20px; border-radius: 12px; border-left: 5px solid #4a2e5d; line-height: 1.6;">
                {ai_analysis}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("Please type a question or tension above before consulting the engine.")


    # ==========================================
    # TAB 4: INTERACTIVE SONGS & MUSIC VAULT
    # ==========================================
    with tab_media:
        st.markdown('<div class="youssef-card">', unsafe_allow_html=True)
        st.subheader("🎶 Interactive Music Vault & 📸 Memory Timeline")
        st.write("Upload audio files or share track links so you can listen to each other's music taste directly inside our sanctuary.")
        st.markdown('</div>', unsafe_allow_html=True)

        col_song, col_mem = st.columns(2)

        with col_song:
            st.markdown("#### 🎧 Share & Listen to Songs")
            
            # File Uploader so she/you can upload MP3s directly
            uploaded_file = st.file_uploader("Upload an audio file (.mp3, .wav)", type=["mp3", "wav"])
            song_title_input = st.text_input("Song Name / Artist", key="upload_title")
            why_input = st.text_input("Why this song?", key="upload_why")
            
            if st.button("Save & Share Track 🎵"):
                if uploaded_file is not None or song_title_input:
                    new_track = {
                        "title": song_title_input if song_title_input else uploaded_file.name,
                        "note": why_input if why_input else "Added to our playlist",
                        "added_by": st.session_state.who,
                        "audio_bytes": uploaded_file.read() if uploaded_file else None
                    }
                    st.session_state.songs.insert(0, new_track)
                    st.success("Track uploaded to our vault!")
                    st.rerun()

            st.markdown("---")
            st.markdown("##### 🔊 Our Shared Tracks")
            
            for s in st.session_state.songs:
                st.markdown(f"""
                <div style="background: white; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #c75b9b;">
                    🎶 <strong>{s.get('title', 'Untitled')}</strong> <span style="font-size: 0.8rem; color: #888;">(Added by {s.get('added_by', 'Us')})</span><br>
                    <span style="font-size: 0.85rem; color: #666;">{s.get('note', '')}</span>
                </div>
                """, unsafe_allow_html=True)
                
                # If an actual audio file was uploaded, render a playable audio bar!
                if s.get("audio_bytes"):
                    st.audio(s["audio_bytes"], format="audio/mp3")

        with col_mem:
            st.markdown("#### 📜 Memory Timeline")
            with st.form("mem_form"):
                m_title = st.text_input("Milestone / Memory Title")
                m_desc = st.text_area("Short description")
                m_sub = st.form_submit_button("Add Memory")
                if m_sub and m_title:
                    st.session_state.memories.append({"title": m_title, "desc": m_desc, "date": "Recent"})
                    st.success("Memory saved!")

            for m in st.session_state.memories:
                st.markdown(f"""
                <div style="background: white; padding: 12px; border-radius: 8px; margin-bottom: 8px; border-left: 3px solid #72a0c1;">
                    ✨ <strong>{m['title']}</strong><br><span style="font-size: 0.85rem; color: #666;">{m['desc']}</span>
                </div>
                """, unsafe_allow_html=True)
