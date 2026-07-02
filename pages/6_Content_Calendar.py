import streamlit as st
import pandas as pd
from utils.ui import inject_css, page_header
from utils.ai_engine import generate_content_calendar

st.set_page_config(page_title="Content Calendar", page_icon="📅", layout="wide")
inject_css()
page_header("📅 Content Calendar Planner", "Get a ready-made weekly posting plan built around content pillars.")

theme = st.text_input("Overall theme/niche", placeholder="e.g. AI & Data Science journey")
days = st.slider("Number of days to plan", 3, 14, 7)

if st.button("✨ Generate Calendar", use_container_width=True):
    if not theme.strip():
        st.warning("Please enter a theme first.")
    else:
        calendar = generate_content_calendar(theme, days)
        df = pd.DataFrame(calendar)
        df.columns = ["Day", "Content Pillar", "Suggestion"]
        st.dataframe(df, use_container_width=True, hide_index=True)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download as CSV", csv, "linkedin_content_calendar.csv", "text/csv")
