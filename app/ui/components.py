"""
Reusable UI Components for AI Code Review Agent.
Engineered for clarity, consistency, and professional developer-tool UX.
"""

import streamlit as st
import html
from typing import Dict, List, Optional, Any
from app.models.review import Issue, CodeReview

def render_header(title: str, subtitle: str, badge: Optional[str] = None):
    """Renders a unified page title header with clean typography and optional status badge."""
    badge_html = f'<span class="cr-feature-badge" style="margin-left: 0.75rem; vertical-align: middle;">{html.escape(badge)}</span>' if badge else ""
    st.markdown(
        f"""
        <div style="margin-bottom: 1.6rem; padding-bottom: 1rem; border-bottom: 1px solid var(--border-subtle);">
            <div style="display: flex; align-items: center; justify-content: space-between;">
                <h1 style="font-size: 1.85rem; font-weight: 700; letter-spacing: -0.02em; margin: 0; color: #ffffff;">
                    {html.escape(title)} {badge_html}
                </h1>
            </div>
            <p style="font-size: 0.96rem; color: var(--text-secondary); margin: 0.4rem 0 0 0; line-height: 1.5;">
                {html.escape(subtitle)}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_severity_badge(severity: str) -> str:
    """Returns HTML for a standardized severity badge."""
    sev = severity.upper().strip()
    css_class = {
        "CRITICAL": "cr-badge-critical",
        "HIGH": "cr-badge-high",
        "MEDIUM": "cr-badge-medium",
        "LOW": "cr-badge-low"
    }.get(sev, "cr-badge-low")
    
    return f'<span class="cr-badge {css_class}">{html.escape(sev)}</span>'

def render_category_badge(category: str) -> str:
    """Returns HTML for a standardized category badge."""
    cat = category.upper().strip()
    css_class = {
        "BUG": "cr-badge-cat-bug",
        "SECURITY": "cr-badge-cat-security",
        "PERFORMANCE": "cr-badge-cat-performance",
        "QUALITY": "cr-badge-cat-quality"
    }.get(cat, "")
    
    return f'<span class="cr-badge cr-badge-category {css_class}">{html.escape(cat)}</span>'

def render_metric_cards(files_reviewed: int, total_issues: int, severity_counts: Dict[str, int]):
    """Renders a row of metric cards summarizing review findings."""
    crit = severity_counts.get("CRITICAL", 0)
    high = severity_counts.get("HIGH", 0)
    med = severity_counts.get("MEDIUM", 0)
    low = severity_counts.get("LOW", 0)
    
    st.markdown(
        f"""
        <div class="cr-metrics-row">
            <div class="cr-metric-box">
                <span class="cr-metric-label">Files Reviewed</span>
                <span class="cr-metric-val">{files_reviewed}</span>
            </div>
            <div class="cr-metric-box">
                <span class="cr-metric-label">Total Issues</span>
                <span class="cr-metric-val">{total_issues}</span>
            </div>
            <div class="cr-metric-box critical">
                <span class="cr-metric-label">Critical</span>
                <span class="cr-metric-val">{crit}</span>
            </div>
            <div class="cr-metric-box high">
                <span class="cr-metric-label">High</span>
                <span class="cr-metric-val">{high}</span>
            </div>
            <div class="cr-metric-box medium">
                <span class="cr-metric-label">Medium</span>
                <span class="cr-metric-val">{med}</span>
            </div>
            <div class="cr-metric-box low">
                <span class="cr-metric-label">Low</span>
                <span class="cr-metric-val">{low}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_issue_card(issue: Issue, index: int, default_expanded: bool = False):
    """
    Renders an expandable issue card with category, severity,
    monospace evidence, explanation, and recommendation.
    """
    sev = issue.severity.upper().strip()
    cat = issue.category.upper().strip()
    sev_class = sev.lower()
    
    line_display = f"Line {issue.line}" if issue.line else "General"
    file_display = issue.file if issue.file else "Current File"
    
    # Header summary line for expander
    expander_title = f"{sev} • [{cat}] {issue.description[:75]}{'...' if len(issue.description) > 75 else ''}"
    
    with st.expander(expander_title, expanded=default_expanded):
        # Top Meta Row
        st.markdown(
            f"""
            <div class="cr-issue-header">
                <div>
                    {render_category_badge(cat)}
                    {render_severity_badge(sev)}
                </div>
                <div class="cr-issue-file-line">
                    <span>File: <strong>{html.escape(file_display)}</strong></span>
                    <span>•</span>
                    <span>{html.escape(line_display)}</span>
                </div>
            </div>
            <div class="cr-section-label">Explanation</div>
            <div style="font-size: 0.92rem; line-height: 1.6; color: var(--text-primary); margin-bottom: 0.75rem;">
                {html.escape(issue.description)}
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Evidence section
        if issue.evidence and issue.evidence.strip():
            st.markdown('<div class="cr-section-label">Evidence</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="cr-evidence-box">{html.escape(issue.evidence.strip())}</div>',
                unsafe_allow_html=True
            )
            
        # Recommendation section
        if issue.recommendation and issue.recommendation.strip():
            st.markdown('<div class="cr-section-label">Recommendation</div>', unsafe_allow_html=True)
            st.markdown(
                f"""
                <div class="cr-recommendation-box">
                    {html.escape(issue.recommendation.strip())}
                </div>
                """,
                unsafe_allow_html=True
            )

def render_testing_recommendations(recommendations: List[str]):
    """Renders testing recommendations if present."""
    if not recommendations:
        return
        
    items_html = "".join(f"<li style='margin-bottom: 0.4rem;'>{html.escape(rec)}</li>" for rec in recommendations)
    st.markdown(
        f"""
        <div style="background: var(--bg-surface); border: 1px solid var(--border-subtle); border-radius: 10px; padding: 1.2rem; margin: 1rem 0;">
            <div style="font-size: 0.75rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--accent-light); margin-bottom: 0.6rem;">
                🧪 Testing Recommendations
            </div>
            <ul style="margin: 0; padding-left: 1.4rem; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6;">
                {items_html}
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_progress_tracker(stages: List[Dict[str, Any]], active_index: int, detail_message: Optional[str] = None,current=None,total=None):
    """
    Renders a live progress tracker with step indicators.
    Each item in stages is {"title": str}.
    """
    step_rows = []
    for idx, stage in enumerate(stages):
        if idx < active_index:
            icon = "✓"
            css = "done"
        elif idx == active_index:
            icon = "⟳"
            css = "active"
        else:
            icon = "○"
            css = "pending"
            
        title = stage["title"]
        if idx == active_index and detail_message:
            title = f"{title} <span style='color: var(--accent-light); font-family: var(--font-mono); font-size: 0.82rem; margin-left: 0.5rem;'>({html.escape(detail_message)})</span>"
            
        step_rows.append(
    f'<div class="cr-progress-step {css}">'
    f'<span class="cr-progress-icon">{icon}</span>'
    f'<span>{title}</span>'
    f'</div>'
)
        
    steps_html = "".join(step_rows)

    st.markdown(
        f"""
        <div class="cr-progress-container">
            <div style="font-size: 0.75rem; font-weight: 700; letter-spacing: 0.06em; text-transform: uppercase; color: var(--text-muted); margin-bottom: 0.8rem;">
                Repository Analysis Pipeline
            </div>
            {steps_html}
        </div>
        """,
        unsafe_allow_html=True
    )

    # Show real file-review progress when available
    if current is not None and total is not None and total > 0:

        progress = current / total

        st.progress(progress)

        st.markdown(
            f"""
            <div style="
                text-align: center;
                color: var(--text-secondary);
                font-family: var(--font-mono);
                font-size: 0.8rem;
                margin-top: -0.5rem;
            ">
                {current} / {total} files reviewed
            </div>
            """,
            unsafe_allow_html=True
        )

def render_empty_state(title: str, subtitle: str, icon: str = "⬡"):
    """Renders a high-end empty state placeholder."""
    st.markdown(
        f"""
        <div class="cr-empty-state">
            <div class="cr-empty-icon">{html.escape(icon)}</div>
            <div class="cr-empty-title">{html.escape(title)}</div>
            <div class="cr-empty-subtitle">{html.escape(subtitle)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

def render_error_banner(message: str):
    """Renders a user-friendly error banner without stack trace."""
    st.markdown(
        f"""
        <div style="background: rgba(239, 68, 68, 0.08); border: 1px solid var(--sev-critical-border); border-left: 4px solid var(--sev-critical-accent); border-radius: 8px; padding: 1rem 1.25rem; margin: 1rem 0;">
            <div style="font-size: 0.85rem; font-weight: 700; color: var(--sev-critical-text); margin-bottom: 0.25rem;">
                Analysis Error
            </div>
            <div style="font-size: 0.9rem; color: #fca5a5; line-height: 1.5;">
                {html.escape(message)}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

