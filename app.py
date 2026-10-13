# ==========================================
    # TAB 3: DEDICATED AI PHILOSOPHY ENGINE
    # ==========================================
    with tab_solver:
        st.markdown('<div class="lily-card">', unsafe_allow_html=True)
        st.subheader("🕊️ The Dedicated Philosophy & Existential Engine")
        st.write("An AI trained and prompted exclusively as a master of philosophy (Existentialism, Stoicism, Taoism, and Ethics). Enter any tension or question below, and it will break down your dilemma through the lens of timeless wisdom.")
        st.markdown('</div>', unsafe_allow_html=True)

        # Extended Philosophy Quote Pool for fallback/inspiration
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

                # Generate AI analysis using Gemini with specialized philosophy persona
                ai_analysis = ""
                if HAS_GENAI and "GEMINI_API_KEY" in st.secrets:
                    try:
                        client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])
                        prompt = f"""
                        You are a dedicated Philosophy & Existential AI Engine built specifically for Youssef and Lina (who have been together since high school, value deep mutual respect, empathy, and existentialism). 
                        They are analyzing this situation/tension: "{problem_input}".
                        The selected philosophical lens is: {philosopher_focus}.
                        The desired tone is: {tone_focus}.

                        Provide a brilliant, non-repetitive, deeply engaging breakdown. Do not sound like a generic chatbot. Use real philosophical principles, honor their shared history, and offer actionable, grounded wisdom for how two partners who respect each other can navigate this together.
                        """
                        response = client.models.generate_content(model="gemini-2.5-flash", contents=prompt)
                        ai_analysis = response.text
                    except Exception:
                        ai_analysis = None

                if not ai_analysis:
                    # Sophisticated Fallback if API key isn't active yet
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
                """, unsafe_app_html=True)
            else:
                st.warning("Please type a question or tension above before consulting the engine.")
