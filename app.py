"""
AI Use Case Management Platform
A comprehensive Streamlit prototype for AI teams to manage, monitor, and optimize AI use cases.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import json
import random
import time
from typing import Dict, List, Any

# ─────────────────────────────────────────────
#  PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="AI Platform Hub",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────
#  GLOBAL STYLES
# ─────────────────────────────────────────────
def inject_css():
    dark = st.session_state.get("dark_mode", True)
    if dark:
        bg        = "#0D0F14"
        surface   = "#14171F"
        surface2  = "#1C2030"
        border    = "#2A2F42"
        text      = "#E8EAF0"
        text2     = "#8891A8"
        accent    = "#4F7EFF"
        accent2   = "#7C5CFC"
        green     = "#2ECC71"
        red       = "#E74C3C"
        orange    = "#F39C12"
        card_bg   = "#14171F"
    else:
        bg        = "#F4F6FB"
        surface   = "#FFFFFF"
        surface2  = "#EEF1F8"
        border    = "#D8DCE8"
        text      = "#111827"
        text2     = "#6B7280"
        accent    = "#3B6FEE"
        accent2   = "#6B46F0"
        green     = "#16A34A"
        red       = "#DC2626"
        orange    = "#D97706"
        card_bg   = "#FFFFFF"

    st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:ital,opsz,wght@0,9..40,300;0,9..40,400;0,9..40,500;0,9..40,600;0,9..40,700;1,9..40,400&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {{
        --bg: {bg};
        --surface: {surface};
        --surface2: {surface2};
        --border: {border};
        --text: {text};
        --text2: {text2};
        --accent: {accent};
        --accent2: {accent2};
        --green: {green};
        --red: {red};
        --orange: {orange};
        --card: {card_bg};
    }}

    * {{ font-family: 'DM Sans', sans-serif !important; }}
    code, pre, .stCode {{ font-family: 'JetBrains Mono', monospace !important; }}

    .stApp {{ background: var(--bg) !important; color: var(--text) !important; }}

    /* Sidebar */
    [data-testid="stSidebar"] {{
        background: var(--surface) !important;
        border-right: 1px solid var(--border) !important;
    }}
    [data-testid="stSidebar"] * {{ color: var(--text) !important; }}

    /* Main content */
    .main .block-container {{ padding: 1.5rem 2rem; max-width: 1400px; }}

    /* Metric cards */
    .metric-card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 12px;
        padding: 1.2rem 1.4rem;
        margin-bottom: 0.5rem;
        position: relative;
        overflow: hidden;
    }}
    .metric-card::before {{
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        background: linear-gradient(90deg, var(--accent), var(--accent2));
    }}
    .metric-label {{ color: var(--text2); font-size: 0.78rem; font-weight: 500; letter-spacing: 0.06em; text-transform: uppercase; margin-bottom: 0.4rem; }}
    .metric-value {{ color: var(--text); font-size: 1.9rem; font-weight: 700; line-height: 1; }}
    .metric-delta {{ font-size: 0.78rem; margin-top: 0.3rem; }}
    .delta-up {{ color: var(--green); }}
    .delta-down {{ color: var(--red); }}

    /* Use case cards */
    .uc-card {{
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 14px;
        padding: 1.3rem 1.5rem;
        margin-bottom: 0.8rem;
        transition: border-color 0.2s;
    }}
    .uc-card:hover {{ border-color: var(--accent); }}
    .uc-title {{ font-size: 1rem; font-weight: 600; color: var(--text); margin-bottom: 0.3rem; }}
    .uc-meta {{ font-size: 0.8rem; color: var(--text2); }}

    /* Status badges */
    .badge {{
        display: inline-block;
        padding: 0.18rem 0.65rem;
        border-radius: 20px;
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.03em;
    }}
    .badge-active {{ background: rgba(46,204,113,0.15); color: var(--green); }}
    .badge-inactive {{ background: rgba(231,76,60,0.15); color: var(--red); }}
    .badge-draft {{ background: rgba(243,156,18,0.15); color: var(--orange); }}
    .badge-pending {{ background: rgba(79,126,255,0.15); color: var(--accent); }}

    /* Section headers */
    .section-header {{
        font-size: 1.4rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    .section-sub {{
        color: var(--text2);
        font-size: 0.85rem;
        margin-bottom: 1.2rem;
    }}

    /* Notification items */
    .notif-item {{
        background: var(--surface2);
        border-left: 3px solid var(--accent);
        border-radius: 0 8px 8px 0;
        padding: 0.7rem 1rem;
        margin-bottom: 0.5rem;
        font-size: 0.85rem;
    }}
    .notif-warn {{ border-left-color: var(--orange); }}
    .notif-error {{ border-left-color: var(--red); }}
    .notif-success {{ border-left-color: var(--green); }}

    /* Timeline / activity log */
    .activity-item {{
        display: flex;
        gap: 1rem;
        padding: 0.6rem 0;
        border-bottom: 1px solid var(--border);
        font-size: 0.84rem;
    }}
    .activity-time {{ color: var(--text2); min-width: 120px; }}
    .activity-text {{ color: var(--text); }}

    /* Override Streamlit default metric */
    [data-testid="stMetric"] {{
        background: var(--card) !important;
        border: 1px solid var(--border) !important;
        border-radius: 12px !important;
        padding: 1rem 1.2rem !important;
    }}
    [data-testid="stMetricLabel"] {{ color: var(--text2) !important; font-size: 0.8rem !important; }}
    [data-testid="stMetricValue"] {{ color: var(--text) !important; font-weight: 700 !important; }}

    /* Plotly charts transparent bg */
    .js-plotly-plot .plotly .modebar {{ background: transparent !important; }}

    /* Buttons */
    .stButton > button {{
        border-radius: 8px !important;
        font-weight: 600 !important;
        font-size: 0.84rem !important;
        transition: all 0.15s !important;
        border: 1px solid var(--border) !important;
        background: var(--surface2) !important;
        color: var(--text) !important;
    }}
    .stButton > button:hover {{
        border-color: var(--accent) !important;
        color: var(--accent) !important;
    }}

    /* Primary button (wrapped in div.primary-btn) */
    .primary-btn .stButton > button {{
        background: var(--accent) !important;
        color: white !important;
        border-color: var(--accent) !important;
    }}

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: var(--surface2) !important;
        border-radius: 10px !important;
        padding: 4px !important;
        gap: 2px !important;
        border: none !important;
    }}
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px !important;
        font-weight: 500 !important;
        font-size: 0.84rem !important;
        color: var(--text2) !important;
        padding: 0.45rem 1rem !important;
    }}
    .stTabs [aria-selected="true"] {{
        background: var(--surface) !important;
        color: var(--text) !important;
        box-shadow: 0 1px 4px rgba(0,0,0,0.2) !important;
    }}
    .stTabs [data-baseweb="tab-panel"] {{ padding-top: 1.2rem !important; }}

    /* Select boxes, inputs */
    .stSelectbox > div > div,
    .stMultiSelect > div > div,
    .stTextInput > div > div,
    .stNumberInput > div > div,
    .stTextArea > div > div {{
        background: var(--surface2) !important;
        border-color: var(--border) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
    }}

    /* Slider */
    .stSlider [data-testid="stSlider"] {{ color: var(--accent) !important; }}

    /* Expander */
    .streamlit-expanderHeader {{
        background: var(--surface2) !important;
        border-radius: 8px !important;
        color: var(--text) !important;
        font-weight: 600 !important;
    }}

    /* DataFrames */
    .stDataFrame {{ border-radius: 10px !important; overflow: hidden !important; }}
    [data-testid="stDataFrame"] th {{
        background: var(--surface2) !important;
        color: var(--text2) !important;
        font-size: 0.78rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }}

    /* Horizontal rule */
    hr {{ border-color: var(--border) !important; }}

    /* Info/warning/error boxes */
    .stAlert {{ border-radius: 10px !important; border: none !important; }}

    /* Progress bar */
    .stProgress > div > div {{
        background: linear-gradient(90deg, var(--accent), var(--accent2)) !important;
        border-radius: 4px !important;
    }}

    /* Login card */
    .login-wrap {{
        max-width: 420px;
        margin: 6rem auto;
        background: var(--card);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 2.5rem 2.8rem;
    }}
    .login-logo {{
        text-align: center;
        font-size: 2.4rem;
        margin-bottom: 0.5rem;
    }}
    .login-title {{
        text-align: center;
        font-size: 1.35rem;
        font-weight: 700;
        color: var(--text);
        margin-bottom: 0.3rem;
    }}
    .login-sub {{
        text-align: center;
        font-size: 0.84rem;
        color: var(--text2);
        margin-bottom: 1.8rem;
    }}

    /* Divider with text */
    .divider-text {{
        text-align: center;
        color: var(--text2);
        font-size: 0.78rem;
        margin: 0.8rem 0;
        position: relative;
    }}

    /* Preset tag pills */
    .preset-tag {{
        display: inline-block;
        background: var(--surface2);
        border: 1px solid var(--border);
        border-radius: 20px;
        padding: 0.2rem 0.8rem;
        font-size: 0.78rem;
        margin-right: 0.3rem;
        cursor: pointer;
        color: var(--text2);
    }}
    .preset-tag.selected {{
        background: rgba(79,126,255,0.15);
        border-color: var(--accent);
        color: var(--accent);
    }}

    /* Scrollbar */
    ::-webkit-scrollbar {{ width: 6px; height: 6px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}
    ::-webkit-scrollbar-thumb {{ background: var(--border); border-radius: 3px; }}

    /* Hide Streamlit branding */
    #MainMenu, footer, header {{ visibility: hidden; }}

    /* Sidebar nav items */
    .nav-item {{
        padding: 0.55rem 0.8rem;
        border-radius: 8px;
        margin-bottom: 2px;
        cursor: pointer;
        font-size: 0.88rem;
        font-weight: 500;
        color: var(--text2);
        display: flex;
        align-items: center;
        gap: 0.6rem;
        transition: all 0.15s;
    }}
    .nav-item:hover, .nav-item.active {{
        background: rgba(79,126,255,0.12);
        color: var(--accent);
    }}

    /* Heatmap label */
    .heatmap-label {{ font-size: 0.72rem; color: var(--text2); }}
    </style>
    """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MOCK DATA GENERATION
# ─────────────────────────────────────────────
def generate_mock_data():
    """Generate comprehensive mock data for the platform."""
    random.seed(42)
    np.random.seed(42)

    users = {
        "sarah.chen@company.com":    {"name": "Sarah Chen",    "role": "Use Case Owner", "unit": "Marketing",   "password": "demo"},
        "james.wright@company.com":  {"name": "James Wright",  "role": "Use Case Owner", "unit": "Operations",  "password": "demo"},
        "priya.patel@company.com":   {"name": "Priya Patel",   "role": "Use Case Owner", "unit": "Finance",     "password": "demo"},
        "alex.torres@company.com":   {"name": "Alex Torres",   "role": "AI Team Member", "unit": "AI Team",     "password": "demo"},
        "morgan.lee@company.com":    {"name": "Morgan Lee",    "role": "AI Team Member", "unit": "AI Team",     "password": "demo"},
        "admin@company.com":         {"name": "Admin User",    "role": "Admin",          "unit": "Platform",    "password": "admin"},
    }

    models = [
        {"id": "gpt-4o",         "name": "GPT-4o",            "provider": "OpenAI",      "context": "128K", "cost_per_1k": 0.005, "status": "active",      "strengths": ["Reasoning","Vision","Code"]},
        {"id": "gpt-4o-mini",    "name": "GPT-4o Mini",       "provider": "OpenAI",      "context": "128K", "cost_per_1k": 0.0003,"status": "active",      "strengths": ["Speed","Cost","General"]},
        {"id": "claude-3-5",     "name": "Claude 3.5 Sonnet", "provider": "Anthropic",   "context": "200K", "cost_per_1k": 0.003, "status": "active",      "strengths": ["Writing","Analysis","Safety"]},
        {"id": "claude-3-haiku", "name": "Claude 3 Haiku",    "provider": "Anthropic",   "context": "200K", "cost_per_1k": 0.0003,"status": "active",      "strengths": ["Speed","Cost","Summarization"]},
        {"id": "gemini-1-5-pro", "name": "Gemini 1.5 Pro",    "provider": "Google",      "context": "1M",   "cost_per_1k": 0.0035,"status": "active",      "strengths": ["Long Context","Multimodal","Code"]},
        {"id": "llama-3-70b",    "name": "Llama 3 70B",       "provider": "Meta/Self",   "context": "8K",   "cost_per_1k": 0.0009,"status": "active",      "strengths": ["Open Source","Privacy","Cost"]},
        {"id": "gpt-3-5-turbo",  "name": "GPT-3.5 Turbo",     "provider": "OpenAI",      "context": "16K",  "cost_per_1k": 0.0005,"status": "deprecated",  "strengths": ["Speed","Legacy"]},
        {"id": "mistral-large",  "name": "Mistral Large",     "provider": "Mistral AI",  "context": "32K",  "cost_per_1k": 0.004, "status": "active",      "strengths": ["European Data","Reasoning","Code"]},
    ]

    now = datetime.now()

    use_cases = [
        # Sarah Chen – Marketing
        {
            "id": "uc-001", "name": "Campaign Copy Generator",
            "description": "Generates marketing copy variants for A/B testing across email, social, and display channels.",
            "owner": "sarah.chen@company.com", "business_unit": "Marketing",
            "type": "Content Generation", "status": "active",
            "model": "claude-3-5", "created": now - timedelta(days=120),
            "last_accessed": now - timedelta(hours=2),
            "usage_count": 3847, "monthly_cost": 284.50, "avg_response_ms": 1230,
            "success_rate": 98.2, "users": ["marketing-team", "agency-partners"],
            "tags": ["marketing", "copywriting", "a/b-testing"],
            "params": {"temperature": 0.8, "max_tokens": 1024, "top_p": 0.95, "frequency_penalty": 0.3, "presence_penalty": 0.1, "response_format": "Markdown", "seed": None},
        },
        {
            "id": "uc-002", "name": "Customer Sentiment Analyzer",
            "description": "Analyzes customer feedback from surveys, reviews, and support tickets for sentiment and themes.",
            "owner": "sarah.chen@company.com", "business_unit": "Marketing",
            "type": "Text Analysis", "status": "active",
            "model": "gpt-4o-mini", "created": now - timedelta(days=85),
            "last_accessed": now - timedelta(hours=5),
            "usage_count": 12540, "monthly_cost": 178.20, "avg_response_ms": 680,
            "success_rate": 99.1, "users": ["cx-team", "marketing-team", "product-team"],
            "tags": ["sentiment", "analytics", "customer-feedback"],
            "params": {"temperature": 0.2, "max_tokens": 512, "top_p": 0.9, "frequency_penalty": 0.0, "presence_penalty": 0.0, "response_format": "JSON", "seed": 42},
        },
        {
            "id": "uc-003", "name": "SEO Brief Writer",
            "description": "Creates detailed SEO content briefs with keyword clustering, structure, and competitor analysis.",
            "owner": "sarah.chen@company.com", "business_unit": "Marketing",
            "type": "Content Generation", "status": "draft",
            "model": "gpt-4o", "created": now - timedelta(days=12),
            "last_accessed": now - timedelta(days=3),
            "usage_count": 45, "monthly_cost": 12.80, "avg_response_ms": 2450,
            "success_rate": 95.5, "users": ["seo-team"],
            "tags": ["seo", "content", "draft"],
            "params": {"temperature": 0.6, "max_tokens": 2048, "top_p": 1.0, "frequency_penalty": 0.2, "presence_penalty": 0.2, "response_format": "Markdown", "seed": None},
        },
        # James Wright – Operations
        {
            "id": "uc-004", "name": "Incident Report Summarizer",
            "description": "Condenses verbose incident reports into executive summaries with action items and risk scores.",
            "owner": "james.wright@company.com", "business_unit": "Operations",
            "type": "Summarization", "status": "active",
            "model": "claude-3-haiku", "created": now - timedelta(days=200),
            "last_accessed": now - timedelta(minutes=45),
            "usage_count": 8920, "monthly_cost": 95.40, "avg_response_ms": 540,
            "success_rate": 99.6, "users": ["ops-team", "executives", "risk-team"],
            "tags": ["operations", "reporting", "risk"],
            "params": {"temperature": 0.1, "max_tokens": 800, "top_p": 0.85, "frequency_penalty": 0.0, "presence_penalty": 0.0, "response_format": "Markdown", "seed": 100},
        },
        {
            "id": "uc-005", "name": "Supplier Contract Reviewer",
            "description": "Reviews supplier contracts to flag non-standard clauses, risk terms, and compliance issues.",
            "owner": "james.wright@company.com", "business_unit": "Operations",
            "type": "Document Review", "status": "active",
            "model": "gemini-1-5-pro", "created": now - timedelta(days=60),
            "last_accessed": now - timedelta(hours=1),
            "usage_count": 1230, "monthly_cost": 310.60, "avg_response_ms": 3200,
            "success_rate": 97.8, "users": ["legal-team", "procurement-team"],
            "tags": ["legal", "contracts", "compliance"],
            "params": {"temperature": 0.1, "max_tokens": 4096, "top_p": 0.9, "frequency_penalty": 0.0, "presence_penalty": 0.0, "response_format": "JSON", "seed": 7},
        },
        {
            "id": "uc-006", "name": "Logistics Route Optimizer",
            "description": "Interprets multi-modal logistics constraints and suggests optimized delivery routes.",
            "owner": "james.wright@company.com", "business_unit": "Operations",
            "type": "Data Analysis", "status": "inactive",
            "model": "gpt-4o", "created": now - timedelta(days=180),
            "last_accessed": now - timedelta(days=30),
            "usage_count": 2100, "monthly_cost": 0.0, "avg_response_ms": 4100,
            "success_rate": 91.2, "users": ["logistics-team"],
            "tags": ["logistics", "optimization", "paused"],
            "params": {"temperature": 0.3, "max_tokens": 1500, "top_p": 0.95, "frequency_penalty": 0.0, "presence_penalty": 0.0, "response_format": "JSON", "seed": None},
        },
        # Priya Patel – Finance
        {
            "id": "uc-007", "name": "Financial Report Narrator",
            "description": "Transforms raw financial tables into natural language narratives for board presentations.",
            "owner": "priya.patel@company.com", "business_unit": "Finance",
            "type": "Report Generation", "status": "active",
            "model": "claude-3-5", "created": now - timedelta(days=95),
            "last_accessed": now - timedelta(hours=3),
            "usage_count": 678, "monthly_cost": 140.30, "avg_response_ms": 1890,
            "success_rate": 98.8, "users": ["finance-team", "executives"],
            "tags": ["finance", "reporting", "board"],
            "params": {"temperature": 0.4, "max_tokens": 2000, "top_p": 0.92, "frequency_penalty": 0.1, "presence_penalty": 0.1, "response_format": "Markdown", "seed": 55},
        },
        {
            "id": "uc-008", "name": "Expense Anomaly Detector",
            "description": "Flags unusual expense patterns, duplicate submissions, and policy violations automatically.",
            "owner": "priya.patel@company.com", "business_unit": "Finance",
            "type": "Anomaly Detection", "status": "active",
            "model": "gpt-4o-mini", "created": now - timedelta(days=45),
            "last_accessed": now - timedelta(hours=0),
            "usage_count": 24500, "monthly_cost": 220.50, "avg_response_ms": 490,
            "success_rate": 99.3, "users": ["finance-team", "hr-team", "audit-team"],
            "tags": ["finance", "compliance", "automation"],
            "params": {"temperature": 0.0, "max_tokens": 256, "top_p": 1.0, "frequency_penalty": 0.0, "presence_penalty": 0.0, "response_format": "JSON", "seed": 99},
        },
        {
            "id": "uc-009", "name": "Earnings Call Q&A Prep",
            "description": "Generates anticipated analyst questions and draft responses based on financial data.",
            "owner": "priya.patel@company.com", "business_unit": "Finance",
            "type": "Content Generation", "status": "draft",
            "model": "gpt-4o", "created": now - timedelta(days=8),
            "last_accessed": now - timedelta(days=2),
            "usage_count": 22, "monthly_cost": 8.90, "avg_response_ms": 3100,
            "success_rate": 94.0, "users": ["executives", "ir-team"],
            "tags": ["finance", "investor-relations", "draft"],
            "params": {"temperature": 0.7, "max_tokens": 3000, "top_p": 0.95, "frequency_penalty": 0.2, "presence_penalty": 0.2, "response_format": "Text", "seed": None},
        },
    ]

    # Generate 90-day usage time series
    days = 90
    dates = [now - timedelta(days=i) for i in range(days, 0, -1)]
    usage_series = {}
    cost_series  = {}
    for uc in use_cases:
        base = uc["usage_count"] / 90
        noise = np.random.normal(0, base * 0.3, days)
        trend = np.linspace(-base * 0.2, base * 0.2, days)
        vals  = np.clip(base + noise + trend, 0, None).astype(int)
        usage_series[uc["id"]] = vals.tolist()
        cost_series[uc["id"]]  = (vals * (uc["monthly_cost"] / max(uc["usage_count"], 1))).tolist()

    # Access requests
    access_requests = [
        {"id": "ar-001", "uc_id": "uc-001", "requester": "tom.brooks@company.com",    "role": "Content Writer",  "status": "pending",  "requested": now - timedelta(days=2), "reason": "Need to generate campaign variants for Q4 launch."},
        {"id": "ar-002", "uc_id": "uc-004", "requester": "lisa.nguyen@company.com",   "role": "Risk Analyst",    "status": "pending",  "requested": now - timedelta(days=1), "reason": "Want to use for daily incident digests."},
        {"id": "ar-003", "uc_id": "uc-007", "requester": "david.kim@company.com",     "role": "Analyst",         "status": "approved", "requested": now - timedelta(days=10),"reason": "Monthly reporting automation."},
        {"id": "ar-004", "uc_id": "uc-002", "requester": "anna.schmidt@company.com",  "role": "CX Manager",      "status": "rejected", "requested": now - timedelta(days=5), "reason": "Aggregate brand sentiment monitoring."},
        {"id": "ar-005", "uc_id": "uc-005", "requester": "raj.iyer@company.com",      "role": "Procurement Lead","status": "pending",  "requested": now - timedelta(hours=3),"reason": "Reviewing vendor agreements before renewal."},
    ]

    # Audit trail
    audit = []
    actions = [
        ("Model changed", "gpt-4o-mini", "uc-002"), ("Params updated", "temperature: 0.2", "uc-002"),
        ("Use case created", "SEO Brief Writer", "uc-003"), ("Access granted", "cx-team", "uc-002"),
        ("Status changed", "active → inactive", "uc-006"), ("Owner reassigned", "james.wright", "uc-006"),
        ("Model changed", "claude-3-5", "uc-001"), ("Params updated", "max_tokens: 1024", "uc-001"),
        ("Access revoked", "old-agency", "uc-001"), ("Use case cloned", "→ SEO Brief Writer", "uc-003"),
    ]
    actors = list(users.keys())
    for i, (action, detail, uc_id) in enumerate(actions):
        audit.append({
            "id": f"audit-{i+1:03d}",
            "timestamp": now - timedelta(hours=i*4 + random.randint(0,3)),
            "actor": random.choice(actors),
            "action": action,
            "detail": detail,
            "uc_id": uc_id,
        })

    # Notifications
    notifications = [
        {"id": "n-1", "type": "warn",    "title": "Budget Threshold",      "msg": "uc-005 (Supplier Contract Reviewer) is at 87% of monthly budget.", "time": now - timedelta(hours=1), "read": False},
        {"id": "n-2", "type": "error",   "title": "Model Deprecation",     "msg": "GPT-3.5 Turbo will be deprecated on April 1. Migrate affected use cases.", "time": now - timedelta(hours=4), "read": False},
        {"id": "n-3", "type": "info",    "title": "New Access Requests",   "msg": "3 new access requests are awaiting your approval.", "time": now - timedelta(hours=6), "read": False},
        {"id": "n-4", "type": "success", "title": "Model Update Available","msg": "Claude 3.5 Sonnet has a new version. Review release notes.", "time": now - timedelta(days=1), "read": True},
        {"id": "n-5", "type": "warn",    "title": "Unusual Usage Spike",   "msg": "uc-008 (Expense Anomaly) showed 3× normal usage yesterday.", "time": now - timedelta(days=1), "read": True},
    ]

    # Feedback
    feedback = []
    sentiments = ["positive", "positive", "positive", "neutral", "negative"]
    comments = [
        "Really helpful, saved me hours on campaign drafts!",
        "Output quality is consistently high.",
        "Occasionally generates off-brand tone — would love a style guide integration.",
        "Works well for most cases but sometimes too verbose.",
        "Response format needs improvement for our CMS integration.",
        "Excellent accuracy on sentiment classification.",
        "Fast and reliable — exactly what we needed.",
        "The JSON output has inconsistent key naming sometimes.",
    ]
    for i in range(20):
        uc = random.choice(use_cases)
        feedback.append({
            "id": f"fb-{i+1:03d}",
            "uc_id": uc["id"],
            "uc_name": uc["name"],
            "rating": random.choice([3, 4, 4, 4, 5, 5, 5]),
            "sentiment": random.choice(sentiments),
            "comment": random.choice(comments),
            "user": random.choice(list(users.keys())),
            "time": now - timedelta(days=random.randint(0, 30)),
        })

    return {
        "users": users, "models": models, "use_cases": use_cases,
        "usage_series": usage_series, "cost_series": cost_series,
        "dates": dates, "access_requests": access_requests,
        "audit": audit, "notifications": notifications, "feedback": feedback,
    }

# ─────────────────────────────────────────────
#  SESSION STATE INIT
# ─────────────────────────────────────────────
def init_session():
    if "data" not in st.session_state:
        st.session_state.data = generate_mock_data()
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "dark_mode" not in st.session_state:
        st.session_state.dark_mode = True
    if "active_page" not in st.session_state:
        st.session_state.active_page = "Dashboard"
    if "selected_uc" not in st.session_state:
        st.session_state.selected_uc = None
    if "show_create_uc" not in st.session_state:
        st.session_state.show_create_uc = False
    if "ab_test" not in st.session_state:
        st.session_state.ab_test = {}

# ─────────────────────────────────────────────
#  CHART HELPERS
# ─────────────────────────────────────────────
def chart_theme():
    dark = st.session_state.get("dark_mode", True)
    return {
        "paper_bg": "rgba(0,0,0,0)",
        "plot_bg":  "rgba(0,0,0,0)",
        "font_color": "#8891A8" if dark else "#6B7280",
        "grid_color": "#2A2F42" if dark else "#E5E7EB",
        "line_color": "#2A2F42" if dark else "#E5E7EB",
    }

def style_fig(fig, height=300):
    t = chart_theme()
    fig.update_layout(
        paper_bgcolor=t["paper_bg"], plot_bgcolor=t["plot_bg"],
        font=dict(color=t["font_color"], family="DM Sans", size=11),
        height=height, margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
        xaxis=dict(gridcolor=t["grid_color"], linecolor=t["line_color"], showgrid=True),
        yaxis=dict(gridcolor=t["grid_color"], linecolor=t["line_color"], showgrid=True),
    )
    return fig

# ─────────────────────────────────────────────
#  LOGIN PAGE
# ─────────────────────────────────────────────
def render_login():
    dark = st.session_state.get("dark_mode", True)
    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        st.markdown("""
        <div class="login-logo">⬡</div>
        <div class="login-title">AI Platform Hub</div>
        <div class="login-sub">Enterprise AI Use Case Management</div>
        """, unsafe_allow_html=True)

        with st.form("login_form"):
            email = st.selectbox(
                "Account",
                options=list(st.session_state.data["users"].keys()),
                format_func=lambda x: f"{st.session_state.data['users'][x]['name']} — {st.session_state.data['users'][x]['role']}",
            )
            pwd = st.text_input("Password", type="password", placeholder="Enter password (demo / admin)")
            submitted = st.form_submit_button("Sign In →", use_container_width=True)

            if submitted:
                user_data = st.session_state.data["users"].get(email, {})
                if pwd == user_data.get("password", ""):
                    st.session_state.logged_in = True
                    st.session_state.current_user = email
                    st.session_state.active_page = "Dashboard"
                    st.rerun()
                else:
                    st.error("Incorrect password. Try: demo (owners/AI team) or admin (admin)")

        st.caption("💡 Quick access: select any account and use the listed password")

        # Theme toggle on login
        if st.button("🌙 Dark" if not dark else "☀️ Light", key="login_theme"):
            st.session_state.dark_mode = not dark
            st.rerun()

# ─────────────────────────────────────────────
#  SIDEBAR
# ─────────────────────────────────────────────
def render_sidebar():
    data  = st.session_state.data
    email = st.session_state.current_user
    user  = data["users"][email]
    role  = user["role"]

    with st.sidebar:
        # Logo & user info
        st.markdown(f"""
        <div style="display:flex;align-items:center;gap:0.8rem;padding:0.5rem 0 1.2rem 0;border-bottom:1px solid var(--border);margin-bottom:1rem;">
            <div style="width:36px;height:36px;border-radius:10px;background:linear-gradient(135deg,var(--accent),var(--accent2));display:flex;align-items:center;justify-content:center;font-weight:700;color:white;font-size:0.9rem;">
                {user['name'][0]}
            </div>
            <div>
                <div style="font-weight:600;font-size:0.88rem;color:var(--text);">{user['name']}</div>
                <div style="font-size:0.75rem;color:var(--text2);">{role} · {user['unit']}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Unread notifications badge
        unread = sum(1 for n in data["notifications"] if not n["read"])

        # Navigation sections
        def nav_btn(icon, label, page, badge=None):
            active = st.session_state.active_page == page
            badge_html = f' <span style="background:var(--red);color:white;border-radius:10px;padding:0 5px;font-size:0.65rem;font-weight:700;">{badge}</span>' if badge else ""
            st.markdown(f"""
            <div class="nav-item {'active' if active else ''}" onclick="" style="{'background:rgba(79,126,255,0.12);color:var(--accent);' if active else ''}">
                {icon} {label}{badge_html}
            </div>
            """, unsafe_allow_html=True)
            if st.button(label, key=f"nav_{page}", use_container_width=True,
                         help=f"Go to {label}",
                         type="primary" if active else "secondary"):
                st.session_state.active_page = page
                st.session_state.selected_uc = None
                st.rerun()

        st.markdown('<div style="font-size:0.7rem;font-weight:600;color:var(--text2);letter-spacing:0.08em;text-transform:uppercase;margin-bottom:0.4rem;">Main</div>', unsafe_allow_html=True)

        nav_btn("📊", "Dashboard", "Dashboard")
        nav_btn("📦", "Use Cases", "Use Cases")

        if role in ["AI Team Member", "Admin"]:
            nav_btn("📈", "Analytics", "Analytics")
            nav_btn("💰", "Cost Tracking", "Cost Tracking")
            nav_btn("⚡", "Performance", "Performance")

        st.markdown('<div style="font-size:0.7rem;font-weight:600;color:var(--text2);letter-spacing:0.08em;text-transform:uppercase;margin:0.8rem 0 0.4rem 0;">Management</div>', unsafe_allow_html=True)

        nav_btn("🔐", "Access Control", "Access Control")
        nav_btn("🤖", "Models", "Models")

        if role in ["AI Team Member", "Admin"]:
            nav_btn("📋", "Activity Log", "Activity Log")
            nav_btn("👥", "User Feedback", "User Feedback")

        st.markdown('<div style="font-size:0.7rem;font-weight:600;color:var(--text2);letter-spacing:0.08em;text-transform:uppercase;margin:0.8rem 0 0.4rem 0;">System</div>', unsafe_allow_html=True)

        nav_btn("🔔", "Notifications", "Notifications", badge=unread if unread else None)
        nav_btn("⚙️", "Settings", "Settings")

        if role == "Admin":
            nav_btn("🛡️", "Admin Panel", "Admin Panel")

        st.markdown("---")

        # Theme toggle
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🌙 Dark" if not st.session_state.dark_mode else "☀️ Light", use_container_width=True):
                st.session_state.dark_mode = not st.session_state.dark_mode
                st.rerun()
        with col2:
            if st.button("Sign Out", use_container_width=True):
                # Preserve theme preference and data, reset everything else
                dark_mode = st.session_state.get("dark_mode", True)
                data = st.session_state.get("data", None)
                st.session_state.clear()
                st.session_state.dark_mode = dark_mode
                if data:
                    st.session_state.data = data
                st.session_state.logged_in = False
                st.rerun()

# ─────────────────────────────────────────────
#  HELPER: Metric Card HTML
# ─────────────────────────────────────────────
def metric_card(label, value, delta=None, delta_up=True):
    delta_html = ""
    if delta:
        cls = "delta-up" if delta_up else "delta-down"
        arrow = "↑" if delta_up else "↓"
        delta_html = f'<div class="metric-delta {cls}">{arrow} {delta}</div>'
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-value">{value}</div>
        {delta_html}
    </div>
    """

def status_badge(status):
    cls_map = {"active": "badge-active", "inactive": "badge-inactive",
               "draft": "badge-draft", "pending": "badge-pending",
               "approved": "badge-active", "rejected": "badge-inactive"}
    return f'<span class="badge {cls_map.get(status, "badge-draft")}">{status.upper()}</span>'

# ─────────────────────────────────────────────
#  PAGE: DASHBOARD
# ─────────────────────────────────────────────
def render_dashboard():
    data  = st.session_state.data
    email = st.session_state.current_user
    user  = data["users"][email]
    role  = user["role"]

    ucs = data["use_cases"]
    if role == "Use Case Owner":
        ucs = [u for u in ucs if u["owner"] == email]

    # ── Header ──
    st.markdown(f"""
    <div class="section-header">📊 Dashboard</div>
    <div class="section-sub">Welcome back, {user['name'].split()[0]}. Here's your platform overview.</div>
    """, unsafe_allow_html=True)

    # ── Top KPIs ──
    total_calls   = sum(u["usage_count"] for u in ucs)
    total_cost    = sum(u["monthly_cost"] for u in ucs)
    active_count  = sum(1 for u in ucs if u["status"] == "active")
    avg_success   = np.mean([u["success_rate"] for u in ucs]) if ucs else 0
    avg_resp_ms   = np.mean([u["avg_response_ms"] for u in ucs]) if ucs else 0

    c1, c2, c3, c4, c5 = st.columns(5)
    with c1: st.markdown(metric_card("Total API Calls", f"{total_calls:,}", "12.4% vs last month", True), unsafe_allow_html=True)
    with c2: st.markdown(metric_card("Monthly Cost", f"${total_cost:,.2f}", "8.1% vs last month", False), unsafe_allow_html=True)
    with c3: st.markdown(metric_card("Active Use Cases", str(active_count), f"{len(ucs)} total"), unsafe_allow_html=True)
    with c4: st.markdown(metric_card("Avg Success Rate", f"{avg_success:.1f}%", "0.3% vs last month", True), unsafe_allow_html=True)
    with c5: st.markdown(metric_card("Avg Response Time", f"{avg_resp_ms:.0f}ms", "Stable"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Charts row ──
    col_left, col_right = st.columns([2, 1])

    with col_left:
        # Usage trend across all use cases
        dates  = data["dates"][-30:]
        totals = np.zeros(30)
        for uc in ucs:
            totals += np.array(data["usage_series"][uc["id"]][-30:])

        df_trend = pd.DataFrame({"Date": dates, "API Calls": totals.astype(int)})
        fig = px.area(df_trend, x="Date", y="API Calls",
                      title="API Calls — Last 30 Days",
                      color_discrete_sequence=["#4F7EFF"])
        fig.update_traces(fill="tozeroy", line_width=2,
                          fillcolor="rgba(79,126,255,0.12)")
        style_fig(fig, 280)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col_right:
        # Model distribution pie
        model_usage = {}
        for uc in ucs:
            m = uc["model"]
            model_usage[m] = model_usage.get(m, 0) + uc["usage_count"]

        model_names = {m["id"]: m["name"] for m in data["models"]}
        labels = [model_names.get(k, k) for k in model_usage.keys()]
        values = list(model_usage.values())

        fig2 = go.Figure(go.Pie(
            labels=labels, values=values,
            hole=0.6,
            textinfo="percent",
            textfont=dict(size=10),
            marker=dict(colors=["#4F7EFF","#7C5CFC","#2ECC71","#F39C12","#E74C3C","#1ABC9C","#3498DB","#9B59B6"]),
        ))
        fig2.update_layout(
            title="Model Distribution",
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color=chart_theme()["font_color"], family="DM Sans"),
            height=280, margin=dict(l=0, r=0, t=30, b=0),
            legend=dict(font=dict(size=9), bgcolor="rgba(0,0,0,0)"),
            showlegend=True,
        )
        fig2.add_annotation(text=f"{sum(values):,}<br>total calls",
                            x=0.5, y=0.5, showarrow=False,
                            font=dict(size=12, color=chart_theme()["font_color"]))
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # ── Use Cases quick view ──
    st.markdown("---")
    st.markdown('<div class="section-header" style="font-size:1rem;">🗂 Use Case Overview</div>', unsafe_allow_html=True)

    # Sort by usage
    sorted_ucs = sorted(ucs, key=lambda x: x["usage_count"], reverse=True)

    for uc in sorted_ucs[:6]:
        with st.container():
            c1, c2, c3, c4, c5 = st.columns([3, 1.5, 1.2, 1.2, 1])
            with c1:
                st.markdown(f"""
                <div style="font-weight:600;color:var(--text);font-size:0.9rem;">{uc['name']}</div>
                <div style="font-size:0.78rem;color:var(--text2);">{uc['type']} · {uc['business_unit']}</div>
                """, unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style="font-size:0.78rem;color:var(--text2);">Calls</div>
                <div style="font-weight:600;color:var(--text);font-size:0.9rem;">{uc['usage_count']:,}</div>
                """, unsafe_allow_html=True)
            with c3:
                st.markdown(f"""
                <div style="font-size:0.78rem;color:var(--text2);">Cost / mo</div>
                <div style="font-weight:600;color:var(--text);font-size:0.9rem;">${uc['monthly_cost']:,.0f}</div>
                """, unsafe_allow_html=True)
            with c4:
                st.markdown(f"""
                <div style="font-size:0.78rem;color:var(--text2);">Success Rate</div>
                <div style="font-weight:600;color:var(--text);font-size:0.9rem;">{uc['success_rate']}%</div>
                """, unsafe_allow_html=True)
            with c5:
                st.markdown(status_badge(uc["status"]), unsafe_allow_html=True)
                if st.button("View", key=f"dash_view_{uc['id']}", use_container_width=True):
                    st.session_state.selected_uc = uc["id"]
                    st.session_state.active_page = "Use Cases"
                    st.rerun()
            st.markdown('<hr style="margin:0.4rem 0;">', unsafe_allow_html=True)

    # ── Notifications preview ──
    unread = [n for n in data["notifications"] if not n["read"]]
    if unread:
        st.markdown("---")
        st.markdown('<div class="section-header" style="font-size:1rem;">🔔 Unread Alerts</div>', unsafe_allow_html=True)
        for n in unread[:3]:
            cls = {"warn": "notif-warn", "error": "notif-error", "success": "notif-success"}.get(n["type"], "")
            icon = {"warn": "⚠️", "error": "🚨", "info": "ℹ️", "success": "✅"}.get(n["type"], "📢")
            st.markdown(f"""
            <div class="notif-item {cls}">
                {icon} <strong>{n['title']}</strong> — {n['msg']}
                <span style="color:var(--text2);font-size:0.72rem;margin-left:0.5rem;">
                    {n['time'].strftime('%b %d, %H:%M')}
                </span>
            </div>
            """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: USE CASES
# ─────────────────────────────────────────────
def render_use_cases():
    data  = st.session_state.data
    email = st.session_state.current_user
    user  = data["users"][email]
    role  = user["role"]

    all_ucs = data["use_cases"]
    my_ucs  = all_ucs if role in ["AI Team Member", "Admin"] else [u for u in all_ucs if u["owner"] == email]

    # Detail view
    if st.session_state.selected_uc:
        render_uc_detail(st.session_state.selected_uc)
        return

    # Create form
    if st.session_state.show_create_uc:
        render_create_uc()
        return

    st.markdown('<div class="section-header">📦 Use Cases</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Manage and monitor all AI use cases.</div>', unsafe_allow_html=True)

    # Search & filter bar
    c1, c2, c3, c4 = st.columns([3, 1.5, 1.5, 1])
    with c1:
        search = st.text_input("", placeholder="🔍  Search use cases…", label_visibility="collapsed")
    with c2:
        status_filter = st.selectbox("Status", ["All", "active", "inactive", "draft"], label_visibility="collapsed")
    with c3:
        type_filter = st.selectbox("Type", ["All Types"] + sorted(set(u["type"] for u in my_ucs)), label_visibility="collapsed")
    with c4:
        if st.button("＋ New Use Case", use_container_width=True):
            st.session_state.show_create_uc = True
            st.rerun()

    # Filter
    filtered = my_ucs
    if search:
        q = search.lower()
        filtered = [u for u in filtered if q in u["name"].lower() or q in u["description"].lower()]
    if status_filter != "All":
        filtered = [u for u in filtered if u["status"] == status_filter]
    if type_filter != "All Types":
        filtered = [u for u in filtered if u["type"] == type_filter]

    st.markdown(f'<div style="color:var(--text2);font-size:0.82rem;margin-bottom:0.8rem;">{len(filtered)} use case{"s" if len(filtered)!=1 else ""} found</div>', unsafe_allow_html=True)

    # Bulk actions
    if role in ["AI Team Member", "Admin"] and filtered:
        with st.expander("⚡ Bulk Operations"):
            bc1, bc2, bc3, bc4 = st.columns(4)
            with bc1:
                if st.button("✅ Enable All Filtered", use_container_width=True):
                    for uc in filtered:
                        uc["status"] = "active"
                    st.success(f"Enabled {len(filtered)} use cases")
                    st.rerun()
            with bc2:
                if st.button("⏸ Disable All Filtered", use_container_width=True):
                    for uc in filtered:
                        uc["status"] = "inactive"
                    st.warning(f"Disabled {len(filtered)} use cases")
                    st.rerun()
            with bc3:
                bulk_model = st.selectbox("Bulk change model to:", ["— select —"] + [m["id"] for m in data["models"] if m["status"] == "active"], label_visibility="collapsed")
            with bc4:
                if st.button("Apply Model Change", use_container_width=True):
                    if bulk_model != "— select —":
                        for uc in filtered:
                            uc["model"] = bulk_model
                        st.success(f"Updated model for {len(filtered)} use cases")
                        st.rerun()

    # Cards grid (2-column)
    model_names = {m["id"]: m["name"] for m in data["models"]}
    owner_names = {k: v["name"] for k, v in data["users"].items()}

    for i in range(0, len(filtered), 2):
        col_a, col_b = st.columns(2)
        for col, idx in zip([col_a, col_b], [i, i+1]):
            if idx >= len(filtered):
                break
            uc = filtered[idx]
            with col:
                last_ts = uc["last_accessed"]
                last_str = last_ts.strftime("%b %d, %H:%M") if isinstance(last_ts, datetime) else str(last_ts)
                st.markdown(f"""
                <div class="uc-card">
                    <div style="display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:0.5rem;">
                        <div class="uc-title">{uc['name']}</div>
                        {status_badge(uc['status'])}
                    </div>
                    <div class="uc-meta" style="margin-bottom:0.7rem;line-height:1.5;">{uc['description'][:100]}{'...' if len(uc['description'])>100 else ''}</div>
                    <div style="display:flex;gap:1rem;margin-bottom:0.7rem;">
                        <span class="uc-meta">🤖 {model_names.get(uc['model'], uc['model'])}</span>
                        <span class="uc-meta">📂 {uc['type']}</span>
                        <span class="uc-meta">🏢 {uc['business_unit']}</span>
                    </div>
                    <div style="display:flex;gap:1rem;">
                        <span class="uc-meta">⚡ {uc['usage_count']:,} calls</span>
                        <span class="uc-meta">💰 ${uc['monthly_cost']:,.0f}/mo</span>
                        <span class="uc-meta">⏱ Last: {last_str}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                # Action buttons
                ac1, ac2, ac3, ac4 = st.columns(4)
                with ac1:
                    if st.button("Details", key=f"view_{uc['id']}", use_container_width=True):
                        st.session_state.selected_uc = uc["id"]
                        st.rerun()
                with ac2:
                    if st.button("Edit", key=f"edit_{uc['id']}", use_container_width=True):
                        st.session_state.selected_uc = uc["id"]
                        st.session_state.edit_mode = True
                        st.rerun()
                with ac3:
                    if st.button("Clone", key=f"clone_{uc['id']}", use_container_width=True):
                        cloned = dict(uc)
                        cloned["id"] = f"uc-{len(data['use_cases'])+1:03d}"
                        cloned["name"] = f"{uc['name']} (Copy)"
                        cloned["status"] = "draft"
                        cloned["usage_count"] = 0
                        cloned["monthly_cost"] = 0.0
                        cloned["created"] = datetime.now()
                        cloned["last_accessed"] = datetime.now()
                        data["use_cases"].append(cloned)
                        data["usage_series"][cloned["id"]] = [0] * 90
                        data["cost_series"][cloned["id"]] = [0.0] * 90
                        st.success(f"Cloned → '{cloned['name']}'")
                        st.rerun()
                with ac4:
                    if st.button("🗑", key=f"del_{uc['id']}", use_container_width=True):
                        data["use_cases"].remove(uc)
                        st.warning(f"Deleted '{uc['name']}'")
                        st.rerun()

# ─────────────────────────────────────────────
#  PAGE: USE CASE DETAIL
# ─────────────────────────────────────────────
def render_uc_detail(uc_id):
    data  = st.session_state.data
    email = st.session_state.current_user
    user  = data["users"][email]

    uc = next((u for u in data["use_cases"] if u["id"] == uc_id), None)
    if not uc:
        st.error("Use case not found.")
        return

    model_info   = next((m for m in data["models"] if m["id"] == uc["model"]), {})
    owner_name   = data["users"].get(uc["owner"], {}).get("name", uc["owner"])
    model_names  = {m["id"]: m["name"] for m in data["models"]}

    # Back button
    if st.button("← Back to Use Cases"):
        st.session_state.selected_uc = None
        st.session_state.edit_mode = False
        st.rerun()

    st.markdown(f"""
    <div class="section-header">{uc['name']} {status_badge(uc['status'])}</div>
    <div class="section-sub">{uc['description']}</div>
    """, unsafe_allow_html=True)

    tabs = st.tabs(["📋 Overview", "⚙️ Parameters", "📊 Analytics", "🧪 A/B Testing", "📝 History"])

    # ── Tab 1: Overview ──
    with tabs[0]:
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("**Use Case Info**")
            info = {
                "ID": uc["id"], "Type": uc["type"], "Business Unit": uc["business_unit"],
                "Owner": owner_name, "Status": uc["status"].capitalize(),
                "Created": uc["created"].strftime("%B %d, %Y"),
                "Last Accessed": uc["last_accessed"].strftime("%b %d, %Y %H:%M"),
                "Intended Users": ", ".join(uc["users"]),
                "Tags": ", ".join(uc["tags"]),
            }
            for k, v in info.items():
                st.markdown(f"""
                <div style="display:flex;justify-content:space-between;padding:0.4rem 0;border-bottom:1px solid var(--border);font-size:0.85rem;">
                    <span style="color:var(--text2);">{k}</span>
                    <span style="color:var(--text);font-weight:500;">{v}</span>
                </div>
                """, unsafe_allow_html=True)
        with c2:
            st.markdown("**Performance Metrics**")
            mc1, mc2 = st.columns(2)
            with mc1:
                st.markdown(metric_card("Total Calls", f"{uc['usage_count']:,}", "all time"), unsafe_allow_html=True)
                st.markdown(metric_card("Monthly Cost", f"${uc['monthly_cost']:,.2f}", "this month"), unsafe_allow_html=True)
            with mc2:
                st.markdown(metric_card("Success Rate", f"{uc['success_rate']}%", "30-day avg"), unsafe_allow_html=True)
                st.markdown(metric_card("Avg Response", f"{uc['avg_response_ms']}ms", "30-day avg"), unsafe_allow_html=True)

            st.markdown("<br>**Current Model**", unsafe_allow_html=True)
            if model_info:
                st.markdown(f"""
                <div class="uc-card">
                    <div style="font-weight:600;color:var(--text);">{model_info.get('name','—')}</div>
                    <div style="font-size:0.8rem;color:var(--text2);">Provider: {model_info.get('provider','—')} · Context: {model_info.get('context','—')}</div>
                    <div style="font-size:0.8rem;color:var(--text2);">Cost: ${model_info.get('cost_per_1k',0):.4f} / 1K tokens</div>
                    <div style="margin-top:0.5rem;">{' '.join(['<span class="badge badge-pending" style="margin-right:3px;">'+s+'</span>' for s in model_info.get('strengths',[])])}</div>
                </div>
                """, unsafe_allow_html=True)

        # Status & model change
        st.markdown("---")
        st.markdown("**Quick Actions**")
        qa1, qa2, qa3 = st.columns(3)
        with qa1:
            new_status = st.selectbox("Change Status", ["active", "inactive", "draft"],
                                      index=["active","inactive","draft"].index(uc["status"]), key="status_chg")
            if st.button("Apply Status", key="apply_status", use_container_width=True):
                uc["status"] = new_status
                st.success(f"Status updated to {new_status}")
                st.rerun()
        with qa2:
            active_models = [m["id"] for m in data["models"] if m["status"] == "active"]
            cur_idx = active_models.index(uc["model"]) if uc["model"] in active_models else 0
            new_model = st.selectbox("Change Model", active_models,
                                     format_func=lambda x: model_names.get(x, x),
                                     index=cur_idx, key="model_chg")
            if st.button("Apply Model", key="apply_model", use_container_width=True):
                uc["model"] = new_model
                st.success(f"Model changed to {model_names.get(new_model,new_model)}")
                st.rerun()
        with qa3:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("✏️ Full Edit", use_container_width=True):
                st.session_state.edit_mode = True
                st.rerun()

    # ── Tab 2: Parameters ──
    with tabs[1]:
        render_param_config(uc)

    # ── Tab 3: Analytics ──
    with tabs[2]:
        # Usage trend for this UC
        series = data["usage_series"][uc_id]
        costs  = data["cost_series"][uc_id]
        dates  = data["dates"]

        sub_tabs = st.tabs(["Usage", "Cost", "Performance"])
        with sub_tabs[0]:
            df = pd.DataFrame({"Date": dates, "API Calls": series})
            fig = px.line(df, x="Date", y="API Calls", title="Daily API Calls — 90 Days",
                         color_discrete_sequence=["#4F7EFF"])
            fig.update_traces(line_width=2)
            style_fig(fig, 300)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        with sub_tabs[1]:
            df2 = pd.DataFrame({"Date": dates, "Cost ($)": costs})
            fig2 = px.bar(df2, x="Date", y="Cost ($)", title="Daily Cost — 90 Days",
                         color_discrete_sequence=["#7C5CFC"])
            style_fig(fig2, 300)
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
        with sub_tabs[2]:
            # Simulated performance metrics
            perf_dates = dates[-30:]
            success = np.clip(np.random.normal(uc["success_rate"], 0.5, 30), 90, 100)
            resp    = np.clip(np.random.normal(uc["avg_response_ms"], 100, 30), 200, 5000)
            df3 = pd.DataFrame({"Date": perf_dates, "Success Rate (%)": success, "Response Time (ms)": resp})
            fig3 = make_subplots(specs=[[{"secondary_y": True}]])
            fig3.add_trace(go.Scatter(x=df3["Date"], y=df3["Success Rate (%)"],
                                       name="Success Rate", line=dict(color="#2ECC71", width=2)), secondary_y=False)
            fig3.add_trace(go.Scatter(x=df3["Date"], y=df3["Response Time (ms)"],
                                       name="Response Time", line=dict(color="#F39C12", width=2)), secondary_y=True)
            t = chart_theme()
            fig3.update_layout(paper_bgcolor=t["paper_bg"], plot_bgcolor=t["plot_bg"],
                               font=dict(color=t["font_color"], family="DM Sans"),
                               height=300, margin=dict(l=10,r=10,t=30,b=10),
                               title="Performance — Last 30 Days",
                               legend=dict(bgcolor="rgba(0,0,0,0)"))
            st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    # ── Tab 4: A/B Testing ──
    with tabs[3]:
        render_ab_test(uc)

    # ── Tab 5: History ──
    with tabs[4]:
        st.markdown("**Audit History for this Use Case**")
        uc_audit = [a for a in data["audit"] if a["uc_id"] == uc_id]
        if not uc_audit:
            st.info("No audit events recorded yet.")
        else:
            for a in uc_audit:
                actor_name = data["users"].get(a["actor"], {}).get("name", a["actor"])
                st.markdown(f"""
                <div class="activity-item">
                    <span class="activity-time">{a['timestamp'].strftime('%b %d %H:%M')}</span>
                    <span class="activity-text"><strong>{a['action']}</strong>: {a['detail']} — by {actor_name}</span>
                </div>
                """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PARAMETER CONFIGURATION
# ─────────────────────────────────────────────
def render_param_config(uc):
    data = st.session_state.data

    presets = {
        "Creative":  {"temperature": 1.2, "max_tokens": 2048, "top_p": 0.95, "frequency_penalty": 0.5, "presence_penalty": 0.5},
        "Balanced":  {"temperature": 0.7, "max_tokens": 1024, "top_p": 0.90, "frequency_penalty": 0.1, "presence_penalty": 0.1},
        "Precise":   {"temperature": 0.1, "max_tokens": 512,  "top_p": 0.80, "frequency_penalty": 0.0, "presence_penalty": 0.0},
    }

    st.markdown("**Parameter Presets**")
    pc1, pc2, pc3, pc4 = st.columns(4)
    for btn_col, (pname, pvals) in zip([pc1, pc2, pc3], presets.items()):
        with btn_col:
            if st.button(f"{pname}", key=f"preset_{pname}_{uc['id']}", use_container_width=True):
                uc["params"].update(pvals)
                st.success(f"Applied '{pname}' preset")
                st.rerun()
    with pc4:
        if st.button("↺ Reset Defaults", key=f"reset_params_{uc['id']}", use_container_width=True):
            uc["params"] = {"temperature": 0.7, "max_tokens": 1024, "top_p": 0.9,
                            "frequency_penalty": 0.0, "presence_penalty": 0.0,
                            "response_format": "Text", "seed": None}
            st.rerun()

    st.markdown("---")
    c1, c2 = st.columns(2)

    with c1:
        st.markdown("**Generation Parameters**")
        temp = st.slider("🌡 Temperature", 0.0, 2.0, float(uc["params"]["temperature"]), 0.05,
                         help="Higher = more creative/random; Lower = more focused/deterministic")
        top_p = st.slider("🎯 Top-P (nucleus sampling)", 0.0, 1.0, float(uc["params"]["top_p"]), 0.01,
                          help="Cumulative probability cutoff for token selection")
        freq_pen = st.slider("🔁 Frequency Penalty", -2.0, 2.0, float(uc["params"]["frequency_penalty"]), 0.05,
                             help="Reduces repetition of frequent tokens")
        pres_pen = st.slider("✨ Presence Penalty", -2.0, 2.0, float(uc["params"]["presence_penalty"]), 0.05,
                             help="Encourages new topics by penalizing already-used tokens")

    with c2:
        st.markdown("**Output Parameters**")
        max_tok = st.number_input("📏 Max Tokens", min_value=1, max_value=128000,
                                  value=int(uc["params"]["max_tokens"]),
                                  help="Maximum tokens in the response")
        resp_fmt = st.selectbox("📄 Response Format", ["Text", "JSON", "Markdown"],
                                index=["Text","JSON","Markdown"].index(uc["params"]["response_format"]),
                                help="Expected output format")
        seed_val = st.number_input("🌱 Seed (for reproducibility)", min_value=-1, max_value=99999,
                                   value=int(uc["params"]["seed"]) if uc["params"]["seed"] else -1,
                                   help="-1 means no seed (random)")

        st.markdown("**Custom Parameters (JSON)**")
        custom_json = st.text_area("Advanced / custom parameters", value="{}", height=80,
                                   help="Provider-specific parameters as JSON",
                                   key=f"custom_params_{uc['id']}")

    if st.button("💾 Save Parameters", key=f"save_params_{uc['id']}", type="primary", use_container_width=False):
        try:
            json.loads(custom_json)  # validate
            uc["params"]["temperature"]      = temp
            uc["params"]["max_tokens"]       = max_tok
            uc["params"]["top_p"]            = top_p
            uc["params"]["frequency_penalty"]= freq_pen
            uc["params"]["presence_penalty"] = pres_pen
            uc["params"]["response_format"]  = resp_fmt
            uc["params"]["seed"]             = seed_val if seed_val >= 0 else None
            st.success("✅ Parameters saved successfully!")
        except json.JSONDecodeError:
            st.error("Custom parameters JSON is invalid.")

    # Parameter summary
    with st.expander("📋 Current Parameter Summary"):
        st.json(uc["params"])

# ─────────────────────────────────────────────
#  A/B TESTING
# ─────────────────────────────────────────────
def render_ab_test(uc):
    data = st.session_state.data
    model_names = {m["id"]: m["name"] for m in data["models"]}
    active_models = [m["id"] for m in data["models"] if m["status"] == "active"]

    st.markdown("**Configure A/B Test**")
    st.info("Run side-by-side model comparisons to evaluate performance before switching.")

    tc1, tc2 = st.columns(2)
    with tc1:
        st.markdown("**Variant A (Control)**")
        st.markdown(f"Current model: **{model_names.get(uc['model'], uc['model'])}**")
        st.markdown(f"Temperature: **{uc['params']['temperature']}**")
    with tc2:
        st.markdown("**Variant B (Challenger)**")
        b_model = st.selectbox("Model", active_models, format_func=lambda x: model_names.get(x,x), key=f"ab_model_{uc['id']}")
        b_temp  = st.slider("Temperature", 0.0, 2.0, 0.7, 0.05, key=f"ab_temp_{uc['id']}")

    traffic_split = st.slider("Traffic split (% to Variant B)", 0, 100, 20, 5,
                              help="What % of traffic goes to the challenger model")
    sample_size = st.number_input("Target sample size (calls)", min_value=100, max_value=10000, value=1000, step=100)

    if st.button("🚀 Launch A/B Test", key=f"launch_ab_{uc['id']}", use_container_width=False):
        ab_key = uc["id"]
        st.session_state.ab_test[ab_key] = {
            "variant_a": {"model": uc["model"], "temp": uc["params"]["temperature"]},
            "variant_b": {"model": b_model, "temp": b_temp},
            "split": traffic_split,
            "target": sample_size,
            "progress": random.randint(20, 80),
            "started": datetime.now().strftime("%b %d %H:%M"),
        }
        st.success("A/B Test launched!")
        st.rerun()

    # Show active test results
    if uc["id"] in st.session_state.ab_test:
        ab = st.session_state.ab_test[uc["id"]]
        st.markdown("---")
        st.markdown("**Active A/B Test — Live Results**")
        progress = ab["progress"]
        st.progress(progress / 100, text=f"Progress: {progress}% of {ab['target']} target samples")

        rr1, rr2, rr3, rr4 = st.columns(4)
        with rr1: st.metric("A — Success Rate", "98.1%", "")
        with rr2: st.metric("B — Success Rate", "97.8%", "-0.3%")
        with rr3: st.metric("A — Avg Response", "1230ms", "")
        with rr4: st.metric("B — Avg Response", "1050ms", "-180ms ✓")

        rr5, rr6 = st.columns(2)
        with rr5: st.metric("A — Est. Monthly Cost", "$284", "")
        with rr6: st.metric("B — Est. Monthly Cost", "$195", "-$89/mo ✓")

        if st.button("⏹ Stop Test & Apply Variant B", key=f"stop_ab_{uc['id']}", use_container_width=False):
            uc["model"] = ab["variant_b"]["model"]
            uc["params"]["temperature"] = ab["variant_b"]["temp"]
            del st.session_state.ab_test[uc["id"]]
            st.success(f"Applied Variant B model: {model_names.get(uc['model'], uc['model'])}")
            st.rerun()

# ─────────────────────────────────────────────
#  CREATE USE CASE FORM
# ─────────────────────────────────────────────
def render_create_uc():
    data  = st.session_state.data
    email = st.session_state.current_user
    model_names = {m["id"]: m["name"] for m in data["models"]}

    if st.button("← Back"):
        st.session_state.show_create_uc = False
        st.rerun()

    st.markdown('<div class="section-header">➕ Create New Use Case</div>', unsafe_allow_html=True)

    with st.form("create_uc_form"):
        c1, c2 = st.columns(2)
        with c1:
            name = st.text_input("Use Case Name *", placeholder="e.g. Contract Summarizer")
            uc_type = st.selectbox("Type *", ["Content Generation","Text Analysis","Summarization",
                                               "Document Review","Data Analysis","Report Generation",
                                               "Anomaly Detection","Chatbot","Code Generation","Other"])
            business_unit = st.selectbox("Business Unit *", ["Marketing","Operations","Finance",
                                                              "HR","IT","Legal","Sales","Product","Other"])
            model = st.selectbox("AI Model *",
                                 [m["id"] for m in data["models"] if m["status"] == "active"],
                                 format_func=lambda x: model_names.get(x, x))
        with c2:
            description = st.text_area("Description *", placeholder="Describe the use case purpose and expected outputs...", height=120)
            intended_users = st.text_input("Intended User Groups", placeholder="e.g. marketing-team, agency-partners")
            tags = st.text_input("Tags (comma-separated)", placeholder="e.g. content, automation, q4")
            owner = st.selectbox("Owner", list(data["users"].keys()),
                                 index=list(data["users"].keys()).index(email) if email in data["users"] else 0,
                                 format_func=lambda x: data["users"][x]["name"])

        st.markdown("**Initial Parameters**")
        pc1, pc2, pc3 = st.columns(3)
        with pc1: temp_init = st.slider("Temperature", 0.0, 2.0, 0.7, 0.05, key="create_temp")
        with pc2: max_tok_init = st.number_input("Max Tokens", 1, 128000, 1024, key="create_maxtok")
        with pc3: resp_fmt_init = st.selectbox("Response Format", ["Text","JSON","Markdown"], key="create_fmt")

        submitted = st.form_submit_button("✅ Create Use Case", use_container_width=False)
        if submitted:
            if not name or not description:
                st.error("Name and description are required.")
            else:
                new_uc = {
                    "id": f"uc-{len(data['use_cases'])+1:03d}",
                    "name": name, "description": description, "owner": owner,
                    "business_unit": business_unit, "type": uc_type, "status": "draft",
                    "model": model, "created": datetime.now(),
                    "last_accessed": datetime.now(),
                    "usage_count": 0, "monthly_cost": 0.0,
                    "avg_response_ms": 0, "success_rate": 0.0,
                    "users": [u.strip() for u in intended_users.split(",") if u.strip()],
                    "tags": [t.strip() for t in tags.split(",") if t.strip()],
                    "params": {"temperature": temp_init, "max_tokens": max_tok_init,
                               "top_p": 0.9, "frequency_penalty": 0.0,
                               "presence_penalty": 0.0, "response_format": resp_fmt_init, "seed": None},
                }
                data["use_cases"].append(new_uc)
                data["usage_series"][new_uc["id"]] = [0] * 90
                data["cost_series"][new_uc["id"]] = [0.0] * 90
                st.success(f"✅ Use case '{name}' created successfully!")
                st.session_state.show_create_uc = False
                st.rerun()

# ─────────────────────────────────────────────
#  PAGE: ACCESS CONTROL (global)
# ─────────────────────────────────────────────
def render_access_control():
    data  = st.session_state.data
    email = st.session_state.current_user
    user  = data["users"][email]
    role  = user["role"]

    ucs = data["use_cases"]
    if role == "Use Case Owner":
        ucs = [u for u in ucs if u["owner"] == email]

    st.markdown('<div class="section-header">🔐 Access Control</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Manage user and group access across all use cases.</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Access Matrix", "Pending Requests", "Request History"])

    with tabs[0]:
        st.markdown("**Access Matrix Overview**")
        matrix_data = []
        for uc in ucs:
            for grp in uc["users"]:
                matrix_data.append({"Use Case": uc["name"], "User/Group": grp,
                                     "Permission": "Full Access", "Status": "Active"})
        if matrix_data:
            df = pd.DataFrame(matrix_data)
            st.dataframe(df, use_container_width=True, hide_index=True)
        else:
            st.info("No access entries found.")

    with tabs[1]:
        pending = [r for r in data["access_requests"] if r["status"] == "pending"]
        if not pending:
            st.success("No pending access requests.")
        else:
            for req in pending:
                uc = next((u for u in data["use_cases"] if u["id"] == req["uc_id"]), None)
                if not uc:
                    continue
                with st.container():
                    rc1, rc2, rc3, rc4, rc5 = st.columns([2, 2, 3, 1, 1])
                    with rc1: st.markdown(f"**{req['requester']}**\n\n_{req['role']}_")
                    with rc2: st.markdown(f"Use Case:\n\n**{uc['name']}**")
                    with rc3: st.markdown(f"Reason: _{req['reason']}_")
                    with rc4:
                        if st.button("✅", key=f"g_approve_{req['id']}", use_container_width=True, help="Approve"):
                            req["status"] = "approved"
                            uc["users"].append(req["requester"])
                            st.success("Approved!")
                            st.rerun()
                    with rc5:
                        if st.button("❌", key=f"g_reject_{req['id']}", use_container_width=True, help="Reject"):
                            req["status"] = "rejected"
                            st.warning("Rejected.")
                            st.rerun()
                    st.markdown("---")

    with tabs[2]:
        history = [r for r in data["access_requests"] if r["status"] != "pending"]
        if not history:
            st.info("No request history yet.")
        else:
            hist_data = []
            for r in history:
                uc = next((u for u in data["use_cases"] if u["id"] == r["uc_id"]), {})
                hist_data.append({
                    "Requester": r["requester"],
                    "Use Case": uc.get("name", r["uc_id"]),
                    "Status": r["status"].upper(),
                    "Requested": r["requested"].strftime("%b %d, %Y"),
                    "Reason": r["reason"][:60] + "…",
                })
            st.dataframe(pd.DataFrame(hist_data), use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────
#  PAGE: MODEL MANAGEMENT
# ─────────────────────────────────────────────
def render_models():
    data = st.session_state.data

    st.markdown('<div class="section-header">🤖 Model Management</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Explore, compare, and manage available AI models.</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Model Catalog", "Comparison", "Usage by Model"])

    with tabs[0]:
        for m in data["models"]:
            dep = m["status"] == "deprecated"
            border_col = "var(--red)" if dep else "var(--border)"
            st.markdown(f"""
            <div class="uc-card" style="{'border-color:var(--red);opacity:0.7;' if dep else ''}">
                <div style="display:flex;justify-content:space-between;">
                    <div>
                        <div style="font-weight:600;font-size:0.95rem;color:var(--text);">{m['name']}</div>
                        <div style="font-size:0.78rem;color:var(--text2);">Provider: {m['provider']} · Context: {m['context']} · ${m['cost_per_1k']:.4f}/1K tokens</div>
                    </div>
                    {status_badge('inactive' if dep else 'active')}
                </div>
                <div style="margin-top:0.5rem;">
                    {''.join([f'<span class="badge badge-pending" style="margin-right:3px;">{s}</span>' for s in m['strengths']])}
                    {f'<span class="badge badge-inactive" style="margin-left:0.5rem;">⚠️ DEPRECATED — Migrate immediately</span>' if dep else ''}
                </div>
            </div>
            """, unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("**Side-by-Side Model Comparison**")
        active_models = [m for m in data["models"] if m["status"] == "active"]
        cc1, cc2 = st.columns(2)
        with cc1:
            model_a_id = st.selectbox("Model A", [m["id"] for m in active_models],
                                       format_func=lambda x: next(m["name"] for m in active_models if m["id"]==x),
                                       key="cmp_a")
        with cc2:
            model_b_id = st.selectbox("Model B", [m["id"] for m in active_models],
                                       format_func=lambda x: next(m["name"] for m in active_models if m["id"]==x),
                                       index=1, key="cmp_b")

        model_a = next(m for m in data["models"] if m["id"] == model_a_id)
        model_b = next(m for m in data["models"] if m["id"] == model_b_id)

        cmp_data = {
            "Attribute": ["Provider", "Context Window", "Cost/1K tokens", "Strengths", "Status"],
            model_a["name"]: [model_a["provider"], model_a["context"],
                              f"${model_a['cost_per_1k']:.4f}",
                              ", ".join(model_a["strengths"]), model_a["status"].capitalize()],
            model_b["name"]: [model_b["provider"], model_b["context"],
                              f"${model_b['cost_per_1k']:.4f}",
                              ", ".join(model_b["strengths"]), model_b["status"].capitalize()],
        }
        st.dataframe(pd.DataFrame(cmp_data).set_index("Attribute"), use_container_width=True)

        # Radar chart comparison (simulated scores)
        categories = ["Speed", "Cost Efficiency", "Context Length", "Reasoning", "Creativity", "Safety"]
        model_scores = {
            "gpt-4o":         [80, 60, 75, 95, 88, 82],
            "gpt-4o-mini":    [95, 92, 75, 72, 70, 78],
            "claude-3-5":     [78, 72, 92, 90, 85, 96],
            "claude-3-haiku": [96, 94, 92, 70, 68, 92],
            "gemini-1-5-pro": [72, 68, 99, 88, 80, 80],
            "llama-3-70b":    [70, 96, 40, 78, 75, 70],
            "mistral-large":  [75, 65, 62, 82, 78, 76],
            "gpt-3-5-turbo":  [90, 88, 50, 65, 68, 72],
        }
        sa = model_scores.get(model_a_id, [70]*6)
        sb = model_scores.get(model_b_id, [70]*6)

        fig = go.Figure()
        for scores, name, color in [(sa, model_a["name"], "#4F7EFF"), (sb, model_b["name"], "#7C5CFC")]:
            fig.add_trace(go.Scatterpolar(
                r=scores + [scores[0]], theta=categories + [categories[0]],
                fill="toself", name=name,
                line=dict(color=color, width=2),
                fillcolor=color.replace("#", "rgba(") + ",0.12)" if "#" in color else color,
            ))
        t = chart_theme()
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0,100],
                                       gridcolor=t["grid_color"],
                                       linecolor=t["line_color"],
                                       tickfont=dict(color=t["font_color"])),
                       angularaxis=dict(gridcolor=t["grid_color"],
                                        linecolor=t["line_color"],
                                        tickfont=dict(color=t["font_color"]))),
            paper_bgcolor=t["paper_bg"], plot_bgcolor=t["plot_bg"],
            font=dict(color=t["font_color"], family="DM Sans"),
            height=380, showlegend=True,
            legend=dict(bgcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with tabs[2]:
        # Usage aggregated by model
        model_totals = {}
        for uc in data["use_cases"]:
            m = uc["model"]
            model_totals[m] = model_totals.get(m, 0) + uc["usage_count"]

        model_names = {m["id"]: m["name"] for m in data["models"]}
        df_mod = pd.DataFrame({
            "Model": [model_names.get(k,k) for k in model_totals.keys()],
            "API Calls": list(model_totals.values()),
        }).sort_values("API Calls", ascending=True)

        fig = px.bar(df_mod, x="API Calls", y="Model", orientation="h",
                     title="Total API Calls by Model",
                     color="API Calls", color_continuous_scale=["#4F7EFF","#7C5CFC"])
        style_fig(fig, 320)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
#  PAGE: ANALYTICS
# ─────────────────────────────────────────────
def render_analytics():
    data  = st.session_state.data

    st.markdown('<div class="section-header">📈 Usage Analytics</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Aggregate usage trends across all use cases and models.</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Usage Trends", "Use Case Breakdown", "Peak Hours Heatmap"])

    with tabs[0]:
        # Multi-line usage trends
        dates = data["dates"]
        period = st.select_slider("Time Range", ["7 days","14 days","30 days","60 days","90 days"],
                                  value="30 days", key="analytics_period")
        n_days = int(period.split()[0])

        df_lines = pd.DataFrame({"Date": dates[-n_days:]})
        for uc in data["use_cases"]:
            df_lines[uc["name"]] = data["usage_series"][uc["id"]][-n_days:]

        uc_cols = [c for c in df_lines.columns if c != "Date"]
        fig = px.line(df_lines, x="Date", y=uc_cols,
                      title=f"Daily API Calls by Use Case — Last {n_days} Days")
        style_fig(fig, 380)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with tabs[1]:
        # Bar chart of total usage per use case
        uc_summary = sorted(data["use_cases"], key=lambda x: x["usage_count"], reverse=True)
        df_bar = pd.DataFrame({
            "Use Case": [u["name"] for u in uc_summary],
            "API Calls": [u["usage_count"] for u in uc_summary],
            "Business Unit": [u["business_unit"] for u in uc_summary],
        })
        fig = px.bar(df_bar, x="Use Case", y="API Calls", color="Business Unit",
                     title="Total API Calls by Use Case",
                     color_discrete_sequence=["#4F7EFF","#7C5CFC","#2ECC71","#F39C12"])
        fig.update_layout(xaxis_tickangle=-30)
        style_fig(fig, 380)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with tabs[2]:
        # Simulated hourly usage heatmap
        np.random.seed(0)
        hours    = list(range(24))
        weekdays = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
        heatmap  = np.random.poisson(lam=np.outer(
            np.array([1.2,1.4,1.3,1.4,1.3,0.5,0.4]),
            np.array([0.1,0.05,0.05,0.05,0.1,0.3,0.6,1.0,1.4,1.6,1.5,1.4,1.2,1.3,1.4,1.5,1.4,1.2,0.9,0.7,0.5,0.4,0.3,0.2]) * 50
        )).astype(int)

        fig = go.Figure(go.Heatmap(
            z=heatmap, x=[f"{h:02d}:00" for h in hours], y=weekdays,
            colorscale=[[0,"rgba(79,126,255,0.05)"],[0.5,"rgba(79,126,255,0.5)"],[1,"#4F7EFF"]],
            showscale=True, colorbar=dict(title="Calls", tickfont=dict(color=chart_theme()["font_color"])),
        ))
        t = chart_theme()
        fig.update_layout(
            title="Peak Usage Heatmap (Hour × Weekday)",
            paper_bgcolor=t["paper_bg"], plot_bgcolor=t["plot_bg"],
            font=dict(color=t["font_color"], family="DM Sans"),
            height=320, margin=dict(l=10,r=10,t=40,b=10),
            xaxis=dict(tickfont=dict(size=9)), yaxis=dict(tickfont=dict(size=9)),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.caption("Data represents simulated hourly call distribution across a week.")

# ─────────────────────────────────────────────
#  PAGE: COST TRACKING
# ─────────────────────────────────────────────
def render_cost_tracking():
    data = st.session_state.data

    st.markdown('<div class="section-header">💰 Cost Tracking</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Monitor and forecast AI spend across use cases, models, and business units.</div>', unsafe_allow_html=True)

    total_cost  = sum(u["monthly_cost"] for u in data["use_cases"])
    budget_limit = 2000.0
    budget_pct  = (total_cost / budget_limit) * 100

    # Budget overview
    bc1, bc2, bc3, bc4 = st.columns(4)
    with bc1: st.markdown(metric_card("Monthly Spend (MTD)", f"${total_cost:,.2f}", "8.1% vs last month", False), unsafe_allow_html=True)
    with bc2: st.markdown(metric_card("Monthly Budget", f"${budget_limit:,.0f}", "Set by platform admin"), unsafe_allow_html=True)
    with bc3: st.markdown(metric_card("Budget Used", f"{budget_pct:.1f}%", f"${budget_limit-total_cost:,.0f} remaining"), unsafe_allow_html=True)
    with bc4: st.markdown(metric_card("Projected Month-End", f"${total_cost*1.15:,.2f}", "+15% pace"), unsafe_allow_html=True)

    st.progress(min(budget_pct / 100, 1.0), text=f"Budget: ${total_cost:,.2f} / ${budget_limit:,.0f} ({budget_pct:.1f}%)")
    st.markdown("<br>", unsafe_allow_html=True)

    tabs = st.tabs(["By Use Case", "By Model", "By Business Unit", "Cost Trend"])

    with tabs[0]:
        df_uc = pd.DataFrame({
            "Use Case": [u["name"] for u in data["use_cases"]],
            "Monthly Cost ($)": [u["monthly_cost"] for u in data["use_cases"]],
            "API Calls": [u["usage_count"] for u in data["use_cases"]],
            "Cost/Call ($)": [round(u["monthly_cost"] / max(u["usage_count"],1), 4) for u in data["use_cases"]],
            "Business Unit": [u["business_unit"] for u in data["use_cases"]],
            "Status": [u["status"] for u in data["use_cases"]],
        }).sort_values("Monthly Cost ($)", ascending=False)

        fig = px.bar(df_uc, x="Use Case", y="Monthly Cost ($)", color="Business Unit",
                     title="Monthly Cost by Use Case",
                     color_discrete_sequence=["#4F7EFF","#7C5CFC","#2ECC71","#F39C12","#E74C3C"])
        fig.update_layout(xaxis_tickangle=-30)
        style_fig(fig, 300)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        st.dataframe(df_uc, use_container_width=True, hide_index=True)

    with tabs[1]:
        model_names = {m["id"]: m["name"] for m in data["models"]}
        model_costs = {}
        for uc in data["use_cases"]:
            m = uc["model"]
            model_costs[m] = model_costs.get(m, 0) + uc["monthly_cost"]

        df_model = pd.DataFrame({
            "Model": [model_names.get(k,k) for k in model_costs.keys()],
            "Cost ($)": list(model_costs.values()),
        }).sort_values("Cost ($)", ascending=False)

        fig2 = px.pie(df_model, names="Model", values="Cost ($)", title="Cost Distribution by Model",
                      color_discrete_sequence=["#4F7EFF","#7C5CFC","#2ECC71","#F39C12","#E74C3C","#1ABC9C","#3498DB","#9B59B6"])
        fig2.update_traces(textinfo="label+percent", hole=0.5)
        style_fig(fig2, 320)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    with tabs[2]:
        unit_costs = {}
        for uc in data["use_cases"]:
            unit_costs[uc["business_unit"]] = unit_costs.get(uc["business_unit"], 0) + uc["monthly_cost"]

        df_unit = pd.DataFrame({"Business Unit": list(unit_costs.keys()), "Cost ($)": list(unit_costs.values())})
        fig3 = px.bar(df_unit, x="Business Unit", y="Cost ($)", title="Monthly Cost by Business Unit",
                      color="Cost ($)", color_continuous_scale=["#4F7EFF","#7C5CFC"])
        style_fig(fig3, 300)
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

    with tabs[3]:
        # Cost trend over 30 days
        dates = data["dates"][-30:]
        daily_costs = np.zeros(30)
        for uc in data["use_cases"]:
            daily_costs += np.array(data["cost_series"][uc["id"]][-30:])

        cumulative = np.cumsum(daily_costs)
        df_trend = pd.DataFrame({"Date": dates, "Daily Cost ($)": daily_costs, "Cumulative ($)": cumulative})

        fig4 = make_subplots(specs=[[{"secondary_y": True}]])
        fig4.add_trace(go.Bar(x=df_trend["Date"], y=df_trend["Daily Cost ($)"],
                               name="Daily Cost", marker_color="rgba(79,126,255,0.6)"), secondary_y=False)
        fig4.add_trace(go.Scatter(x=df_trend["Date"], y=df_trend["Cumulative ($)"],
                                   name="Cumulative", line=dict(color="#F39C12", width=2)), secondary_y=True)
        t = chart_theme()
        fig4.update_layout(paper_bgcolor=t["paper_bg"], plot_bgcolor=t["plot_bg"],
                           font=dict(color=t["font_color"], family="DM Sans"),
                           height=300, margin=dict(l=10,r=10,t=30,b=10),
                           title="Daily vs Cumulative Cost — Last 30 Days",
                           legend=dict(bgcolor="rgba(0,0,0,0)"),
                           xaxis=dict(gridcolor=t["grid_color"]),
                           yaxis=dict(gridcolor=t["grid_color"]))
        st.plotly_chart(fig4, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
#  PAGE: PERFORMANCE
# ─────────────────────────────────────────────
def render_performance():
    data = st.session_state.data

    st.markdown('<div class="section-header">⚡ Performance Monitoring</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Response times, success rates, and error tracking across the platform.</div>', unsafe_allow_html=True)

    # Overall performance metrics
    all_ucs  = data["use_cases"]
    avg_resp = np.mean([u["avg_response_ms"] for u in all_ucs])
    avg_succ = np.mean([u["success_rate"] for u in all_ucs])

    pc1, pc2, pc3, pc4 = st.columns(4)
    with pc1: st.markdown(metric_card("Avg Response Time", f"{avg_resp:.0f}ms", "platform-wide"), unsafe_allow_html=True)
    with pc2: st.markdown(metric_card("Platform Success Rate", f"{avg_succ:.1f}%", "30-day avg"), unsafe_allow_html=True)
    with pc3: st.markdown(metric_card("Error Rate", f"{100-avg_succ:.1f}%", "30-day avg"), unsafe_allow_html=True)
    with pc4: st.markdown(metric_card("P95 Latency", f"{avg_resp*2.2:.0f}ms", "estimated"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    tabs = st.tabs(["Response Times", "Success Rates", "Error Analysis"])

    with tabs[0]:
        df_resp = pd.DataFrame({
            "Use Case": [u["name"] for u in all_ucs],
            "Avg Response (ms)": [u["avg_response_ms"] for u in all_ucs],
            "P95 (ms)": [u["avg_response_ms"] * random.uniform(1.8, 2.5) for u in all_ucs],
        }).sort_values("Avg Response (ms)")

        fig = px.bar(df_resp, y="Use Case", x=["Avg Response (ms)","P95 (ms)"],
                     orientation="h", barmode="group",
                     title="Response Time by Use Case",
                     color_discrete_sequence=["#4F7EFF","#7C5CFC"])
        style_fig(fig, 380)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with tabs[1]:
        df_succ = pd.DataFrame({
            "Use Case": [u["name"] for u in all_ucs],
            "Success Rate (%)": [u["success_rate"] for u in all_ucs],
            "Business Unit": [u["business_unit"] for u in all_ucs],
        }).sort_values("Success Rate (%)")

        fig2 = px.bar(df_succ, x="Success Rate (%)", y="Use Case", orientation="h",
                      color="Success Rate (%)", title="Success Rate by Use Case",
                      color_continuous_scale=["#E74C3C","#F39C12","#2ECC71"],
                      range_color=[88, 100])
        style_fig(fig2, 380)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    with tabs[2]:
        st.markdown("**Simulated Error Breakdown (Last 30 Days)**")
        error_types = ["Timeout", "Rate Limit", "Invalid Format", "Content Filter", "Context Overflow", "Other"]
        error_counts = [12, 28, 8, 5, 3, 4]

        fig3 = px.pie(names=error_types, values=error_counts, title="Error Type Distribution",
                      hole=0.5, color_discrete_sequence=["#E74C3C","#F39C12","#4F7EFF","#7C5CFC","#2ECC71","#1ABC9C"])
        fig3.update_traces(textinfo="label+percent")
        style_fig(fig3, 320)
        st.plotly_chart(fig3, use_container_width=True, config={"displayModeBar": False})

# ─────────────────────────────────────────────
#  PAGE: ACTIVITY LOG
# ─────────────────────────────────────────────
def render_activity_log():
    data = st.session_state.data

    st.markdown('<div class="section-header">📋 Activity Log & Audit Trail</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Complete record of all actions, changes, and access events.</div>', unsafe_allow_html=True)

    tabs = st.tabs(["All Activity", "Audit Trail", "User Access Log"])

    with tabs[0]:
        # Simulate rich activity
        activities = []
        actions_pool = [
            ("API Call", "Successful inference", "#2ECC71"),
            ("API Call", "Response timeout", "#E74C3C"),
            ("Config Change", "Parameters updated", "#F39C12"),
            ("Access Event", "New user granted access", "#4F7EFF"),
            ("Model Change", "Model switched", "#7C5CFC"),
            ("Status Change", "Use case activated", "#2ECC71"),
        ]
        np.random.seed(1)
        users_list = list(data["users"].keys())
        ucs_list = data["use_cases"]
        for i in range(50):
            action, detail, color = random.choice(actions_pool)
            uc = random.choice(ucs_list)
            user = random.choice(users_list)
            activities.append({
                "Timestamp": (datetime.now() - timedelta(hours=i*0.5)).strftime("%b %d %H:%M"),
                "User": data["users"][user]["name"],
                "Action": action,
                "Detail": detail,
                "Use Case": uc["name"],
            })

        df_act = pd.DataFrame(activities)
        st.dataframe(df_act, use_container_width=True, hide_index=True, height=400)

    with tabs[1]:
        st.markdown("**Platform Audit Trail** — All configuration changes")
        for a in data["audit"]:
            actor_name = data["users"].get(a["actor"], {}).get("name", a["actor"])
            uc = next((u for u in data["use_cases"] if u["id"] == a["uc_id"]), {})
            st.markdown(f"""
            <div class="activity-item">
                <span class="activity-time">{a['timestamp'].strftime('%b %d %H:%M')}</span>
                <span class="activity-text">
                    <strong>{a['action']}</strong>: {a['detail']}
                    <span style="color:var(--text2);"> · {uc.get('name', a['uc_id'])} · by {actor_name}</span>
                </span>
            </div>
            """, unsafe_allow_html=True)

    with tabs[2]:
        st.markdown("**User Access Log** — Who accessed what")
        access_log = []
        for i in range(30):
            uc = random.choice(data["use_cases"])
            user = random.choice(list(data["users"].keys()))
            access_log.append({
                "Timestamp": (datetime.now() - timedelta(hours=i*0.8)).strftime("%b %d %H:%M"),
                "User": data["users"][user]["name"],
                "Use Case": uc["name"],
                "Action": random.choice(["Executed", "Viewed", "Configured"]),
                "Tokens Used": random.randint(100, 4000),
                "Response (ms)": random.randint(300, 4000),
                "Status": random.choice(["✅ Success","✅ Success","✅ Success","❌ Error"]),
            })
        st.dataframe(pd.DataFrame(access_log), use_container_width=True, hide_index=True, height=350)

# ─────────────────────────────────────────────
#  PAGE: USER FEEDBACK
# ─────────────────────────────────────────────
def render_feedback():
    data = st.session_state.data

    st.markdown('<div class="section-header">👥 User Feedback</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Ratings and comments from end users across all use cases.</div>', unsafe_allow_html=True)

    fb = data["feedback"]
    avg_rating = np.mean([f["rating"] for f in fb])
    pos = sum(1 for f in fb if f["sentiment"] == "positive")
    neg = sum(1 for f in fb if f["sentiment"] == "negative")

    fc1, fc2, fc3, fc4 = st.columns(4)
    with fc1: st.markdown(metric_card("Avg Rating", f"⭐ {avg_rating:.1f}/5", f"{len(fb)} responses"), unsafe_allow_html=True)
    with fc2: st.markdown(metric_card("Positive", f"{pos}", f"{pos/len(fb)*100:.0f}%"), unsafe_allow_html=True)
    with fc3: st.markdown(metric_card("Neutral", str(sum(1 for f in fb if f["sentiment"]=="neutral")), ""), unsafe_allow_html=True)
    with fc4: st.markdown(metric_card("Negative", f"{neg}", f"{neg/len(fb)*100:.0f}%"), unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Rating distribution
    fc_l, fc_r = st.columns(2)
    with fc_l:
        rating_dist = pd.Series([f["rating"] for f in fb]).value_counts().sort_index()
        fig = px.bar(x=rating_dist.index, y=rating_dist.values,
                     title="Rating Distribution",
                     labels={"x": "Stars", "y": "Count"},
                     color=rating_dist.values,
                     color_continuous_scale=["#E74C3C","#F39C12","#F39C12","#2ECC71","#2ECC71"])
        style_fig(fig, 240)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with fc_r:
        sent_dist = pd.Series([f["sentiment"] for f in fb]).value_counts()
        fig2 = px.pie(names=sent_dist.index, values=sent_dist.values,
                      title="Sentiment Distribution", hole=0.55,
                      color_discrete_sequence=["#2ECC71","#F39C12","#E74C3C"])
        fig2.update_traces(textinfo="label+percent")
        style_fig(fig2, 240)
        st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    # Recent feedback
    st.markdown("---")
    st.markdown("**Recent Feedback**")
    for f in sorted(fb, key=lambda x: x["time"], reverse=True)[:8]:
        stars = "⭐" * f["rating"]
        sent_color = {"positive": "var(--green)","neutral": "var(--orange)","negative": "var(--red)"}.get(f["sentiment"],"var(--text2)")
        st.markdown(f"""
        <div class="uc-card" style="padding:0.8rem 1rem;">
            <div style="display:flex;justify-content:space-between;">
                <div style="font-size:0.82rem;font-weight:600;color:var(--text);">{f['uc_name']}</div>
                <div style="font-size:0.78rem;color:var(--text2);">{f['time'].strftime('%b %d')}</div>
            </div>
            <div style="margin:0.3rem 0;font-size:0.88rem;">{stars} <span style="color:{sent_color};font-size:0.75rem;font-weight:600;margin-left:0.3rem;">{f['sentiment'].upper()}</span></div>
            <div style="font-size:0.84rem;color:var(--text2);font-style:italic;">"{f['comment']}"</div>
        </div>
        """, unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  PAGE: NOTIFICATIONS
# ─────────────────────────────────────────────
def render_notifications():
    data = st.session_state.data

    st.markdown('<div class="section-header">🔔 Notification Center</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Alerts, warnings, and system updates.</div>', unsafe_allow_html=True)

    col_l, col_r = st.columns([4, 1])
    with col_r:
        if st.button("Mark All Read", use_container_width=True):
            for n in data["notifications"]:
                n["read"] = True
            st.rerun()

    for n in data["notifications"]:
        cls = {"warn": "notif-warn", "error": "notif-error", "success": "notif-success"}.get(n["type"], "")
        icon = {"warn": "⚠️", "error": "🚨", "info": "ℹ️", "success": "✅"}.get(n["type"], "📢")
        read_style = "opacity:0.6;" if n["read"] else ""
        st.markdown(f"""
        <div class="notif-item {cls}" style="{read_style}">
            <div style="display:flex;justify-content:space-between;align-items:flex-start;">
                <div>{icon} <strong>{n['title']}</strong></div>
                <span style="color:var(--text2);font-size:0.72rem;">{n['time'].strftime('%b %d, %H:%M')} {'· read' if n['read'] else '<strong style="color:var(--accent);">· NEW</strong>'}</span>
            </div>
            <div style="margin-top:0.3rem;font-size:0.84rem;color:var(--text2);">{n['msg']}</div>
        </div>
        """, unsafe_allow_html=True)

        if not n["read"]:
            if st.button(f"Mark as read", key=f"read_{n['id']}", use_container_width=False):
                n["read"] = True
                st.rerun()

# ─────────────────────────────────────────────
#  PAGE: SETTINGS
# ─────────────────────────────────────────────
def render_settings():
    data  = st.session_state.data
    email = st.session_state.current_user
    user  = data["users"][email]

    st.markdown('<div class="section-header">⚙️ Settings & Configuration</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Appearance", "Notifications", "API Keys", "Integrations", "Profile"])

    with tabs[0]:
        st.markdown("**Theme**")
        dark = st.toggle("Dark Mode", value=st.session_state.dark_mode)
        if dark != st.session_state.dark_mode:
            st.session_state.dark_mode = dark
            st.rerun()
        st.info("Changes apply immediately across the platform.")

    with tabs[1]:
        st.markdown("**Notification Preferences**")
        c1, c2 = st.columns(2)
        with c1:
            st.toggle("Budget threshold alerts", value=True)
            st.toggle("Model deprecation warnings", value=True)
            st.toggle("Access request notifications", value=True)
            st.toggle("Unusual usage spike alerts", value=True)
        with c2:
            st.toggle("Weekly usage digest email", value=False)
            st.toggle("New model availability", value=True)
            st.toggle("Platform maintenance notices", value=True)
            st.toggle("A/B test completion alerts", value=True)

        st.markdown("**Alert Thresholds**")
        st.slider("Budget alert at (%)", 50, 95, 80)
        st.slider("Usage spike threshold (× normal)", 1.5, 10.0, 3.0, 0.5)
        st.number_input("Error rate alert threshold (%)", 0.0, 100.0, 5.0, 0.5)

    with tabs[2]:
        st.markdown("**API Key Management**")
        st.info("Keys are encrypted at rest and never exposed in plaintext.")
        keys = [
            ("OpenAI", "sk-•••••••••••••••••••••••••••••••••••••Xj9K", "Active", "Jul 15, 2025"),
            ("Anthropic", "sk-ant-•••••••••••••••••••••••••••••••••Yw3M", "Active", "Dec 31, 2025"),
            ("Google AI", "AIza•••••••••••••••••••••••••••••••••••9pQL", "Active", "Perpetual"),
            ("Mistral AI", "ms-•••••••••••••••••••••••••••••••••••••4xRN", "Active", "Sep 30, 2025"),
        ]
        for provider, masked, status, expiry in keys:
            kc1, kc2, kc3, kc4 = st.columns([2, 4, 1.5, 1])
            with kc1: st.markdown(f"**{provider}**")
            with kc2: st.code(masked, language=None)
            with kc3: st.markdown(f'<span class="badge badge-active">{status}</span><br><span style="font-size:0.72rem;color:var(--text2);">Exp: {expiry}</span>', unsafe_allow_html=True)
            with kc4: st.button("Rotate", key=f"rotate_{provider}", use_container_width=True)
            st.markdown('<hr style="margin:0.3rem 0;">', unsafe_allow_html=True)

        st.markdown("**Add New API Key**")
        nkc1, nkc2, nkc3 = st.columns([2, 4, 1])
        with nkc1: new_provider = st.text_input("Provider", placeholder="e.g. Cohere", label_visibility="collapsed")
        with nkc2: new_key = st.text_input("API Key", placeholder="Paste key here (will be masked)", type="password", label_visibility="collapsed")
        with nkc3:
            if st.button("Save Key", use_container_width=True):
                if new_provider and new_key:
                    st.success(f"Key for {new_provider} saved securely!")

    with tabs[3]:
        st.markdown("**Integration Settings**")
        integrations = [
            ("Slack", "🟢", "Connected to #ai-alerts channel", "Disconnect"),
            ("Microsoft Teams", "⚪", "Not connected", "Connect"),
            ("Email (SMTP)", "🟢", "Configured for automated reports", "Edit"),
            ("PagerDuty", "⚪", "Not connected", "Connect"),
            ("Datadog", "🟡", "Partially configured — missing API key", "Configure"),
        ]
        for name, dot, status_text, action in integrations:
            ic1, ic2, ic3 = st.columns([2, 4, 1.5])
            with ic1: st.markdown(f"**{name}**")
            with ic2: st.markdown(f"{dot} _{status_text}_")
            with ic3: st.button(action, key=f"int_{name}", use_container_width=True)
            st.markdown('<hr style="margin:0.3rem 0;">', unsafe_allow_html=True)

    with tabs[4]:
        st.markdown("**Profile Information**")
        c1, c2 = st.columns(2)
        with c1:
            st.text_input("Full Name", value=user["name"])
            st.text_input("Email", value=email, disabled=True)
            st.text_input("Business Unit", value=user["unit"])
        with c2:
            st.text_input("Role", value=user["role"], disabled=True)
            st.text_input("Department", value=user["unit"])
            st.text_area("Bio", placeholder="Add a short bio…", height=100)
        if st.button("Save Profile"):
            st.success("Profile updated!")

# ─────────────────────────────────────────────
#  PAGE: ADMIN PANEL
# ─────────────────────────────────────────────
def render_admin():
    data = st.session_state.data

    st.markdown('<div class="section-header">🛡️ Admin Panel</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-sub">Platform-wide management, user administration, and system health.</div>', unsafe_allow_html=True)

    tabs = st.tabs(["Users", "Platform Health", "Budget Controls", "Documentation Hub"])

    with tabs[0]:
        st.markdown("**User Management**")
        user_rows = []
        for email, u in data["users"].items():
            uc_count = sum(1 for uc in data["use_cases"] if uc["owner"] == email)
            user_rows.append({"Email": email, "Name": u["name"], "Role": u["role"],
                               "Unit": u["unit"], "Owned Use Cases": uc_count})
        st.dataframe(pd.DataFrame(user_rows), use_container_width=True, hide_index=True)

        st.markdown("---")
        st.markdown("**Add New User**")
        uc1, uc2, uc3, uc4 = st.columns(4)
        with uc1: st.text_input("Email", placeholder="user@company.com", key="new_user_email")
        with uc2: st.text_input("Full Name", placeholder="First Last", key="new_user_name")
        with uc3: st.selectbox("Role", ["Use Case Owner","AI Team Member","Admin"], key="new_user_role")
        with uc4:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("Add User", use_container_width=True):
                st.success("User invited!")

    with tabs[1]:
        st.markdown("**System Health**")
        health_items = [
            ("API Gateway", "🟢 Operational", "99.99% uptime"),
            ("Model Proxy Layer", "🟢 Operational", "Latency P50: 820ms"),
            ("Auth Service", "🟢 Operational", "0 incidents last 7d"),
            ("Audit Log Storage", "🟡 Warning", "Disk at 78% — cleanup scheduled"),
            ("Cost Tracking DB", "🟢 Operational", "Last synced 2 min ago"),
        ]
        for svc, status, detail in health_items:
            sc1, sc2, sc3 = st.columns([2, 2, 3])
            with sc1: st.markdown(f"**{svc}**")
            with sc2: st.markdown(status)
            with sc3: st.markdown(f"_{detail}_")
            st.markdown('<hr style="margin:0.3rem 0;">', unsafe_allow_html=True)

    with tabs[2]:
        st.markdown("**Budget Controls**")
        overall_budget = st.number_input("Platform Monthly Budget ($)", value=2000.0, step=100.0)

        st.markdown("**Per Business Unit Budgets**")
        for unit in ["Marketing", "Operations", "Finance"]:
            uc1, uc2, uc3 = st.columns([2, 3, 1])
            with uc1: st.markdown(f"**{unit}**")
            with uc2: st.slider(f"Budget for {unit}", 0, 1000, 600 if unit=="Marketing" else 400, 50, key=f"budget_{unit}", label_visibility="collapsed")
            with uc3: st.markdown(f"${'600' if unit=='Marketing' else '400'}/mo")

        if st.button("Save Budget Controls"):
            st.success("Budget limits updated!")

    with tabs[3]:
        st.markdown("**Documentation Hub**")
        docs = [
            ("OpenAI API Reference", "https://platform.openai.com/docs", "Official API docs for GPT-4 and related models."),
            ("Anthropic Claude Docs", "https://docs.anthropic.com", "Documentation for Claude model family."),
            ("Google Gemini API", "https://ai.google.dev/docs", "Gemini model API and usage guides."),
            ("Prompt Engineering Guide", "https://platform.openai.com/docs/guides/prompt-engineering", "Best practices for prompt design."),
            ("Token Counting Reference", "https://platform.openai.com/tokenizer", "Understand and estimate token usage."),
            ("AI Safety Guidelines", "#", "Internal safety and content policy documentation."),
        ]
        for title, url, desc in docs:
            dc1, dc2 = st.columns([3, 1])
            with dc1:
                st.markdown(f"**[{title}]({url})**")
                st.caption(desc)
            with dc2:
                st.link_button("Open →", url, use_container_width=True)
            st.markdown('<hr style="margin:0.3rem 0;">', unsafe_allow_html=True)

# ─────────────────────────────────────────────
#  MAIN ROUTER
# ─────────────────────────────────────────────
def main():
    init_session()
    inject_css()

    if not st.session_state.logged_in:
        render_login()
        return

    render_sidebar()

    page = st.session_state.active_page
    role = st.session_state.data["users"][st.session_state.current_user]["role"]

    if page == "Dashboard":
        render_dashboard()
    elif page == "Use Cases":
        render_use_cases()
    elif page == "Analytics":
        if role in ["AI Team Member", "Admin"]:
            render_analytics()
        else:
            st.error("Access restricted to AI Team Members and Admins.")
    elif page == "Cost Tracking":
        if role in ["AI Team Member", "Admin"]:
            render_cost_tracking()
        else:
            st.error("Access restricted.")
    elif page == "Performance":
        if role in ["AI Team Member", "Admin"]:
            render_performance()
        else:
            st.error("Access restricted.")
    elif page == "Access Control":
        render_access_control()
    elif page == "Models":
        render_models()
    elif page == "Activity Log":
        if role in ["AI Team Member", "Admin"]:
            render_activity_log()
        else:
            st.error("Access restricted.")
    elif page == "User Feedback":
        if role in ["AI Team Member", "Admin"]:
            render_feedback()
        else:
            st.error("Access restricted.")
    elif page == "Notifications":
        render_notifications()
    elif page == "Settings":
        render_settings()
    elif page == "Admin Panel":
        if role == "Admin":
            render_admin()
        else:
            st.error("Admin access required.")
    else:
        render_dashboard()

if __name__ == "__main__":
    main()
