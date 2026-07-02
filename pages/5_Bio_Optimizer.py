import streamlit as st
from utils.ui import inject_css, page_header
from utils.ai_engine import optimize_bio

st.set_page_config(page_title="Bio Optimizer", page_icon="👤", layout="wide")
inject_css()
page_header("👤 LinkedIn Bio/Headline Optimizer", "Get an optimized headline and About section.")

col1, col2 = st.columns(2)
with col1:
    target_role = st.text_input("Target role", placeholder="e.g. AI/Data Science Student & Aspiring ML Engineer")
with col2:
    industry = st.text_input("Industry", placeholder="e.g. Artificial Intelligence")

current_bio = st.text_area("Current headline/bio (optional)", placeholder="Paste your current LinkedIn headline or About section...")

if st.button("✨ Optimize", use_container_width=True):
    if not target_role.strip() or not industry.strip():
        st.warning("Please fill in target role and industry.")
    else:
        with st.spinner("Optimizing your profile..."):
            result = optimize_bio(current_bio, target_role, industry)
        st.markdown(f'<div class="content-card">{result["text"].replace(chr(10), "<br>")}</div>', unsafe_allow_html=True)
        st.text_area("Copy-ready text", result["text"], height=250)
        st.caption(f"Generated in **{result['mode'].upper()}** mode")
