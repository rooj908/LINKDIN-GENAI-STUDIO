import streamlit as st
from utils.ui import inject_css, page_header
from utils.ai_engine import generate_hashtags

st.set_page_config(page_title="Hashtag Generator", page_icon="#️⃣", layout="wide")
inject_css()
page_header("#️⃣ Hashtag Generator", "Get relevant, high-reach hashtags for your post.")

topic = st.text_input("Topic / industry", placeholder="e.g. AI, career growth, final year project")
count = st.slider("Number of hashtags", 5, 15, 10)

if st.button("✨ Generate Hashtags", use_container_width=True):
    if not topic.strip():
        st.warning("Please enter a topic first.")
    else:
        with st.spinner("Finding hashtags..."):
            tags = generate_hashtags(topic, count)
        st.markdown(
            f'<div class="content-card">{" ".join(f"<span class=\'pill\'>{t}</span>" for t in tags)}</div>',
            unsafe_allow_html=True,
        )
        st.text_area("Copy-ready", " ".join(tags), height=100)
        st.caption("💡 Best practice: use 3-5 in your post/comment, not all of them at once.")
