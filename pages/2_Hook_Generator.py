import streamlit as st
from utils.ui import inject_css, page_header
from utils.ai_engine import generate_hooks

st.set_page_config(page_title="Hook Generator", page_icon="🎣", layout="wide")
inject_css()
page_header("🎣 Hook Generator", "Get scroll-stopping opening lines for your next post.")

topic = st.text_input("Topic", placeholder="e.g. switching careers into data science")
count = st.slider("Number of hooks", 3, 10, 6)

if st.button("✨ Generate Hooks", use_container_width=True):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Brainstorming hooks..."):
            hooks = generate_hooks(topic, count)
        for i, h in enumerate(hooks, 1):
            st.markdown(f'<div class="content-card">**{i}.** {h}</div>', unsafe_allow_html=True)
