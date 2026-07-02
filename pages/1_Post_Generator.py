import streamlit as st
from utils.ui import inject_css, page_header
from utils.ai_engine import generate_post

st.set_page_config(page_title="Post Generator", page_icon="📝", layout="wide")
inject_css()
page_header("📝 LinkedIn Post Generator", "Turn any topic into a ready-to-publish LinkedIn post.")

col1, col2 = st.columns([1, 1])

with col1:
    topic = st.text_input("What's the post about?", placeholder="e.g. finishing my Final Year Project in AI")
    post_type = st.selectbox("Post type", ["Tips/How-To", "Story", "Achievement", "Thought Leadership", "Announcement"])
    tone = st.selectbox("Tone", ["Professional", "Casual", "Inspirational", "Bold/Contrarian"])
    length = st.select_slider("Length", options=["Short", "Medium", "Long"], value="Medium")
    generate_btn = st.button("✨ Generate Post", use_container_width=True)

with col2:
    st.markdown("#### Preview")
    if generate_btn:
        if not topic.strip():
            st.warning("Please enter a topic first.")
        else:
            with st.spinner("Writing your post..."):
                result = generate_post(topic, post_type, tone, length)
            st.markdown(f'<div class="content-card">{result["text"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
            st.text_area("Copy-ready text", result["text"], height=250)
            st.caption(f"Generated in **{result['mode'].upper()}** mode")
    else:
        st.markdown(
            '<div class="content-card" style="color:#94A3B8;">Your generated post will appear here.</div>',
            unsafe_allow_html=True,
        )

st.markdown("---")
st.caption("💡 Tip: Keep hashtags out of the post body — add 3-5 relevant ones as a comment instead for better reach (see Hashtag Generator).")
