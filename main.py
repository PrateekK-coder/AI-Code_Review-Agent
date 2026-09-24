"""
AI-Powered Code Review Agent - Production Streamlit Application.
"""

import streamlit as st
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration - must be the first Streamlit command
st.set_page_config(
    page_title="AI Code Review Agent",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

from app.ui.styles import inject_theme
from app.ui.state import (
    init_session_state,
    PAGE_HOME,
    PAGE_FILE_REVIEW,
    PAGE_REPO_REVIEW,
    PAGE_SEMANTIC_SEARCH
)
from app.views.home_view import render_home_view
from app.views.file_review_view import render_file_review_view
from app.views.repo_review_view import render_repo_review_view
from app.views.semantic_search_view import render_semantic_search_view

# Initialize session state & inject custom CSS design system
init_session_state()
inject_theme()

# -------------------------------------------------------------
# Sidebar Navigation & System Status
# -------------------------------------------------------------
with st.sidebar:
    # Brand Identity Header
    st.markdown(
        """
        <div style="padding: 0.5rem 0.25rem 1.25rem 0.25rem; border-bottom: 1px solid var(--border-subtle); margin-bottom: 1.25rem;">
            <div style="display: flex; align-items: center; gap: 0.6rem;">
                <span style="font-size: 1.4rem;">⬡</span>
                <span style="font-size: 1.05rem; font-weight: 700; letter-spacing: -0.01em; color: #ffffff;">
                    AI CODE REVIEW
                </span>
            </div>
            <div style="font-size: 0.75rem; color: var(--text-muted); margin-top: 0.3rem; font-family: var(--font-mono);">
                Autonomous Code Intelligence
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div style="font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.6rem; padding-left: 0.25rem;">
            Navigation
        </div>
        """,
        unsafe_allow_html=True
    )

    nav_pages = [
        {"id": PAGE_HOME, "label": "⌂  Home"},
        {"id": PAGE_FILE_REVIEW, "label": "▣  File Review"},
        {"id": PAGE_REPO_REVIEW, "label": "◫  Repository Review"},
        {"id": PAGE_SEMANTIC_SEARCH, "label": "⌕  Semantic Search"}
    ]

    for item in nav_pages:
        is_active = st.session_state.current_page == item["id"]
        btn_type = "primary" if is_active else "secondary"
        if st.button(item["label"], key=f"nav_{item['id']}", type=btn_type, use_container_width=True):
            st.session_state.current_page = item["id"]
            st.rerun()

    # Context & System Diagnostics Box at bottom of sidebar
    st.markdown("<div style='margin-top: 3rem;'></div>", unsafe_allow_html=True)
    
    active_repo = st.session_state.get("active_repo_name", "None loaded")
    indexed_files = len(st.session_state.get("active_code_files") or [])
    
    st.markdown(
        f"""
        <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 8px; padding: 0.85rem; font-family: var(--font-mono); font-size: 0.75rem;">
            <div style="font-weight: 700; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.5rem; letter-spacing: 0.05em;">
                System Status
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                <span style="color: var(--text-secondary);">Model:</span>
                <span style="color: #60a5fa;">GPT-4o Mini</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                <span style="color: var(--text-secondary);">Store:</span>
                <span style="color: #34d399;">ChromaDB</span>
            </div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                <span style="color: var(--text-secondary);">Active Repo:</span>
                <span style="color: #f1f5f9; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; max-width: 110px;">
                    {active_repo}
                </span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: var(--text-secondary);">Indexed Files:</span>
                <span style="color: #f1f5f9;">{indexed_files}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -------------------------------------------------------------
# Main Content View Router
# -------------------------------------------------------------
current_page = st.session_state.current_page

if current_page == PAGE_HOME:
    render_home_view()
elif current_page == PAGE_FILE_REVIEW:
    render_file_review_view()
elif current_page == PAGE_REPO_REVIEW:
    render_repo_review_view()
elif current_page == PAGE_SEMANTIC_SEARCH:
    render_semantic_search_view()
else:
    render_home_view()
