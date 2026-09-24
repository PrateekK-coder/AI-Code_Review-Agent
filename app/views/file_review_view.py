"""
File-Level Code Review View.
"""

import streamlit as st
from pathlib import Path
from app.ui.components import (
    render_header,
    render_metric_cards,
    render_issue_card,
    render_severity_badge,
    render_testing_recommendations,
    render_empty_state,
    render_error_banner
)
from app.loaders.code_loader import EXTENSION_MAP
from app.models.code import CodeFile
from app.agents.code_reviewer import CodeReviewer

def get_file_language(filename: str) -> str:
    """Detects programming language from filename extension."""
    suffix = Path(filename).suffix.lower()
    return EXTENSION_MAP.get(suffix, "text")

def render_file_review_view():
    """Renders the file review page and handles single-file AI review."""
    render_header(
        title="File-Level Code Review",
        subtitle="Upload a source file and analyze it with AI.",
        badge="Single File"
    )

    # -------------------------------------------------------------
    # Upload & File Source Section
    # -------------------------------------------------------------
    col_upload, col_demo = st.columns([3, 1], gap="medium")
    
    with col_upload:
        st.markdown(
            """
            <div style="font-size: 0.8rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.5rem;">
                Upload Source File
            </div>
            """,
            unsafe_allow_html=True
        )
        uploaded_file = st.file_uploader(
            label="Upload your source file (Drag & drop or browse files)",
            type=["py", "js", "ts", "java", "kt", "cpp", "c", "cs", "go", "rs", "sql"],
            label_visibility="collapsed"
        )

    with col_demo:
        st.markdown(
            """
            <div style="font-size: 0.8rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.5rem;">
                Quick Demo
            </div>
            """,
            unsafe_allow_html=True
        )
        st.markdown(
            """
            <div style="font-size: 0.83rem; color: var(--text-secondary); margin-bottom: 0.5rem; line-height: 1.4;">
                Load pre-built vulnerability test file:
            </div>
            """,
            unsafe_allow_html=True
        )
        if st.button("Load Demo (bad_code.py)", use_container_width=True, type="secondary"):
            sample_path = Path("app/data/sample_code/bad_code.py")
            if sample_path.exists():
                content = sample_path.read_text(encoding="utf-8")
                st.session_state.uploaded_file_info = {
                    "name": "bad_code.py",
                    "size": len(content.encode("utf-8")),
                    "language": "python",
                    "content": content,
                    "path": str(sample_path)
                }
                st.session_state.file_review_result = None
                st.rerun()

    # Process uploaded file if provided via widget
    if uploaded_file is not None:
        try:
            content_bytes = uploaded_file.getvalue()
            content = content_bytes.decode("utf-8", errors="replace")
            st.session_state.uploaded_file_info = {
                "name": uploaded_file.name,
                "size": len(content_bytes),
                "language": get_file_language(uploaded_file.name),
                "content": content,
                "path": uploaded_file.name
            }
        except Exception as e:
            st.error(f"Error reading file: {e}")

    file_info = st.session_state.get("uploaded_file_info")

    if not file_info:
        render_empty_state(
            title="Upload a source file to begin",
            subtitle="Drag & drop any Python, Java, Kotlin, TypeScript, C#, Go, or C++ file above, or click 'Load Demo' to test immediately.",
            icon="📄"
        )
        return

    # -------------------------------------------------------------
    # Uploaded File Metadata Card
    # -------------------------------------------------------------
    st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
    size_kb = file_info["size"] / 1024.0
    line_count = len(file_info["content"].splitlines())

    col_meta, col_btn = st.columns([3, 1], gap="medium")
    with col_meta:
        st.markdown(
            f"""
            <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 10px; padding: 0.9rem 1.25rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <span style="font-size: 1.3rem;">📄</span>
                    <div>
                        <div style="font-weight: 700; font-size: 0.95rem; color: #ffffff; font-family: var(--font-mono);">
                            {file_info["name"]}
                        </div>
                        <div style="font-size: 0.8rem; color: var(--text-muted); font-family: var(--font-mono);">
                            {size_kb:.1f} KB • {line_count} lines
                        </div>
                    </div>
                </div>
                <div>
                    <span class="cr-badge cr-badge-category" style="font-size: 0.8rem; padding: 0.3rem 0.7rem;">
                        {file_info["language"].upper()}
                    </span>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_btn:
        review_clicked = st.button(
            "Review File ⚡",
            type="primary",
            use_container_width=True,
            key="btn_review_file"
        )

    # Collapsible Source Code Preview
    with st.expander("Inspect File Source Code", expanded=False):
        st.code(file_info["content"], language=file_info["language"])

    # -------------------------------------------------------------
    # Execute File Review
    # -------------------------------------------------------------
    if review_clicked:
        with st.status("Analyzing your code...", expanded=True) as status:
            st.write("Initializing AI Code Reviewer...")
            try:
                code_file = CodeFile(
                    file_name=file_info["name"],
                    file_path=file_info.get("path", file_info["name"]),
                    language=file_info["language"],
                    content=file_info["content"]
                )
                
                st.write("Inspecting syntax, security vulnerabilities, edge cases, and performance...")
                reviewer = CodeReviewer()
                review_result = reviewer.review(
                    code_file=code_file,
                    code=file_info["content"],
                    context="",
                    review_request="Perform a general code review."
                )
                
                st.session_state.file_review_result = review_result
                status.update(label="Analysis complete!", state="complete", expanded=False)
                st.rerun()
            except Exception as ex:
                status.update(label="Analysis failed", state="error", expanded=False)
                render_error_banner(f"Failed to complete review: {str(ex)}")
                return

    # -------------------------------------------------------------
    # Display Results Dashboard
    # -------------------------------------------------------------
    result = st.session_state.get("file_review_result")
    if not result:
        return

    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    
    # Severity counts calculation
    sev_counts = {"CRITICAL": 0, "HIGH": 0, "MEDIUM": 0, "LOW": 0}
    for issue in result.issues:
        sev_counts[issue.severity.upper()] = sev_counts.get(issue.severity.upper(), 0) + 1

    # Review Summary Banner
    overall_badge = render_severity_badge(result.overall_severity)
    st.markdown(
        f"""
        <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 12px; padding: 1.4rem 1.6rem; margin-bottom: 1.25rem;">
            <div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 0.6rem; flex-wrap: wrap; gap: 0.5rem;">
                <div style="font-size: 0.78rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: var(--text-muted);">
                    Review Summary
                </div>
                <div style="display: flex; align-items: center; gap: 0.5rem;">
                    <span style="font-size: 0.8rem; color: var(--text-muted);">Overall Risk:</span>
                    {overall_badge}
                </div>
            </div>
            <div style="font-size: 0.96rem; line-height: 1.6; color: var(--text-primary);">
                {result.summary}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    # Metric Cards
    render_metric_cards(
        files_reviewed=1,
        total_issues=len(result.issues),
        severity_counts=sev_counts
    )

    # Testing Recommendations
    if hasattr(result, "testing_recommendations") and result.testing_recommendations:
        render_testing_recommendations(result.testing_recommendations)

    # -------------------------------------------------------------
    # Findings & Interactive Filters
    # -------------------------------------------------------------
    st.markdown(
        """
        <div style="font-size: 1.05rem; font-weight: 700; color: #ffffff; margin: 1.75rem 0 0.75rem 0;">
            Findings & Issues
        </div>
        """,
        unsafe_allow_html=True
    )

    if not result.issues:
        st.success("No issues detected! Clean code.")
        return

    # Filter row
    fcol1, fcol2, fcol3 = st.columns([1, 1, 2], gap="small")
    with fcol1:
        sev_filter = st.selectbox(
            "Filter by Severity",
            options=["ALL", "CRITICAL", "HIGH", "MEDIUM", "LOW"],
            index=0,
            key="file_filter_sev"
        )
    with fcol2:
        cat_filter = st.selectbox(
            "Filter by Category",
            options=["ALL", "BUG", "SECURITY", "PERFORMANCE", "QUALITY"],
            index=0,
            key="file_filter_cat"
        )
    with fcol3:
        search_kw = st.text_input(
            "Search in findings",
            placeholder="Search description, recommendation, or evidence...",
            key="file_filter_search"
        )

    # Filter issues
    filtered_issues = []
    for issue in result.issues:
        if sev_filter != "ALL" and issue.severity.upper() != sev_filter:
            continue
        if cat_filter != "ALL" and issue.category.upper() != cat_filter:
            continue
        if search_kw:
            kw = search_kw.lower()
            text_corpus = f"{issue.description} {issue.evidence} {issue.recommendation} {issue.file}".lower()
            if kw not in text_corpus:
                continue
        filtered_issues.append(issue)

    st.markdown(
        f"""
        <div style="font-size: 0.8rem; color: var(--text-muted); font-family: var(--font-mono); margin-bottom: 0.75rem;">
            Showing {len(filtered_issues)} of {len(result.issues)} findings
        </div>
        """,
        unsafe_allow_html=True
    )

    # Render issue cards
    for idx, issue in enumerate(filtered_issues):
        render_issue_card(issue, index=idx, default_expanded=(idx == 0))

