import streamlit as st
from dotenv import load_dotenv
from utils.ui import inject_css, mode_badge

load_dotenv()

st.set_page_config(
    page_title="LinkedIn GenAI Content Studio",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

inject_css()

st.markdown(
    """
    <div style="text-align:center; padding: 1.5rem 0 0.5rem 0;">
        <h1>💼 LinkedIn GenAI Content Studio</h1>
        <p style="font-size:1.05rem; color:#4A5568;">
            One AI-powered toolkit to write, plan, and optimize everything you post on LinkedIn.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

col_a, col_b, col_c = st.columns([1, 1, 1])
with col_b:
    mode_badge()

st.markdown("---")

st.markdown("### 🚀 What's inside")

features = [
    ("📝", "Post Generator", "Generate ready-to-publish LinkedIn posts — tips, stories, achievements, thought leadership — in any tone."),
    ("🎣", "Hook Generator", "Get scroll-stopping opening lines that boost your post's reach in the first 2 seconds."),
    ("#️⃣", "Hashtag Generator", "Get relevant, high-reach hashtags tailored to your topic and industry."),
    ("🎠", "Carousel Planner", "Turn any topic into a slide-by-slide LinkedIn carousel outline."),
    ("👤", "Bio Optimizer", "Rewrite your headline and About section for maximum recruiter/algorithm visibility."),
    ("📅", "Content Calendar", "Get a ready-made weekly posting plan built around content pillars."),
]

cols = st.columns(3)
for i, (icon, name, desc) in enumerate(features):
    with cols[i % 3]:
        st.markdown(
            f"""
            <div class="content-card">
                <div style="font-size:1.8rem;">{icon}</div>
                <div style="font-weight:700; font-size:1.05rem; margin:0.3rem 0;">{name}</div>
                <div style="font-size:0.9rem; color:#4A5568;">{desc}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("---")
st.info(
    "👈 Use the sidebar to navigate between tools. Works instantly in **Demo Mode** "
    "(no API key needed) — or plug in your OpenAI/Grok API key for **Live AI Mode** "
    "with richer, more dynamic generations. See the README for setup."
)

st.markdown(
    """
    <div style="text-align:center; padding-top:2rem; color:#94A3B8; font-size:0.85rem;">
        Built with ❤️ using Streamlit — LinkedIn GenAI Content Studio
    </div>
    """,
    unsafe_allow_html=True,
)
