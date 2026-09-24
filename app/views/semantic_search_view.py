"""
Semantic / Targeted Issue Search View.
"""

import streamlit as st
from pathlib import Path
from app.ui.components import (
    render_header,
    render_metric_cards,
    render_issue_card,
    render_empty_state,
    render_error_banner
)
from app.loaders.repository_scanner import RepositoryScanner
from app.loaders import code_loader
from app.processors.code_chunker import CodeChunker
from app.vector_stores.chroma_store import ChromaStore
from app.agents.code_reviewer import CodeReviewer
from app.agents.semantic_reviewer import SemanticReviewer
from app.agents.review_aggregator import ReviewAgentAggregator

EXAMPLE_QUERIES = [
    "Find SQL injection vulnerabilities",
    "Find hardcoded secrets",
    "Find authentication issues",
    "Find unsafe null handling",
    "Find potential crash risks",
    "Find inefficient database operations"
]

def load_default_demo_repo_if_needed():
    """Helper to initialize the sample repo into vector store for fast semantic search demo."""
    sample_repo_dir = Path("app/data/repositories/Wish_List-App")
    if not sample_repo_dir.exists():
        return False
        
    scanner = RepositoryScanner()
    files = scanner.scan(sample_repo_dir)
    loaded_files = [code_loader.load_code(str(f)) for f in files]
    
    chunker = CodeChunker()
    all_chunks = []
    for cf in loaded_files:
        doc = chunker.convert_to_document(cf)
        chunks = chunker.code_splitter(doc)
        all_chunks.extend(chunks)
        
    store = ChromaStore()
    store.add_documents(all_chunks)
    
    st.session_state.active_repo_name = "Wish_List-App"
    st.session_state.active_repo_path = str(sample_repo_dir)
    st.session_state.active_code_files = loaded_files
    st.session_state.active_chunks = all_chunks
    st.session_state.active_vector_store = store
    return True

def render_semantic_search_view():
    """Renders the semantic issue search page."""
    render_header(
        title="Semantic Issue Search",
        subtitle="Describe the issue you want to find in your code.",
        badge="Targeted Search"
    )

    # Targeted scope disclaimer banner
    st.markdown(
        """
        <div style="background: rgba(56, 189, 248, 0.06); border: 1px solid rgba(56, 189, 248, 0.2); border-radius: 8px; padding: 0.75rem 1rem; margin-bottom: 1.25rem; display: flex; align-items: center; gap: 0.6rem;">
            <span style="font-size: 1.1rem;">ℹ️</span>
            <span style="font-size: 0.88rem; color: #7dd3fc; line-height: 1.4;">
                <strong>Focused Investigation:</strong> This performs a targeted semantic search across your codebase using vector embeddings, rather than a full repository audit.
            </span>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Repository source indicator / check
    active_repo = st.session_state.get("active_repo_name")
    has_index = st.session_state.get("active_vector_store") is not None and st.session_state.get("active_code_files") is not None

    col_repo_stat, col_repo_action = st.columns([3, 1], gap="medium")
    with col_repo_stat:
        if has_index:
            files_count = len(st.session_state.active_code_files)
            chunks_count = len(st.session_state.active_chunks) if st.session_state.active_chunks else 0
            st.markdown(
                f"""
                <div style="font-family: var(--font-mono); font-size: 0.82rem; color: var(--text-secondary); margin-bottom: 0.5rem;">
                    Active Index: <strong style="color: #ffffff;">{active_repo or 'Project'}</strong> ({files_count} files, {chunks_count} chunks indexed)
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                """
                <div style="font-family: var(--font-mono); font-size: 0.82rem; color: #fbbf24; margin-bottom: 0.5rem;">
                    ⚠️ No repository currently indexed in session.
                </div>
                """,
                unsafe_allow_html=True
            )
            
    with col_repo_action:
        if not has_index:
            if st.button("Load Demo Index (Wish_List-App)", use_container_width=True, type="secondary"):
                with st.spinner("Indexing demo repository..."):
                    if load_default_demo_repo_if_needed():
                        st.success("Demo repository indexed!")
                        st.rerun()
                    else:
                        st.error("Demo repository not found locally.")

    # -------------------------------------------------------------
    # Query Textarea & Example Queries
    # -------------------------------------------------------------
    current_q = st.session_state.get("semantic_query", "")
    query_input = st.text_area(
        label="Search Query",
        value=current_q,
        placeholder="e.g. Find potential null-safety and crash risks",
        height=100,
        help="Enter a specific vulnerability, bug pattern, or architectural concern in plain English."
    )
    st.session_state.semantic_query = query_input

    # Clickable Example Queries
    st.markdown(
        """
        <div style="font-size: 0.78rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted); margin: 0.6rem 0 0.4rem 0;">
            Example Queries:
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Render example buttons in a clean wrap row
    cols = st.columns(3)
    for i, ex in enumerate(EXAMPLE_QUERIES):
        col = cols[i % 3]
        if col.button(f"• {ex}", key=f"ex_btn_{i}", use_container_width=True, type="secondary"):
            st.session_state.semantic_query = ex
            st.rerun()

    # Primary Search CTA
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    search_clicked = st.button(
        "Search Repository ⌕",
        type="primary",
        use_container_width=True,
        key="btn_execute_semantic_search"
    )

    # -------------------------------------------------------------
    # Execute Semantic Search
    # -------------------------------------------------------------
    if search_clicked:
        if not query_input or not query_input.strip():
            render_error_banner("Please enter an issue description or query to search.")
            return

        if not has_index:
            with st.spinner("Indexing local demo repository..."):
                success = load_default_demo_repo_if_needed()
                if not success:
                    render_error_banner("Please index a repository in Repository Review first or load the demo repository.")
                    return
                has_index = True

        with st.status(f"Conducting semantic search for '{query_input[:40]}...' ", expanded=True) as status:
            try:
                st.write("Retrieving semantically relevant code chunks from ChromaDB...")
                vector_store = st.session_state.active_vector_store
                code_files = st.session_state.active_code_files
                
                code_reviewer = CodeReviewer()
                semantic_reviewer = SemanticReviewer(
                    code_reviewer=code_reviewer,
                    vector_store=vector_store,
                    code_files=code_files
                )
                
                st.write("Analyzing matched code sections against requested criteria...")
                reviews = semantic_reviewer.review(query=query_input.strip(), k=5)
                
                aggregator = ReviewAgentAggregator()
                aggregated = aggregator.aggregate(reviews)
                
                # Also collect relevant file names
                relevant_files = []
                for cf, _ in semantic_reviewer.retrieve_relevant_files(query_input.strip(), k=5):
                    relevant_files.append(cf.file_name)
                    
                st.session_state.semantic_results = {
                    "query": query_input.strip(),
                    "relevant_files": relevant_files,
                    "aggregated": aggregated,
                    "raw_reviews": reviews
                }
                
                status.update(label="Semantic search complete!", state="complete", expanded=False)
                st.rerun()
            except Exception as e:
                status.update(label="Search failed", state="error", expanded=False)
                render_error_banner(f"Search failed: {str(e)}")
                return

    # -------------------------------------------------------------
    # Display Semantic Results or Empty State
    # -------------------------------------------------------------
    results_data = st.session_state.get("semantic_results")
    if not results_data:
        render_empty_state(
            title="Describe what you want to find",
            subtitle="Ask the codebase a question and our semantic engine will locate the most relevant code and perform a targeted review.",
            icon="⌕"
        )
        return

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    
    query_str = results_data["query"]
    rel_files = results_data["relevant_files"]
    aggregated = results_data["aggregated"]
    issues = aggregated.get("issues", [])

    # Search Summary Banner
    files_badge = ", ".join(rel_files) if rel_files else "None"
    st.markdown(
        f"""
        <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 1.25rem;">
            <div style="font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--accent-light); margin-bottom: 0.35rem;">
                Targeted Search Results
            </div>
            <div style="font-size: 1.1rem; font-weight: 600; color: #ffffff; margin-bottom: 0.6rem;">
                "{query_str}"
            </div>
            <div style="font-size: 0.84rem; color: var(--text-secondary); font-family: var(--font-mono);">
                Relevant Files Inspected: <span style="color: var(--text-primary);">{files_badge}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Metrics
    render_metric_cards(
        files_reviewed=len(rel_files),
        total_issues=len(issues),
        severity_counts=aggregated.get("severity_counts", {})
    )

    # Findings
    st.markdown(
        """
        <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin: 1.75rem 0 0.75rem 0;">
            Targeted Findings
        </div>
        """,
        unsafe_allow_html=True
    )

    if not issues:
        st.success(f"No defects found related to '{query_str}'. The inspected files look clean for this issue type.")
        return

    # Filter row
    fcol1, fcol2 = st.columns(2, gap="small")
    with fcol1:
        sev_filter = st.selectbox(
            "Filter by Severity",
            options=["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"],
            index=0,
            key="sem_filter_sev"
        )
    with fcol2:
        cat_filter = st.selectbox(
            "Filter by Category",
            options=["ALL", "BUG", "SECURITY", "PERFORMANCE", "QUALITY"],
            index=0,
            key="sem_filter_cat"
        )

    # Render filtered issue cards
    for idx, issue in enumerate(issues):
        if sev_filter != "ALL" and issue.severity.upper() != sev_filter:
            continue
        if cat_filter != "ALL" and issue.category.upper() != cat_filter:
            continue
        render_issue_card(issue, index=idx, default_expanded=(idx == 0))

