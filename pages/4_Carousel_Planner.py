import streamlit as st
from utils.ui import inject_css, page_header
from utils.ai_engine import generate_carousel

st.set_page_config(page_title="Carousel Planner", page_icon="🎠", layout="wide")
inject_css()
page_header("🎠 Carousel Content Planner", "Turn any topic into a slide-by-slide LinkedIn carousel outline.")

topic = st.text_input("Carousel topic", placeholder="e.g. 5 lessons from building my final year project")
slides = st.slider("Number of slides", 4, 10, 6)

if st.button("✨ Generate Carousel Outline", use_container_width=True):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Structuring your carousel..."):
            slide_list = generate_carousel(topic, slides)
        for i, s in enumerate(slide_list, 1):
            st.markdown(
                f"""
                <div class="content-card">
                    <span class="pill">Slide {i}</span>
                    <div style="font-weight:700; margin-top:0.4rem;">{s['title']}</div>
                    <div style="color:#4A5568; margin-top:0.2rem;">{s['content']}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
