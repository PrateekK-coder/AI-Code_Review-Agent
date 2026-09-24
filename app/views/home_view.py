"""
Home / Dashboard View for AI Code Review Agent.
"""

import streamlit as st
from app.ui.state import navigate_to, PAGE_FILE_REVIEW, PAGE_REPO_REVIEW, PAGE_SEMANTIC_SEARCH

def render_home_view():
    """Renders the professional landing dashboard."""
    
    # -------------------------------------------------------------
    # Hero Section (Compact, Technical, Developer-Grade)
    # -------------------------------------------------------------
    st.markdown(
        """
        <div style="padding: 1.5rem 0 2rem 0; max-width: 800px;">
            <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.8rem;">
                <span class="cr-feature-badge">v1.0 • Autonomous Engine</span>
                <span style="font-family: var(--font-mono); font-size: 0.75rem; color: var(--text-muted);">
                    AST & Semantic Indexing Active
                </span>
            </div>
            <h1 style="font-size: 2.35rem; font-weight: 700; letter-spacing: -0.03em; color: #ffffff; margin: 0 0 0.6rem 0; line-height: 1.2;">
                AI Code Review Agent
            </h1>
            <p style="font-size: 1.05rem; color: var(--text-secondary); line-height: 1.6; margin: 0;">
                Intelligent code analysis for files, repositories, and targeted engineering issues.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    st.markdown(
        """
        <div style="font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 1rem;">
            Select Review Mode
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # -------------------------------------------------------------
    # Three Premium Feature Cards
    # -------------------------------------------------------------
    col1, col2, col3 = st.columns(3, gap="medium")
    
    with col1:
        st.markdown(
            """
            <div class="cr-feature-card">
                <div>
                    <span class="cr-feature-badge">Isolated File</span>
                    <div class="cr-feature-title">File-Level Review</div>
                    <div class="cr-feature-desc">
                        Upload a source file and get an AI-powered code review with line-by-line defect detection, evidence extraction, and concrete fixes.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)
        if st.button("Review a File →", key="btn_home_file", type="primary", use_container_width=True):
            navigate_to(PAGE_FILE_REVIEW)

    with col2:
        st.markdown(
            """
            <div class="cr-feature-card">
                <div>
                    <span class="cr-feature-badge" style="color: #a855f7; background: rgba(168, 85, 247, 0.12); border-color: rgba(168, 85, 247, 0.3);">
                        Whole Project
                    </span>
                    <div class="cr-feature-title">Repository Review</div>
                    <div class="cr-feature-desc">
                        Analyze an entire GitHub repository for bugs, security issues, performance problems, and code quality across interconnected files.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)
        if st.button("Review Repository →", key="btn_home_repo", type="primary", use_container_width=True):
            navigate_to(PAGE_REPO_REVIEW)

    with col3:
        st.markdown(
            """
            <div class="cr-feature-card">
                <div>
                    <span class="cr-feature-badge" style="color: #38bdf8; background: rgba(56, 189, 248, 0.12); border-color: rgba(56, 189, 248, 0.3);">
                        Targeted Query
                    </span>
                    <div class="cr-feature-title">Semantic Search</div>
                    <div class="cr-feature-desc">
                        Describe an issue and find relevant code across your project. Conduct focused inquiries on specific targeted vulnerability patterns.
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown("<div style='margin-top: 0.75rem;'></div>", unsafe_allow_html=True)
        if st.button("Search for Issues →", key="btn_home_semantic", type="primary", use_container_width=True):
            navigate_to(PAGE_SEMANTIC_SEARCH)

    # -------------------------------------------------------------
    # Architecture Distinction & Technical Highlights
    # -------------------------------------------------------------
    st.markdown("<div style='margin-top: 2.5rem;'></div>", unsafe_allow_html=True)
    
    st.markdown(
        """
        <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 1.5rem 1.75rem;">
            <div style="font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent-light); margin-bottom: 0.5rem;">
                Engine Capabilities & Scope
            </div>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 1.5rem; margin-top: 1rem;">
                <div>
                    <div style="font-weight: 600; color: #ffffff; font-size: 0.95rem; margin-bottom: 0.3rem;">
                        1. File Review
                    </div>
                    <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
                        Deep inspection of individual modules. Identifies syntax errors, type safety gaps, and localized logic flaws without repo overhead.
                    </div>
                </div>
                <div>
                    <div style="font-weight: 600; color: #ffffff; font-size: 0.95rem; margin-bottom: 0.3rem;">
                        2. Repository Review
                    </div>
                    <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
                        Full pipeline: clones repo, resolves cross-file dependencies, creates vector embeddings, and reviews every file with project context.
                    </div>
                </div>
                <div>
                    <div style="font-weight: 600; color: #ffffff; font-size: 0.95rem; margin-bottom: 0.3rem;">
                        3. Semantic Search
                    </div>
                    <div style="font-size: 0.85rem; color: var(--text-secondary); line-height: 1.5;">
                        Targeted discovery: uses vector similarity search in ChromaDB to retrieve only code chunks matching your natural language query.
                    </div>
                </div>
            </div>
            <div style="margin-top: 1.5rem; padding-top: 1rem; border-top: 1px solid var(--border-subtle); display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.75rem;">
                <span style="font-size: 0.8rem; color: var(--text-muted); font-family: var(--font-mono);">
                    Supported Languages:
                </span>
                <div style="display: flex; gap: 0.5rem; flex-wrap: wrap;">
                    <span class="cr-badge cr-badge-category">Python</span>
                    <span class="cr-badge cr-badge-category">TypeScript</span>
                    <span class="cr-badge cr-badge-category">JavaScript</span>
                    <span class="cr-badge cr-badge-category">Java</span>
                    <span class="cr-badge cr-badge-category">Kotlin</span>
                    <span class="cr-badge cr-badge-category">C#</span>
                    <span class="cr-badge cr-badge-category">Go</span>
                    <span class="cr-badge cr-badge-category">Rust</span>
                    <span class="cr-badge cr-badge-category">C/C++</span>
                    <span class="cr-badge cr-badge-category">SQL</span>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

