"""
Session State Management for AI Code Review Agent.
Manages application routing, active repository, vector index cache, and review results.
"""

import streamlit as st
from typing import Optional, List, Any
from app.models.code import CodeFile
from app.models.review import CodeReview

PAGE_HOME = "HOME"
PAGE_FILE_REVIEW = "FILE REVIEW"
PAGE_REPO_REVIEW = "REPOSITORY REVIEW"
PAGE_SEMANTIC_SEARCH = "SEMANTIC SEARCH"

def init_session_state():
    """Initializes standard session state keys if not already set."""
    defaults = {
        "current_page": PAGE_HOME,
        
        # File Review State
        "uploaded_file_info": None,  # {"name": ..., "size": ..., "language": ..., "content": ...}
        "file_review_result": None,  # CodeReview object
        "file_review_loading": False,
        
        # Repository Review State
        "repo_url": "https://github.com/PrateekK-coder/Wish_List-App.git",
        "active_repo_name": None,
        "active_repo_path": None,
        "active_code_files": None,   # List[CodeFile]
        "active_chunks": None,       # List[Document]
        "active_vector_store": None, # ChromaStore
        "repo_review_result": None,  # Aggregated dict from ReviewAgentAggregator
        "repo_review_loading": False,
        
        # Semantic Search State
        "semantic_query": "",
        "semantic_results": None,    # List[CodeReview]
        "semantic_loading": False,
        
        # System notification / error
        "app_error": None
    }
    
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val

def navigate_to(page_name: str):
    """Navigates to a specific page and triggers rerun."""
    st.session_state.current_page = page_name
    st.session_state.app_error = None
    st.rerun()

