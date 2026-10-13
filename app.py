
import streamlit as st
import random

st.set_page_config(
    page_title="Our Little Universe ♡",
    page_icon="🌷",
    layout="centered",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Playfair+Display:ital,wght@0,500;0,600;1,500&display=swap');

.stApp {
    background: linear-gradient(160deg, #fff5f9, #fffafd 55%, #fce9f1);
    color: #684454;
    font-family: 'DM Sans', sans-serif;
}
h1, h2, h3 {
    font-family: 'Playfair Display', serif !important;
    color: #b54f7b !important;
}
.hero {
    text-align: center;
    padding: 30px 12px;
    border: 1px solid #f3d4e1;
    border-radius: 24px;
    background: rgba(255,255,255,.78);
}
.flower { font-size: 55px; }
.subtitle { color: #98677e; font-style: italic; }
.love-card {
    padding: 20px;
    border-radius: 18px;
    background: #fff;
    border: 1px solid #f3dce6;
    margin: 10px 0;
}
div.stButton > button {
    border-radius: 14px;
    border: 1px solid #e8b7cc;
    background: #f8e1eb;
    color: #8d3e62;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
  <div class="flower">🌷</div>
  <h1>Our Little Universe ♡</h1>
  <p class="subtitle">A little corner of the world, made just for you.</p>
  <p>For my favourite girl — and all the little things that make you YOU.</p>
</div>
""", unsafe_allow_html=True)

st.write("")

page = st.radio(
    "Explore our little world",
    ["Home ♡", "Lily Garden 🌷", "Nutrition Corner 🍓", "Little Love Notes 💌"],
    horizontal=True,
    label_visibility="collapsed",
)

if page == "Home ♡":
    st.markdown("## To my favourite person 💗")
    st.write(
        "If I could give you a little place in the universe, "
        "it would look something like this. Pink skies, peaceful "
        "moments, your favourite flowers, and reminders that you are loved."
    )
    st.markdown("""
    <div class="love-card">
      <h3>🌸 A little reminder</h3>
      You don't have to do everything perfectly. I hope you always
      make room for your own happiness while chasing your dreams.
    </div>
    """, unsafe_allow_html=True)

elif page == "Lily Garden 🌷":
    st.markdown("## A garden just for you")
    st.write("Pick a flower. Each one has a little message for you.")
    notes = [
        "You make ordinary days feel special. ♡",
        "I hope your dreams grow as beautifully as these flowers.",
        "You deserve kindness, rest, and so much happiness.",
        "If I could, I'd bring you lilies just to see you smile.",
        "One tiny flower, one big reminder: you are loved.",
    ]
    cols = st.columns(3)
    for i, col in enumerate(cols):
        with col:
            if st.button(["🌷", "🤍", "🌸"][i], key=f"flower{i}"):
                st.session_state.flower_note = notes[i]
    if st.button("Grow another flower 🌱"):
        st.session_state.flower_note = random.choice(notes)
    if st.session_state.get("flower_note"):
        st.success(st.session_state.flower_note)

elif page == "Nutrition Corner 🍓":
    st.markdown("## For my future nutritionist 🥗")
    st.write(
        "A little corner celebrating something you love. "
        "Your curiosity, your studies, and all the good you hope "
        "to bring into the world matter."
    )
    st.markdown("""
    <div class="love-card">
      <h3>🍓 Today's gentle reminder</h3>
      Food is nourishment, culture, enjoyment, and connection.
      Your future work can help people build a healthier relationship
      with food, one thoughtful step at a time.
    </div>
    """, unsafe_allow_html=True)
    st.write("A tiny study break:")
    if st.button("Give me a study-break reminder ✨"):
        st.info(random.choice([
            "Relax your shoulders, breathe, and take a little break.",
            "One topic at a time. Progress doesn't need to be perfect.",
            "Drink some water, stretch, and be proud of your effort.",
            "Rest is part of learning, too. You've got this. ♡",
        ]))

elif page == "Little Love Notes 💌":
    st.markdown("## A few words for you")
    st.write("For the moments when you need a little extra love.")
    options = {
        "When you need encouragement": (
            "I believe in you, even on the days when you doubt yourself. ♡"
        ),
        "When studying gets stressful": (
            "You are more than your grades or your productivity. "
            "Take a breath. I'm cheering for you."
        ),
        "When you need a smile": (
            "Official reminder: someone thinks you're ridiculously special. 💗"
        ),
        "When you miss me": (
            "Imagine a big hug from me, lasting exactly as long as you need."
        ),
    }
    choice = st.selectbox("Open a little note", list(options.keys()))
    if st.button("Open my letter 💌", type="primary"):
        st.markdown(
            f'<div class="love-card">{options[choice]}</div>',
            unsafe_allow_html=True,
        )

st.write("")
st.divider()
st.markdown(
    "<p style='text-align:center;color:#b87b96'>"
    "Made with love, a little pink, and lots of heart ♡"
    "</p>",
    unsafe_allow_html=True,
)
