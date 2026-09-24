"""
Global CSS and Design System for AI Code Review Agent.
Engineered for a high-end, minimal, dark developer-tool aesthetic.
"""

import streamlit as st

DESIGN_SYSTEM_CSS = """
<style>
/* -------------------------------------------------------------
   1. Typography & Global Resets
------------------------------------------------------------- */
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {
    --bg-primary: #0a0d14;
    --bg-secondary: #0f1420;
    --bg-surface: #141b29;
    --bg-surface-hover: #1b2438;
    --bg-surface-elevated: #1e293b;
    
    --border-subtle: #1e283d;
    --border-default: #26334d;
    --border-bright: #3b4d71;
    
    --accent-primary: #3b82f6;
    --accent-primary-hover: #2563eb;
    --accent-light: #60a5fa;
    --accent-glow: rgba(59, 130, 246, 0.15);
    
    --text-primary: #f1f5f9;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    
    /* Severities */
    --sev-critical-bg: rgba(239, 68, 68, 0.12);
    --sev-critical-border: #7f1d1d;
    --sev-critical-text: #f87171;
    --sev-critical-accent: #ef4444;
    
    --sev-high-bg: rgba(249, 115, 22, 0.12);
    --sev-high-border: #7c2d12;
    --sev-high-text: #fb923c;
    --sev-high-accent: #f97316;
    
    --sev-medium-bg: rgba(245, 158, 11, 0.12);
    --sev-medium-border: #78350f;
    --sev-medium-text: #fbbf24;
    --sev-medium-accent: #f59e0b;
    
    --sev-low-bg: rgba(56, 189, 248, 0.12);
    --sev-low-border: #0c4a6e;
    --sev-low-text: #38bdf8;
    --sev-low-accent: #0284c7;

    /* Categories */
    --cat-bug: #f43f5e;
    --cat-security: #a855f7;
    --cat-perf: #eab308;
    --cat-quality: #06b6d4;

    --font-sans: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-mono: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
}

html, body, [class*="css"] {
    font-family: var(--font-sans);
    color: var(--text-primary);
}

.stApp {
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

/* Hide default streamlit clutter */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header[data-testid="stHeader"] {
    background-color: rgba(10, 13, 20, 0.85);
    backdrop-filter: blur(12px);
    border-bottom: 1px solid var(--border-subtle);
}

/* -------------------------------------------------------------
   2. Sidebar Refinement
------------------------------------------------------------- */
section[data-testid="stSidebar"] {
    background-color: var(--bg-secondary);
    border-right: 1px solid var(--border-subtle);
    padding-top: 1rem;
}

section[data-testid="stSidebar"] div.stButton > button {
    width: 100%;
    text-align: left;
    display: flex;
    justify-content: flex-start;
    align-items: center;
    background: transparent;
    color: var(--text-secondary);
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 0.6rem 0.85rem;
    font-weight: 500;
    font-size: 0.92rem;
    transition: all 0.15s ease-in-out;
}

section[data-testid="stSidebar"] div.stButton > button:hover {
    background: var(--bg-surface);
    color: var(--text-primary);
    border-color: var(--border-subtle);
}

section[data-testid="stSidebar"] div.stButton > button:active,
section[data-testid="stSidebar"] div.stButton > button[kind="primary"] {
    background: var(--bg-surface-elevated);
    color: var(--accent-light);
    border-color: var(--accent-primary);
    box-shadow: 0 0 12px var(--accent-glow);
}

/* -------------------------------------------------------------
   3. Buttons & Form Controls
------------------------------------------------------------- */
div.stButton > button[kind="primary"] {
    background: linear-gradient(180deg, #3b82f6 0%, #2563eb 100%);
    color: #ffffff;
    border: 1px solid rgba(255, 255, 255, 0.15);
    font-weight: 600;
    border-radius: 8px;
    padding: 0.6rem 1.4rem;
    transition: all 0.2s ease;
    box-shadow: 0 2px 8px rgba(37, 99, 235, 0.35);
}

div.stButton > button[kind="primary"]:hover {
    background: linear-gradient(180deg, #60a5fa 0%, #3b82f6 100%);
    box-shadow: 0 4px 14px rgba(37, 99, 235, 0.5);
    transform: translateY(-1px);
}

div.stButton > button[kind="secondary"] {
    background: var(--bg-surface);
    color: var(--text-primary);
    border: 1px solid var(--border-default);
    font-weight: 500;
    border-radius: 8px;
    padding: 0.55rem 1.2rem;
    transition: all 0.15s ease;
}

div.stButton > button[kind="secondary"]:hover {
    background: var(--bg-surface-hover);
    border-color: var(--border-bright);
    color: #ffffff;
}

/* Inputs, Textareas, and Selects */
div[data-baseweb="input"] > div,
div[data-baseweb="textarea"] > div,
div[data-baseweb="select"] > div {
    background-color: var(--bg-surface) !important;
    border-color: var(--border-default) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

div[data-baseweb="input"] > div:focus-within,
div[data-baseweb="textarea"] > div:focus-within,
div[data-baseweb="select"] > div:focus-within {
    border-color: var(--accent-primary) !important;
    box-shadow: 0 0 0 1px var(--accent-primary) !important;
}

textarea {
    font-family: var(--font-sans) !important;
    font-size: 0.95rem !important;
}

/* -------------------------------------------------------------
   4. Custom Product Components & Cards
------------------------------------------------------------- */
.cr-card {
    background-color: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.5rem;
    transition: all 0.2s ease;
}

.cr-card:hover {
    border-color: var(--border-default);
    background-color: var(--bg-surface-hover);
}

.cr-feature-card {
    background: linear-gradient(180deg, var(--bg-surface) 0%, rgba(20, 27, 41, 0.7) 100%);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.6rem;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 100%;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s ease, border-color 0.2s ease, box-shadow 0.2s ease;
}

.cr-feature-card:hover {
    border-color: var(--border-bright);
    box-shadow: 0 8px 24px rgba(0, 0, 0, 0.45);
    transform: translateY(-2px);
}

.cr-feature-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent 0%, var(--accent-primary) 50%, transparent 100%);
    opacity: 0.4;
}

.cr-feature-badge {
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--accent-light);
    background: var(--accent-glow);
    border: 1px solid rgba(59, 130, 246, 0.3);
    padding: 0.25rem 0.6rem;
    border-radius: 9999px;
    display: inline-block;
    margin-bottom: 0.85rem;
}

.cr-feature-title {
    font-size: 1.22rem;
    font-weight: 700;
    color: #ffffff;
    margin-bottom: 0.5rem;
}

.cr-feature-desc {
    font-size: 0.9rem;
    line-height: 1.55;
    color: var(--text-secondary);
    margin-bottom: 1.25rem;
}

/* -------------------------------------------------------------
   5. Metrics Cards
------------------------------------------------------------- */
.cr-metrics-row {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(140px, 1fr));
    gap: 0.85rem;
    margin: 1.25rem 0;
}

.cr-metric-box {
    background-color: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1rem 1.1rem;
    display: flex;
    flex-direction: column;
}

.cr-metric-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.35rem;
}

.cr-metric-val {
    font-family: var(--font-mono);
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--text-primary);
    line-height: 1;
}

/* Severity-specific metric tinting */
.cr-metric-box.critical .cr-metric-val { color: var(--sev-critical-text); }
.cr-metric-box.high .cr-metric-val { color: var(--sev-high-text); }
.cr-metric-box.medium .cr-metric-val { color: var(--sev-medium-text); }
.cr-metric-box.low .cr-metric-val { color: var(--sev-low-text); }

/* -------------------------------------------------------------
   6. Badges (Severity & Category)
------------------------------------------------------------- */
.cr-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    padding: 0.2rem 0.55rem;
    border-radius: 6px;
    line-height: 1.2;
}

.cr-badge-critical {
    background: var(--sev-critical-bg);
    border: 1px solid var(--sev-critical-border);
    color: var(--sev-critical-text);
}

.cr-badge-high {
    background: var(--sev-high-bg);
    border: 1px solid var(--sev-high-border);
    color: var(--sev-high-text);
}

.cr-badge-medium {
    background: var(--sev-medium-bg);
    border: 1px solid var(--sev-medium-border);
    color: var(--sev-medium-text);
}

.cr-badge-low {
    background: var(--sev-low-bg);
    border: 1px solid var(--sev-low-border);
    color: var(--sev-low-text);
}

.cr-badge-category {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid var(--border-default);
    color: var(--text-secondary);
}

.cr-badge-cat-bug {
    color: var(--cat-bug);
    border-color: rgba(244, 63, 94, 0.3);
    background: rgba(244, 63, 94, 0.08);
}

.cr-badge-cat-security {
    color: var(--cat-security);
    border-color: rgba(168, 85, 247, 0.3);
    background: rgba(168, 85, 247, 0.08);
}

.cr-badge-cat-performance {
    color: var(--cat-perf);
    border-color: rgba(234, 179, 8, 0.3);
    background: rgba(234, 179, 8, 0.08);
}

.cr-badge-cat-quality {
    color: var(--cat-quality);
    border-color: rgba(6, 182, 212, 0.3);
    background: rgba(6, 182, 212, 0.08);
}

/* -------------------------------------------------------------
   7. Issue Card & Evidence Box
------------------------------------------------------------- */
.cr-issue-card {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 10px;
    padding: 1.25rem 1.4rem;
    margin-bottom: 1rem;
    border-left: 4px solid var(--border-bright);
    transition: border-color 0.15s ease;
}

.cr-issue-card.critical { border-left-color: var(--sev-critical-accent); }
.cr-issue-card.high { border-left-color: var(--sev-high-accent); }
.cr-issue-card.medium { border-left-color: var(--sev-medium-accent); }
.cr-issue-card.low { border-left-color: var(--sev-low-accent); }

.cr-issue-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.75rem;
    flex-wrap: wrap;
    gap: 0.5rem;
}

.cr-issue-file-line {
    font-family: var(--font-mono);
    font-size: 0.82rem;
    color: var(--text-secondary);
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
}

.cr-issue-file-line strong {
    color: var(--text-primary);
}

.cr-section-label {
    font-size: 0.75rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--text-muted);
    margin: 0.85rem 0 0.35rem 0;
}

.cr-evidence-box {
    font-family: var(--font-mono);
    font-size: 0.83rem;
    line-height: 1.5;
    background: #080b11;
    border: 1px solid #1a2233;
    border-radius: 8px;
    padding: 0.85rem 1rem;
    overflow-x: auto;
    color: #e2e8f0;
    margin: 0.4rem 0 0.75rem 0;
    white-space: pre-wrap;
    word-break: break-word;
}

.cr-recommendation-box {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(59, 130, 246, 0.2);
    border-left: 3px solid var(--accent-primary);
    border-radius: 6px;
    padding: 0.75rem 1rem;
    font-size: 0.88rem;
    line-height: 1.55;
    color: #cbd5e1;
    margin-top: 0.4rem;
}

/* -------------------------------------------------------------
   8. Progress Tracker Component
------------------------------------------------------------- */
.cr-progress-container {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.4rem;
    margin: 1.25rem 0;
}

.cr-progress-step {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    padding: 0.5rem 0;
    font-size: 0.9rem;
    color: var(--text-secondary);
}

.cr-progress-step.done {
    color: #10b981;
}

.cr-progress-step.active {
    color: #ffffff;
    font-weight: 600;
}

.cr-progress-step.pending {
    color: var(--text-muted);
    opacity: 0.6;
}

.cr-progress-icon {
    font-family: var(--font-mono);
    font-size: 1rem;
    width: 20px;
    text-align: center;
}

/* -------------------------------------------------------------
   9. Empty States & Alerts
------------------------------------------------------------- */
.cr-empty-state {
    background: var(--bg-surface);
    border: 1px dashed var(--border-default);
    border-radius: 12px;
    padding: 3rem 2rem;
    text-align: center;
    margin: 1.5rem 0;
}

.cr-empty-icon {
    font-size: 2.2rem;
    color: var(--text-muted);
    margin-bottom: 0.85rem;
}

.cr-empty-title {
    font-size: 1.15rem;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 0.4rem;
}

.cr-empty-subtitle {
    font-size: 0.9rem;
    color: var(--text-secondary);
    max-width: 480px;
    margin: 0 auto;
    line-height: 1.5;
}

/* Query Chips */
.cr-chip {
    background: var(--bg-surface);
    border: 1px solid var(--border-subtle);
    color: var(--text-secondary);
    padding: 0.35rem 0.75rem;
    border-radius: 9999px;
    font-size: 0.8rem;
    display: inline-block;
    margin: 0.25rem;
    cursor: pointer;
    transition: all 0.15s ease;
}

.cr-chip:hover {
    border-color: var(--accent-primary);
    color: #ffffff;
    background: var(--bg-surface-elevated);
}

/* Code Preview Box */
.cr-code-preview {
    font-family: var(--font-mono);
    font-size: 0.82rem;
    line-height: 1.5;
    background: #080b11;
    border: 1px solid var(--border-subtle);
    border-radius: 8px;
    padding: 1rem;
    max-height: 320px;
    overflow-y: auto;
    color: #cbd5e1;
}

/* Scrollbars */
::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: var(--bg-primary);
}
::-webkit-scrollbar-thumb {
    background: var(--border-default);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--border-bright);
}
</style>
"""

def inject_theme():
    """Injects the global design system stylesheet into the Streamlit application."""
    st.markdown(DESIGN_SYSTEM_CSS, unsafe_allow_html=True)

