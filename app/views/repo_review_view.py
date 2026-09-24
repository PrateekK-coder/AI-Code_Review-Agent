"""
Repository Review View.
"""

import streamlit as st
import time
from pathlib import Path
from app.ui.components import (
    render_header,
    render_metric_cards,
    render_issue_card,
    render_progress_tracker,
    render_empty_state,
    render_error_banner
)
from app.loaders.github_loader import GitHubRepositoryLoader
from app.loaders.repository_scanner import RepositoryScanner
from app.loaders import code_loader
from app.processors.code_chunker import CodeChunker
from app.vector_stores.chroma_store import ChromaStore
from app.agents.code_reviewer import CodeReviewer
from app.agents.repository_reviewer import RepositoryReviewer
from app.agents.review_aggregator import ReviewAgentAggregator

DEMO_REPO_URL = "https://github.com/PrateekK-coder/Wish_List-App.git"

def render_repo_review_view():
    """Renders the repository review page and runs multi-file analysis."""
    render_header(
        title="Repository Review",
        subtitle="Analyze an entire GitHub repository for bugs, security, and architectural issues.",
        badge="Whole Project"
    )

    # -------------------------------------------------------------
    # GitHub URL Input Form
    # -------------------------------------------------------------
    col_input, col_action = st.columns([3, 1], gap="medium")
    
    with col_input:
        current_url = st.session_state.get("repo_url", DEMO_REPO_URL)
        repo_url = st.text_input(
            "GitHub Repository URL",
            value=current_url,
            placeholder="https://github.com/user/repository.git",
            help="Enter any public GitHub repository URL."
        )
        st.session_state.repo_url = repo_url

    with col_action:
        st.markdown("<div style='margin-top: 1.75rem;'></div>", unsafe_allow_html=True)
        start_clicked = st.button(
            "Start Repository Review ⚡",
            type="primary",
            use_container_width=True,
            key="btn_start_repo_review"
        )

    # Demo quick-fill chip
    st.markdown(
        f"""
        <div style="display: flex; align-items: center; gap: 0.5rem; margin-top: -0.5rem; margin-bottom: 1.25rem;">
            <span style="font-size: 0.78rem; color: var(--text-muted);">Quick fill:</span>
            <span class="cr-chip" onclick="navigator.clipboard.writeText('{DEMO_REPO_URL}')">
                📦 {DEMO_REPO_URL}
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # -------------------------------------------------------------
    # Execute Repository Review Pipeline
    # -------------------------------------------------------------
    if start_clicked:
        if not repo_url or not repo_url.strip():
            render_error_banner("Please enter a valid GitHub repository URL.")
            return
            
        progress_placeholder = st.empty()
        status_text_placeholder = st.empty()
        
        stages = [
            {"title": "Repository cloned"},
            {"title": "Source files discovered"},
            {"title": "Code loaded"},
            {"title": "Code indexed into vector store"},
            {"title": "Reviewing repository"},
            {"title": "Findings aggregated"}
        ]
        
        try:
            # Stage 0: Clone
            with progress_placeholder.container():
                render_progress_tracker(stages, 0, "Cloning from GitHub...")
            loader = GitHubRepositoryLoader()
            repo_path = loader.clone(repo_url.strip())
            repo_name = repo_path.name
            st.session_state.active_repo_path = str(repo_path)
            st.session_state.active_repo_name = repo_name
            
            # Stage 1: Scan
            with progress_placeholder.container():
                render_progress_tracker(stages, 1, "Scanning repository tree...")
            scanner = RepositoryScanner()
            scanned_files = scanner.scan(repo_path)
            if not scanned_files:
                progress_placeholder.empty()
                render_error_banner(f"No supported code files found in repository {repo_name}.")
                return
                
            # Stage 2: Load
            with progress_placeholder.container():
                render_progress_tracker(stages, 2, f"Loading {len(scanned_files)} files...")
            loaded_files = []
            for file_p in scanned_files:
                loaded_files.append(code_loader.load_code(str(file_p)))
            st.session_state.active_code_files = loaded_files
            
            # Stage 3: Chunk & Index
            with progress_placeholder.container():
                render_progress_tracker(stages, 3, "Chunking and creating embeddings...")
            chunker = CodeChunker()
            all_chunks = []
            for cf in loaded_files:
                doc = chunker.convert_to_document(cf)
                chunks = chunker.code_splitter(doc)
                all_chunks.extend(chunks)
            st.session_state.active_chunks = all_chunks
            
            store = ChromaStore()
            store.add_documents(all_chunks)
            st.session_state.active_vector_store = store
            
            # Stage 4: Review files
            code_reviewer = CodeReviewer()
            repo_reviewer = RepositoryReviewer(
                code_reviewer=code_reviewer,
                vector_store=store,
                code_files=loaded_files
            )
            
            def on_file_progress(cur, total, current_file):
                short_name = Path(current_file).name
                with progress_placeholder.container():
                    render_progress_tracker(stages, 4, f"Reviewing file {cur} of {total}: {short_name}",            current=cur,
                    total=total)
            
            reviews = repo_reviewer.review_repository(
                code_files=loaded_files,
                chunks=all_chunks,
                progress_callback=on_file_progress
            )
            
            # Stage 5: Aggregate
            with progress_placeholder.container():
                render_progress_tracker(stages, 5, "Deduplicating & ranking findings...")
            aggregator = ReviewAgentAggregator()
            final_report = aggregator.aggregate(reviews)
            
            st.session_state.repo_review_result = final_report
            
            # Finish
            with progress_placeholder.container():
                render_progress_tracker(stages, 6, "Analysis Complete")
            time.sleep(0.5)
            progress_placeholder.empty()
            st.rerun()

        except Exception as e:
            progress_placeholder.empty()
            err_msg = str(e)
            if "not a valid GitHub repository" in err_msg:
                render_error_banner("That doesn't appear to be a valid GitHub repository URL.")
            elif "Could not resolve host" in err_msg or "Failed to connect" in err_msg:
                render_error_banner("Network error while connecting to GitHub. Please verify your connection.")
            else:
                render_error_banner(f"We couldn't complete the repository review. Error: {err_msg}")
            return

    # -------------------------------------------------------------
    # Display Results Dashboard or Empty State
    # -------------------------------------------------------------
    report = st.session_state.get("repo_review_result")
    
    if not report:
        render_empty_state(
            title="Enter a GitHub repository to begin analysis",
            subtitle="The agent will clone the repository, index dependencies in ChromaDB, and perform a comprehensive review of all source files.",
            icon="◫"
        )
        return

    # Review Complete Banner
    repo_name = st.session_state.get("active_repo_name", "Repository")
    st.markdown(
        f"""
        <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 1.25rem 1.5rem; margin-bottom: 1.25rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
            <div>
                <div style="font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: #10b981; margin-bottom: 0.25rem;">
                    ✓ Repository Review Complete
                </div>
                <div style="font-size: 1.15rem; font-weight: 700; color: #ffffff; font-family: var(--font-mono);">
                    {repo_name}
                </div>
            </div>
            <div>
                <span class="cr-feature-badge" style="margin: 0;">
                    Indexed & Ready for Semantic Search
                </span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Metric Cards
    render_metric_cards(
        files_reviewed=report.get("files_reviewed", 0),
        total_issues=report.get("total_issues", 0),
        severity_counts=report.get("severity_counts", {})
    )

    # -------------------------------------------------------------
    # Findings & Interactive Filters
    # -------------------------------------------------------------
    st.markdown(
        """
        <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin: 1.75rem 0 0.75rem 0;">
            Repository Findings
        </div>
        """,
        unsafe_allow_html=True
    )

    issues = report.get("issues", [])
    if not issues:
        st.success("No issues found in this repository! Excellent code hygiene.")
        return

    # Extract all distinct files present in issues
    distinct_files = ["ALL"] + sorted(list({Path(i.file).name for i in issues if i.file}))

    # Filter controls
    fcol1, fcol2, fcol3 = st.columns([1, 1, 2], gap="small")
    with fcol1:
        sev_filter = st.selectbox(
            "Filter by Severity",
            options=["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"],
            index=0,
            key="repo_filter_sev"
        )
    with fcol2:
        cat_filter = st.selectbox(
            "Filter by Category",
            options=["ALL", "BUG", "SECURITY", "PERFORMANCE", "QUALITY"],
            index=0,
            key="repo_filter_cat"
        )
    with fcol3:
        file_filter = st.selectbox(
            "Filter by File",
            options=distinct_files,
            index=0,
            key="repo_filter_file"
        )

    # Apply filters
    filtered_issues = []
    for issue in issues:
        if sev_filter != "ALL" and issue.severity.upper() != sev_filter:
            continue
        if cat_filter != "ALL" and issue.category.upper() != cat_filter:
            continue
        if file_filter != "ALL" and Path(issue.file).name != file_filter:
            continue
        filtered_issues.append(issue)

    st.markdown(
        f"""
        <div style="font-size: 0.8rem; color: var(--text-muted); font-family: var(--font-mono); margin-bottom: 0.75rem;">
            Showing {len(filtered_issues)} of {len(issues)} repository findings
        </div>
        """,
        unsafe_allow_html=True
    )

    if not filtered_issues:
        st.info("No findings match the selected filters.")
        return

    # Render issue cards
    for idx, issue in enumerate(filtered_issues):
        render_issue_card(issue, index=idx, default_expanded=(idx == 0))

