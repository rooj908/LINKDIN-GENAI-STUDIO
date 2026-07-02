"""Shared UI helpers / theme for LinkedIn GenAI Content Studio."""
import streamlit as st
from utils.ai_engine import is_live_mode

LINKEDIN_BLUE = "#0A66C2"
DARK_NAVY = "#0B1F3A"
LIGHT_BG = "#F3F6F8"


def inject_css():
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-color: {LIGHT_BG};
        }}
        section[data-testid="stSidebar"] {{
            background-color: {DARK_NAVY};
        }}
        section[data-testid="stSidebar"] * {{
            color: #F3F6F8 !important;
        }}
        h1, h2, h3 {{
            color: {DARK_NAVY};
        }}
        .stButton>button {{
            background-color: {LINKEDIN_BLUE};
            color: white;
            border-radius: 6px;
            border: none;
            padding: 0.5rem 1.2rem;
            font-weight: 600;
        }}
        .stButton>button:hover {{
            background-color: #084d94;
            color: white;
        }}
        .content-card {{
            background-color: white;
            border-radius: 10px;
            padding: 1.3rem 1.5rem;
            border: 1px solid #E3E8ED;
            box-shadow: 0 1px 4px rgba(0,0,0,0.05);
            margin-bottom: 1rem;
        }}
        .pill {{
            display: inline-block;
            background-color: #E7F0FA;
            color: {LINKEDIN_BLUE};
            padding: 3px 12px;
            border-radius: 999px;
            font-size: 0.8rem;
            font-weight: 600;
            margin-right: 6px;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


def mode_badge():
    if is_live_mode():
        st.markdown(
            '<span class="pill" style="background:#E6F7EC;color:#1A7F37;">🟢 Live AI Mode</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span class="pill" style="background:#FFF4E5;color:#B76E00;">🟡 Demo Mode (no API key set)</span>',
            unsafe_allow_html=True,
        )


def page_header(title: str, subtitle: str = ""):
    st.markdown(f"## {title}")
    if subtitle:
        st.caption(subtitle)
    mode_badge()
    st.markdown("---")
