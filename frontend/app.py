import datetime
from typing import Any, Dict, List, Optional
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

import api
from login import show_login
from landing import show_landing


# ============================================================
# 1. APPLICATION CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="RoboPulse AI",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ============================================================
# 2. SESSION STATE & LOGIN GUARD
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if "access_token" not in st.session_state:
    st.session_state["access_token"] = None

if "user_id" not in st.session_state:
    st.session_state["user_id"] = None

if "full_name" not in st.session_state:
    st.session_state["full_name"] = "Operator"

if "email" not in st.session_state:
    st.session_state["email"] = ""

if "role" not in st.session_state:
    st.session_state["role"] = "Operator"


if not st.session_state["logged_in"]:
    show_login()
    st.stop()


# ============================================================
# 3.LIGHT DESIGN SYSTEM & STYLING
# ============================================================

st.markdown(
    """
    <style>
    /* Light Industrial Sans Typography & Pure White Canvas */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        letter-spacing: -0.01em;
    }

    /* Hide Streamlit header anchor link icons completely */
    [data-testid="stHeaderActionElements"],
    .stHeadingWithActionElements a,
    a.header-anchor,
    a[aria-label="Link to this heading"],
    button[aria-label="Copy link to heading"],
    .stHeadingWithActionElements button,
    .stHeadingWithActionElements [data-testid="stHeaderActionElements"],
    a[href^="#"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* Hide Streamlit's accessibility shortcut and heading permalink controls. */
    button[aria-label*="Accessibility"],
    button[title*="Accessibility"],
    [data-testid*="Accessibility"],
    [data-testid="stHeader"] a[href*="#"],
    [data-testid="stMain"] .stHeadingWithActionElements a,
    [data-testid="stMarkdownContainer"] .stHeadingWithActionElements a {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* Hide Streamlit running status icon (the cycling wheelchair/runner widget) and footer/menu */
    [data-testid="stStatusWidget"],
    [data-testid="stStatusWidgetRunningIcon"],
    [data-testid="stStatusWidgetNewYearsIcon"],
    .stStatusWidget,
    div[data-testid="InputInstructions"],
    #MainMenu,
    footer,
    footer[data-testid="stFooter"] {
        display: none !important;
        visibility: hidden !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }

    /* Hide right-aligned toolbar actions (deploy button, etc.) but KEEP sidebar toggle toolbar */
    [data-testid="stToolbarActions"] {
        display: none !important;
    }

    /* Keep header transparent and pass clicks through, except on interactive controls */
    header[data-testid="stHeader"],
    header.stAppHeader {
        background-color: transparent !important;
        pointer-events: none !important;
        z-index: 10000 !important;
    }

    header[data-testid="stHeader"] [data-testid="stToolbar"],
    [data-testid="stToolbar"] {
        background-color: transparent !important;
        pointer-events: auto !important;
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
    }

    /* Expand Sidebar Button (shown when sidebar is collapsed) */
    [data-testid="stExpandSidebarButton"],
    button[data-testid="stExpandSidebarButton"],
    header[data-testid="stHeader"] button[data-testid="stExpandSidebarButton"],
    header[data-testid="stHeader"] [data-testid="stExpandSidebarButton"],
    [data-testid="stSidebarCollapsedControl"],
    [data-testid="stSidebarCollapsedControl"] button {
        display: inline-flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        background-color: #FFFFFF !important;
        border: 1.5px solid #E05C1A !important;
        border-radius: 6px !important;
        color: #E05C1A !important;
        box-shadow: 0 2px 6px rgba(224, 92, 26, 0.25) !important;
        cursor: pointer !important;
        z-index: 999999 !important;
        padding: 4px 8px !important;
        margin-left: 8px !important;
        margin-top: 8px !important;
        transition: all 0.15s ease !important;
    }

    [data-testid="stExpandSidebarButton"]:hover,
    button[data-testid="stExpandSidebarButton"]:hover {
        background-color: #FFF4EC !important;
        border-color: #C04A10 !important;
    }

    [data-testid="stExpandSidebarButton"] svg,
    button[data-testid="stExpandSidebarButton"] svg {
        fill: #E05C1A !important;
        color: #E05C1A !important;
    }

    /* Sidebar Collapse Button inside the sidebar header */
    [data-testid="stSidebarCollapseButton"],
    button[data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarHeader"] [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarHeader"] button {
        display: inline-flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        cursor: pointer !important;
        color: #6A6A6A !important;
    }

    [data-testid="stSidebarCollapseButton"]:hover,
    button[data-testid="stSidebarCollapseButton"]:hover {
        color: #E05C1A !important;
        background-color: #FFF4EC !important;
    }

    /* Invisible iframe for auto-expand helper */
    iframe[title="streamlit.components.v1.html"] {
        position: absolute !important;
        width: 0 !important;
        height: 0 !important;
        border: none !important;
        opacity: 0 !important;
        pointer-events: none !important;
    }
    
    .stApp {
        background-color: #F8F7F4 !important;
        color: #1A1A1A !important;
    }

    /* Top Global Application Header */
    .top-header-bar {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #FFFFFF;
        border-bottom: 1px solid #EEECE8;
        padding: 8px 0px 16px 0px;
        margin-bottom: 20px;
    }
    .top-header-logo {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .top-header-search {
        display: flex;
        align-items: center;
        gap: 10px;
        background: #F2F2F2;
        border: 1px solid #EEECE8;
        border-radius: 20px;
        padding: 7px 16px;
        width: 420px;
    }
    .top-header-search input {
        border: none;
        background: transparent;
        color: #1A1A1A;
        font-size: 13px;
        outline: none;
        width: 100%;
    }
    .top-header-search input::placeholder {
        color: #AAAAAA;
    }
    .top-header-right {
        display: flex;
        align-items: center;
        gap: 18px;
    }
    .header-notif-btn {
        position: relative;
        display: flex;
        align-items: center;
        justify-content: center;
        width: 36px;
        height: 36px;
        border-radius: 50%;
        background: #FFFFFF;
        border: 1px solid #EEECE8;
        cursor: pointer;
    }
    .header-notif-badge {
        position: absolute;
        top: -3px;
        right: -3px;
        background: #E05C1A;
        color: #FFFFFF;
        font-size: 10px;
        font-weight: 700;
        width: 16px;
        height: 16px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .header-user {
        display: flex;
        align-items: center;
        gap: 10px;
    }
    .header-user-avatar {
        width: 34px;
        height: 34px;
        border-radius: 50%;
        background: #4A4A4A;
        color: #FFFFFF;
        font-weight: 600;
        font-size: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    .header-user-name {
        font-size: 13px;
        font-weight: 600;
        color: #1A1A1A;
        line-height: 1.2;
    }
    .header-user-role {
        font-size: 11px;
        color: #6A6A6A;
    }

    /* Sidebar Light Industrial Styling */
    section[data-testid="stSidebar"] {
        background-color: #FAFAF8 !important;
        border-right: 1px solid #EEECE8 !important;
    }

    section[data-testid="stSidebar"] * {
        color: #1A1A1A;
    }

    /* The visible section labels are custom markup, not Streamlit widget labels. */
    section[data-testid="stSidebar"] [data-testid="stRadio"] > label {
        display: none !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] div[role="radiogroup"] {
        gap: 4px !important;
        display: flex !important;
        flex-direction: column !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label {
        background-color: transparent !important;
        border-radius: 6px !important;
        padding: 9px 12px !important;
        border: 1px solid transparent !important;
        border-left: 3px solid transparent !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
        display: flex !important;
        align-items: center !important;
        width: 100% !important;
        color: #3D3D3D !important;
        font-size: 13.5px !important;
        font-weight: 500 !important;
    }

    /* Hide default radio circle */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label > div:first-child,
    section[data-testid="stSidebar"] [data-testid="stRadio"] label[data-baseweb="radio"] > div:first-child {
        display: none !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
        background-color: #FFF4EC !important;
        color: #E05C1A !important;
    }

    /* Selected / Active navigation pill */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        background: #FFF4EC !important;
        border-left: 3px solid #E05C1A !important;
        border-radius: 0 6px 6px 0 !important;
        color: #E05C1A !important;
        font-weight: 600 !important;
        box-shadow: none !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) span {
        color: #E05C1A !important;
        font-weight: 600 !important;
    }

    /* SVG Icons for all 11 Navigation Items (Monochrome #6A6A6A, active #E05C1A) */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[value="Fleet Overview"])::before {
        content: ""; display: inline-block; width: 17px; height: 17px; margin-right: 10px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236A6A6A' stroke-width='2'%3E%3Crect x='3' y='3' width='7' height='7' rx='1'/%3E%3Crect x='14' y='3' width='7' height='7' rx='1'/%3E%3Crect x='3' y='14' width='7' height='7' rx='1'/%3E%3Crect x='14' y='14' width='7' height='7' rx='1'/%3E%3C/svg%3E") no-repeat center;
        background-size: contain;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[value="Robotic Assets"])::before {
        content: ""; display: inline-block; width: 17px; height: 17px; margin-right: 10px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236A6A6A' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z'/%3E%3C/svg%3E") no-repeat center;
        background-size: contain;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[value="Sensor Network"])::before {
        content: ""; display: inline-block; width: 17px; height: 17px; margin-right: 10px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236A6A6A' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M8.111 16.404a5.5 5.5 0 017.778 0M12 20h.01m-7.08-7.071c3.904-3.905 10.236-3.905 14.141 0M1.394 9.393c5.857-5.857 15.355-5.857 21.213 0'/%3E%3C/svg%3E") no-repeat center;
        background-size: contain;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[value="Telemetry and Charts"])::before {
        content: ""; display: inline-block; width: 17px; height: 17px; margin-right: 10px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236A6A6A' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M3 13l4-4 4 6 4-8 6 6'/%3E%3C/svg%3E") no-repeat center;
        background-size: contain;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[value="Predictive Analytics"])::before {
        content: ""; display: inline-block; width: 17px; height: 17px; margin-right: 10px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236A6A6A' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'/%3E%3C/svg%3E") no-repeat center;
        background-size: contain;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[value="Maintenance Scheduler"])::before {
        content: ""; display: inline-block; width: 17px; height: 17px; margin-right: 10px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236A6A6A' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z'/%3E%3C/svg%3E") no-repeat center;
        background-size: contain;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[value="Incident Tracker"])::before {
        content: ""; display: inline-block; width: 17px; height: 17px; margin-right: 10px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236A6A6A' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z'/%3E%3C/svg%3E") no-repeat center;
        background-size: contain;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[value="Notification Center"])::before {
        content: ""; display: inline-block; width: 17px; height: 17px; margin-right: 10px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236A6A6A' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9'/%3E%3C/svg%3E") no-repeat center;
        background-size: contain;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[value="Health Diagnostics"])::before {
        content: ""; display: inline-block; width: 17px; height: 17px; margin-right: 10px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236A6A6A' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z'/%3E%3C/svg%3E") no-repeat center;
        background-size: contain;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[value="User Management"])::before {
        content: ""; display: inline-block; width: 17px; height: 17px; margin-right: 10px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236A6A6A' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M12 4.354a4 4 0 110 5.292M15 21H3v-1a6 6 0 0112 0v1zm0 0h6v-1a6 6 0 00-9-5.197M13 7a4 4 0 11-8 0 4 4 0 018 0z'/%3E%3C/svg%3E") no-repeat center;
        background-size: contain;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input[value="Product Overview"])::before {
        content: ""; display: inline-block; width: 17px; height: 17px; margin-right: 10px;
        background: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 24 24' stroke='%236A6A6A' stroke-width='2'%3E%3Cpath stroke-linecap='round' stroke-linejoin='round' d='M5 3v4M3 5h4M6 17v4m-2-2h4m5-16l2.286 6.857L21 12l-5.714 2.143L13 21l-2.286-6.857L5 12l5.714-2.143L13 3z'/%3E%3C/svg%3E") no-repeat center;
        background-size: contain;
    }
    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked)::before {
        filter: sepia(100%) hue-rotate(345deg) saturate(450%) brightness(85%);
    }

    /* Text-only grouped navigation: suppress every generated navigation icon. */
    section[data-testid="stSidebar"] [data-testid="stRadio"] label::before {
        content: none !important;
        display: none !important;
        background: none !important;
    }

    section[data-testid="stSidebar"] .nav-section-title {
        margin: 18px 12px 6px !important;
        color: #7A7A7A !important;
        font-size: 10px !important;
        font-weight: 700 !important;
        letter-spacing: 0.12em !important;
    }

    section[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked) {
        border-left: 0 !important;
        border-radius: 999px !important;
        padding: 9px 14px !important;
        background: #FFF1E8 !important;
    }

    /* General Typography */
    h1, h2, h3, h4, h5, h6 {
        color: #1A1A1A !important;
        letter-spacing: -0.02em;
    }
    p, span, label, div {
        color: inherit;
    }
    .stMarkdown p {
        color: #1A1A1A;
    }
    .stCaption, small {
        color: #6A6A6A !important;
    }
    hr {
        border-color: #EEECE8 !important;
    }

    /* Main Section Header */
    .main-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.2rem 0 1.2rem 0;
        margin-bottom: 1.2rem;
    }
    .main-title {
        font-size: 22px;
        font-weight: 700;
        color: #1A1A1A !important;
        margin: 0;
        letter-spacing: -0.02em;
        line-height: 1.2;
    }
    .main-subtitle {
        font-size: 13.5px;
        color: #6A6A6A !important;
        margin: 4px 0 0 0;
        font-weight: 400;
    }

    /* Metric Cards (White #FFFFFF, Border #EEECE8, Radius 8px) */
    .metric-box {
        background: #FFFFFF !important;
        border: 1px solid #EEECE8 !important;
        border-radius: 8px;
        padding: 14px 16px;
        min-height: 116px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: all 0.2s cubic-bezier(0.16, 1, 0.3, 1) !important;
        cursor: pointer;
    }
    .metric-box:hover {
        border-color: #E05C1A !important;
        box-shadow: 0 6px 18px rgba(224, 92, 26, 0.12), 0 2px 6px rgba(0, 0, 0, 0.04) !important;
        transform: translateY(-3px) !important;
        background: #FFFDFB !important;
    }
    .metric-box-title-row {
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .metric-box-title {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #1A1A1A !important;
    }
    .metric-box-icon {
        display: flex;
        align-items: center;
        justify-content: center;
        width: 24px;
        height: 24px;
    }
    .metric-box-val {
        font-size: 28px;
        font-weight: 700;
        color: #1A1A1A !important;
        line-height: 1.1;
        margin: 6px 0 2px 0;
        letter-spacing: -0.02em;
    }
    .metric-box-desc {
        font-size: 11.5px;
        color: #6A6A6A !important;
    }
    .metric-trend-badge {
        font-size: 10.5px;
        font-weight: 600;
        padding: 1px 6px;
        border-radius: 4px;
        display: inline-flex;
        align-items: center;
        gap: 2px;
    }

        /* Status Badges */
    .status-badge {
        display: inline-block;
        padding: 3px 8px;
        font-size: 10.5px;
        font-weight: 700;
        border-radius: 4px;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }
    .badge-active { background: #EBF5EE; color: #2E7D4E; border: 1px solid #B8E0C8; }
    .badge-warning { background: #FEF6E9; color: #B26A00; border: 1px solid #F8D8A0; }
    .badge-critical { background: #FDF0EE; color: #C53030; border: 1px solid #F6B8AF; }
    .badge-medium { background: #FFF4EC; color: #E05C1A; border: 1px solid #F4D2B8; }
    .badge-neutral { background: #F8F7F4; color: #6A6A6A; border: 1px solid #E2E0DA; }

    /* Health Diagnosis Banners */
    .risk-banner-safe {
        background: #FFFFFF !important;
        border: 1px solid #B8E0C8 !important;
        border-left: 5px solid #2E7D4E !important;
        border-radius: 8px !important;
        padding: 20px 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }
    .risk-banner-warning {
        background: #FFFFFF !important;
        border: 1px solid #F8D8A0 !important;
        border-left: 5px solid #E05C1A !important;
        border-radius: 8px !important;
        padding: 20px 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }
    .risk-banner-critical {
        background: #FFFFFF !important;
        border: 1px solid #F6B8AF !important;
        border-left: 5px solid #C53030 !important;
        border-radius: 8px !important;
        padding: 20px 24px !important;
        margin-bottom: 20px !important;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
    }

    /* Robotic Asset Cards */
    .robot-card {
        background: #FFFFFF !important;
        border: 1px solid #EEECE8 !important;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 14px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .robot-card:hover {
        border-color: #E05C1A !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
    }

    /* Progress bar track (6px fully rounded) */
    .risk-progress-track {
        width: 100%;
        height: 6px;
        background: #F0EEEA;
        border-radius: 3px;
        overflow: hidden;
        margin-top: 8px;
    }
    .risk-progress-fill {
        height: 100%;
        border-radius: 3px;
    }

    /* High-Risk Prediction Item */
    .prediction-card {
        background: #FFFFFF !important;
        border: 1px solid #EEECE8 !important;
        border-radius: 8px;
        padding: 12px 14px;
        margin-bottom: 10px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04);
        transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .prediction-card:hover {
        border-color: #E05C1A !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
    }

    /* Risk Banners */
    .risk-banner-critical {
        background: rgba(217, 64, 64, 0.08) !important;
        border: 1px solid rgba(217, 64, 64, 0.25) !important;
        border-left: 4px solid #D94040 !important;
        border-radius: 6px;
        padding: 16px 20px;
        color: #1A1A1A !important;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }
    .risk-banner-safe {
        background: rgba(74, 155, 111, 0.08) !important;
        border: 1px solid rgba(74, 155, 111, 0.25) !important;
        border-left: 4px solid #4A9B6F !important;
        border-radius: 6px;
        padding: 16px 20px;
        color: #1A1A1A !important;
        margin-bottom: 16px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
    }

    /* Section Subheadings */
    .section-header-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin: 1.2rem 0 0.8rem 0;
    }
    .section-header {
        font-size: 15px;
        font-weight: 700;
        color: #1A1A1A !important;
        letter-spacing: -0.01em;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .section-header-bar {
        width: 3px;
        height: 15px;
        background: #E05C1A;
        border-radius: 2px;
        display: inline-block;
    }
    .section-view-all {
        font-size: 12px;
        font-weight: 600;
        color: #E05C1A !important;
        text-decoration: none;
        cursor: pointer;
    }

    /* Inputs, Selectboxes, and Forms */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid #EEECE8 !important;
        border-radius: 6px !important;
        font-size: 13.5px !important;
    }
    .stTextInput > div > div > input:focus,
    .stSelectbox > div > div > div:focus-within {
        border-color: #E05C1A !important;
        box-shadow: 0 0 0 2px rgba(224, 92, 26, 0.15) !important;
    }
    .stTextInput label, .stSelectbox label, .stNumberInput label, .stTextArea label, .stSlider label {
        color: #1A1A1A !important;
        font-weight: 500 !important;
        font-size: 13px !important;
    }

    /* Buttons (Light Industrial Orange) */
    .stButton > button, .stFormSubmitButton > button {
        background-color: #E05C1A !important;
        color: #FFFFFF !important;
        border: 1px solid #E05C1A !important;
        border-radius: 6px !important;
        font-size: 13.5px !important;
        font-weight: 600 !important;
        padding: 8px 18px !important;
        box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04) !important;
        transition: all 0.15s ease !important;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background-color: #C84E12 !important;
        border-color: #C84E12 !important;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08) !important;
    }

    /* Secondary Buttons */
    button[kind="secondary"], button[data-testid="baseButton-secondary"] {
        background-color: #FFFFFF !important;
        color: #1A1A1A !important;
        border: 1px solid #EEECE8 !important;
        border-radius: 6px !important;
        font-weight: 500 !important;
    }
    button[kind="secondary"]:hover, button[data-testid="baseButton-secondary"]:hover {
        background-color: #FFF4EC !important;
        border-color: #E05C1A !important;
        color: #E05C1A !important;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 6px;
        background-color: #FFFFFF !important;
        padding: 4px;
        border-radius: 6px;
        border: 1px solid #EEECE8 !important;
        margin-bottom: 18px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 4px;
        padding: 6px 14px;
        font-weight: 500;
        font-size: 13px;
        color: #6A6A6A !important;
        background-color: transparent !important;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #FFF4EC !important;
        color: #E05C1A !important;
        border: 1px solid rgba(224, 92, 26, 0.25) !important;
        font-weight: 600 !important;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #FFFFFF !important;
        border: 1px solid #EEECE8 !important;
        border-radius: 6px !important;
        font-weight: 600 !important;
        color: #1A1A1A !important;
        font-size: 13.5px !important;
    }
    .streamlit-expanderContent {
        background-color: #FFFFFF !important;
        border: 1px solid #EEECE8 !important;
        border-top: none !important;
        border-bottom-left-radius: 6px !important;
        border-bottom-right-radius: 6px !important;
        padding: 16px !important;
    }

    /* Dataframe wrapper */
    [data-testid="stDataFrame"] {
        background: #FFFFFF !important;
        border: 1px solid #EEECE8 !important;
        border-radius: 6px !important;
        padding: 4px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03) !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. SIDEBAR NAVIGATION
# ============================================================


# Automatically restore / expand the sidebar if collapsed in user's browser session
st.html(
    """
    <script>
    function expandSidebarIfNeeded() {
        try {
            const pDoc = window.parent.document;
            const expandBtn = pDoc.querySelector('[data-testid="stExpandSidebarButton"]') || 
                              pDoc.querySelector('[data-testid="stSidebarCollapsedControl"] button');
            if (expandBtn) {
                expandBtn.click();
            }
        } catch(e) {}
    }
    expandSidebarIfNeeded();
    setTimeout(expandSidebarIfNeeded, 100);
    setTimeout(expandSidebarIfNeeded, 300);
    setTimeout(expandSidebarIfNeeded, 600);
    </script>
    """,
)

with st.sidebar:
    # Top Branding Header
    st.markdown(
        """
        <div style="display: flex; align-items: center; gap: 10px; padding: 10px 4px 16px 4px; margin-bottom: 8px; border-bottom: 1px solid #EEECE8;">
            <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
                <rect width="28" height="28" rx="6" fill="#E05C1A"/>
                <circle cx="14" cy="14" r="5" fill="#FFFFFF"/>
                <path d="M14 4v4m0 12v4m-10-10h4m12 0h4" stroke="#FFFFFF" stroke-width="2.2" stroke-linecap="round"/>
            </svg>
            <div>
                <div style="font-size: 18px; font-weight: 700; color: #1A1A1A; letter-spacing: -0.025em; line-height: 1.1;">RoboPulse</div>
                <div style="font-size: 11px; font-weight: 500; color: #6A6A6A; letter-spacing: 0.01em;">Smart Maintenance. Higher Uptime.</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Grouped, text-only navigation keeps the 11 destinations easy to scan.
    navigation_groups = {
        "FLEET": ["Fleet Overview", "Robotic Assets", "Sensor Network"],
        "OPERATIONS": [
            "Telemetry and Charts",
            "Predictive Analytics",
            "Maintenance Scheduler",
            "Incident Tracker",
            "Notification Center",
            "Health Diagnostics",
        ],
        "ADMIN": ["User Management", "Product Overview"],
    }
    navigation_keys = ["nav_fleet", "nav_operations", "nav_admin"]

    if "selected_page" not in st.session_state:
        st.session_state["selected_page"] = "Fleet Overview"

    def select_navigation_page(widget_key):
        for navigation_key in navigation_keys:
            if navigation_key != widget_key:
                st.session_state[navigation_key] = None
        st.session_state["selected_page"] = st.session_state[widget_key]

    for (section_name, pages), widget_key in zip(navigation_groups.items(), navigation_keys):
        st.markdown(f"<div class='nav-section-title'>{section_name}</div>", unsafe_allow_html=True)
        current_page = st.session_state["selected_page"]
        st.radio(
            "Navigation",
            pages,
            index=pages.index(current_page) if current_page in pages else None,
            key=widget_key,
            label_visibility="collapsed",
            on_change=select_navigation_page,
            args=(widget_key,),
        )

    selected_page = st.session_state["selected_page"]

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Operator Profile Card
    st.markdown(
        f"""
        <div style="background: #FFFFFF; border: 1px solid #EEECE8; border-radius: 6px; padding: 12px; margin-bottom: 12px; box-shadow: 0 1px 2px rgba(0,0,0,0.03);">
            <div style="font-size: 10px; color: #6A6A6A; text-transform: uppercase; font-weight: 600; letter-spacing: 0.05em;">Signed In Operator</div>
            <div style="font-size: 13px; font-weight: 600; color: #1A1A1A; margin-top: 2px;">{st.session_state['full_name']}</div>
            <div style="font-size: 11px; color: #E05C1A; font-weight: 500; margin-top: 1px;">Role: {st.session_state['role']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Sidebar Action Buttons
    col_em, col_out = st.columns(2)
    with col_em:
        if st.button("Emergency Stop", width="stretch", help="Trigger emergency stop protocol", key="btn_e_stop"):
            st.toast("Emergency Stop signal dispatched to all active controllers.")
    with col_out:
        if st.button("Sign Out", width="stretch"):
            st.session_state["logged_in"] = False
            st.session_state["access_token"] = None
            st.rerun()


# ============================================================
# 5. DATA FETCHING HELPERS
# ============================================================

# Fast cache: robots, sensors, predictions, incidents etc. refresh every 10s
@st.cache_data(ttl=10)
def load_fast_data():
    robots = api.get_robots()
    sensors = api.get_sensors()
    predictions = api.get_all_predictions()
    maintenance = api.get_all_maintenance()
    incidents = api.get_all_incidents()
    notifications = api.get_all_notifications()
    users = api.get_all_users()
    return {
        "robots": robots,
        "sensors": sensors,
        "predictions": predictions,
        "maintenance": maintenance,
        "incidents": incidents,
        "notifications": notifications,
        "users": users,
    }

# Telemetry is a large dataset — only fetch when needed, cache for 30s
@st.cache_data(ttl=30)
def load_telemetry():
    return api.get_all_telemetry()

data = load_fast_data()
robots = data["robots"]
sensors = data["sensors"]
predictions = data["predictions"]
maintenance = data["maintenance"]
incidents = data["incidents"]
notifications = data["notifications"]
users = data["users"]

# Telemetry loaded lazily only when the page needs it
if selected_page in ["Telemetry", "Telemetry and Charts"]:
    telemetry = load_telemetry()
else:
    # Light summary for Fleet Overview KPIs — use cached or empty list
    try:
        telemetry = load_telemetry()
    except Exception:
        telemetry = []




# ============================================================
# 6. PAGE 1: FLEET OVERVIEW
# ============================================================

if selected_page in ["Dashboard", "Fleet Overview"]:
    st.markdown(
        '''
        <div class="main-header">
            <div>
                <h1 class="main-title">Fleet Overview</h1>
                <p class="main-subtitle">Real-time status, health metrics, and automated failure detection across all robotic assets.</p>
            </div>
        </div>
        ''',
        unsafe_allow_html=True,
    )

    total_r = len(robots)
    active_r = sum(1 for r in robots if str(r.get("status", "")).lower() in ["active", "operational", "normal", "online"])
    open_incidents = sum(1 for inc in incidents if not inc.get("resolved", False))
    unread_notifs = sum(1 for n in notifications if str(n.get("status", "")).lower() == "unread")

    critical_pred = sum(1 for p in predictions if float(p.get("failure_probability", 0) or 0) >= 0.80)
    warning_pred = sum(1 for p in predictions if 0.50 <= float(p.get("failure_probability", 0) or 0) < 0.80)

    # Top KPI Row - 6 Clean Industrial Metric Cards (No Emotes)
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    with kpi1:
        st.markdown(
            f'''<div class="metric-box">
                <div class="metric-box-title-row">
                    <span class="metric-box-title">Total Fleet</span>
                    <span style="width:7px; height:7px; border-radius:50%; background:#6A6A6A;"></span>
                </div>
                <div class="metric-box-val">{total_r}</div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="metric-box-desc">Registered Arms</span>
                    <span class="metric-trend-badge" style="background:#EBF5EE; color:#2E7D4E;">+12%</span>
                </div>
            </div>''',
            unsafe_allow_html=True
        )
    with kpi2:
        st.markdown(
            f'''<div class="metric-box">
                <div class="metric-box-title-row">
                    <span class="metric-box-title">Operational</span>
                    <span style="width:7px; height:7px; border-radius:50%; background:#4A9B6F;"></span>
                </div>
                <div class="metric-box-val" style="color:#2E7D4E;">{active_r}</div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="metric-box-desc">Online & Active</span>
                    <span class="metric-trend-badge" style="background:#EBF5EE; color:#2E7D4E;">+8%</span>
                </div>
            </div>''',
            unsafe_allow_html=True
        )
    with kpi3:
        st.markdown(
            f'''<div class="metric-box">
                <div class="metric-box-title-row">
                    <span class="metric-box-title">Warning Risk</span>
                    <span style="width:7px; height:7px; border-radius:50%; background:#E8A020;"></span>
                </div>
                <div class="metric-box-val" style="color:#B26A00;">{warning_pred}</div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="metric-box-desc">50% - 80% Prob</span>
                    <span class="metric-trend-badge" style="background:#FEF6E9; color:#B26A00;">-5%</span>
                </div>
            </div>''',
            unsafe_allow_html=True
        )
    with kpi4:
        st.markdown(
            f'''<div class="metric-box">
                <div class="metric-box-title-row">
                    <span class="metric-box-title">Critical Stops</span>
                    <span style="width:7px; height:7px; border-radius:50%; background:#D94040;"></span>
                </div>
                <div class="metric-box-val" style="color:#C53030;">{critical_pred}</div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="metric-box-desc">>80% Probability</span>
                    <span class="metric-trend-badge" style="background:#FDF0EE; color:#C53030;">+2%</span>
                </div>
            </div>''',
            unsafe_allow_html=True
        )
    with kpi5:
        st.markdown(
            f'''<div class="metric-box">
                <div class="metric-box-title-row">
                    <span class="metric-box-title">Open Incidents</span>
                    <span style="width:7px; height:7px; border-radius:50%; background:#E8A020;"></span>
                </div>
                <div class="metric-box-val">{open_incidents}</div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="metric-box-desc">Pending Action</span>
                    <span class="metric-trend-badge" style="background:#EBF5EE; color:#2E7D4E;">-11%</span>
                </div>
            </div>''',
            unsafe_allow_html=True
        )
    with kpi6:
        st.markdown(
            f'''<div class="metric-box">
                <div class="metric-box-title-row">
                    <span class="metric-box-title">Unread Alerts</span>
                    <span style="width:7px; height:7px; border-radius:50%; background:#E05C1A;"></span>
                </div>
                <div class="metric-box-val" style="color:#E05C1A;">{unread_notifs}</div>
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span class="metric-box-desc">Notification Feed</span>
                    <span class="metric-trend-badge" style="background:#FDF0EE; color:#C53030;">+20%</span>
                </div>
            </div>''',
            unsafe_allow_html=True
        )
    st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

    # Main split layout (Left: 60%, Right: 40%)
    col_left, col_right = st.columns([1.55, 1])

    with col_left:
        st.markdown(
            '''
            <div class="section-header-row">
                <div class="section-header"><span class="section-header-bar"></span> Robotic Asset Fleet Status</div>
            </div>
            ''',
            unsafe_allow_html=True
        )
        if robots:
            latest_pred_by_robot = {}
            for p in predictions:
                rid = p.get("robot_id")
                if rid not in latest_pred_by_robot:
                    latest_pred_by_robot[rid] = p

            card_cols = st.columns(2)
            for idx, r in enumerate(robots[:8]):
                rid = r.get("robot_id")
                r_pred = latest_pred_by_robot.get(rid)
                prob = float(r_pred.get("failure_probability", 0) or 0) if r_pred else 0.0
                prob_pct = prob * 100
                status = r.get("status", "Active")
                
                status_lower = status.lower()
                if status_lower in ["active", "operational", "normal", "online"]:
                    status_class = "badge-active"
                    badge_label = "OPERATIONAL"
                elif status_lower in ["maintenance", "inspect", "warning"]:
                    status_class = "badge-warning"
                    badge_label = "MAINTENANCE"
                else:
                    status_class = "badge-critical"
                    badge_label = "HIGH RISK"

                bar_color = "#C53030" if prob >= 0.60 else ("#B26A00" if prob >= 0.30 else "#2E7D4E")
                loc = r.get('location') or f"Assembly Line {((idx % 6) + 1)}"

                with card_cols[idx % 2]:
                    st.markdown(
                        f'''
                        <div class="robot-card">
                            <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                                <div>
                                    <strong style="font-size:15px; color:#1A1A1A; display:block; line-height:1.2;">{r.get('robot_name')}</strong>
                                    <div style="font-size:12px; color:#6A6A6A; margin-top:2px;">
                                        {r.get('manufacturer')} &bull; {r.get('model')} &bull; {loc}
                                    </div>
                                </div>
                                <span class="status-badge {status_class}">{badge_label}</span>
                            </div>
                            <div style="font-size:11.5px; color:#6A6A6A; margin: 10px 0 6px 0; border-top: 1px solid #EEECE8; padding-top: 6px;">
                                Payload: <strong style="color:#1A1A1A;">{r.get('payload_capacity', 'N/A')} kg</strong> &nbsp;|&nbsp; Reach: <strong style="color:#1A1A1A;">{r.get('reach', 'N/A')} m</strong>
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; font-size:12px; color:#6A6A6A;">
                                <span>Failure Risk</span>
                                <strong style="font-size:12.5px; color:{bar_color};">{prob_pct:.1f}%</strong>
                            </div>
                            <div class="risk-progress-track">
                                <div class="risk-progress-fill" style="width: {min(max(prob_pct, 4), 100)}%; background: {bar_color};"></div>
                            </div>
                        </div>
                        ''',
                        unsafe_allow_html=True,
                    )
        else:
            st.info("No robotic assets registered yet.")

    with col_right:
        st.markdown(
            '''
            <div class="section-header-row">
                <div class="section-header"><span class="section-header-bar"></span> Recent High-Risk Predictions</div>
            </div>
            ''',
            unsafe_allow_html=True
        )
        if predictions:
            recent_high_risk = [p for p in predictions if float(p.get("failure_probability", 0) or 0) >= 0.50]
            if not recent_high_risk:
                recent_high_risk = predictions[-4:]
            for pred in recent_high_risk[:4]:
                p_prob = float(pred.get("failure_probability", 0) or 0) * 100
                if p_prob >= 80:
                    badge_text = "CRITICAL"
                    badge_class = "badge-critical"
                elif p_prob >= 65:
                    badge_text = "HIGH"
                    badge_class = "badge-critical"
                else:
                    badge_text = "MEDIUM"
                    badge_class = "badge-medium"
                
                st.markdown(
                    f'''
                    <div class="prediction-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; width:100%;">
                            <div>
                                <strong style="font-size:14px; color:#1A1A1A;">Robot {pred.get('robot_id')}</strong>
                                <div style="font-size:12px; color:#6A6A6A; margin-top:2px;">
                                    Fault: <span style="color:#1A1A1A; font-weight:600;">{pred.get('predicted_fault', 'Motor Overheating')}</span>
                                </div>
                                <div style="font-size:11.5px; color:#E05C1A; font-weight:600; margin-top:2px;">
                                    {pred.get('recommendation', 'Inspect Component')}
                                </div>
                            </div>
                            <div style="text-align:right;">
                                <div style="font-size:13px; font-weight:700; color:#1A1A1A;">{p_prob:.1f}% Risk</div>
                                <span class="status-badge {badge_class}" style="margin-top:3px;">{badge_text}</span>
                            </div>
                        </div>
                    </div>
                    ''',
                    unsafe_allow_html=True,
                )
        else:
            st.info("No prediction records generated yet.")

        st.markdown(
            '''
            <div class="section-header-row" style="margin-top:1.5rem;">
                <div class="section-header"><span class="section-header-bar"></span> Latest Telemetry Summary</div>
            </div>
            ''',
            unsafe_allow_html=True
        )
        if telemetry:
            latest_t = telemetry[-1]
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                st.metric("Target Asset", f"Robot {latest_t.get('robot_id')}")
                st.metric("Joint 0 Current", f"{latest_t.get('Current_J0', 0):.2f} A")
                st.metric("Joint 0 Speed", f"{latest_t.get('Speed_J0', 0):.1f} deg/s")
            with t_col2:
                st.metric("Joint 0 Temp", f"{latest_t.get('Temperature_T0', 0):.1f} C")
                st.metric("Tool Current", f"{latest_t.get('Tool_current', 0):.2f} A")
                st.metric("Cycle Count", f"{latest_t.get('cycle', 0)}")
        else:
            st.info("No telemetry records available.")

elif selected_page in ["Fleet", "Robotic Assets"]:
    st.markdown(
        """
        <div class="main-header">
            <div>
                <h1 class="main-title">Robotic Assets</h1>
                <p class="main-subtitle">Manage, register, modify, and monitor industrial robot arms</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Add Robot Expander
    with st.expander("Register New Robot Arm", expanded=False):
        with st.form("create_robot_form"):
            r_col1, r_col2 = st.columns(2)
            with r_col1:
                new_r_name = st.text_input("Robot Name", placeholder="e.g. Robot-51 (Welding Arm)")
                new_r_mfr = st.selectbox("Manufacturer", ["ABB", "KUKA", "Fanuc", "Yaskawa", "Universal Robots", "Siemens", "Other"])
                new_r_model = st.text_input("Model", placeholder="e.g. IRB 6700")
                new_r_serial = st.text_input("Serial Number", placeholder="e.g. RB98210")
            with r_col2:
                new_r_loc = st.text_input("Location / Station", placeholder="e.g. Assembly Line 3")
                new_r_payload = st.number_input("Payload Capacity (kg)", min_value=0.0, max_value=500.0, value=20.0, step=0.5)
                new_r_reach = st.number_input("Reach (meters)", min_value=0.0, max_value=10.0, value=1.8, step=0.1)
                new_r_status = st.selectbox("Operational Status", ["Active", "Maintenance", "Inactive"])

            submit_new_robot = st.form_submit_button("Register Robot Arm", width="stretch")

            if submit_new_robot:
                if not new_r_name or not new_r_model or not new_r_serial:
                    st.warning("Please provide Robot Name, Model, and Serial Number.")
                else:
                    payload = {
                        "robot_name": new_r_name,
                        "manufacturer": new_r_mfr,
                        "model": new_r_model,
                        "serial_number": new_r_serial,
                        "installation_date": datetime.date.today().isoformat(),
                        "location": new_r_loc,
                        "payload_capacity": new_r_payload,
                        "reach": new_r_reach,
                        "status": new_r_status,
                    }
                    res, err = api.create_robot(payload)
                    if res:
                        st.success(f"Robot '{new_r_name}' registered successfully with ID {res.get('robot_id')}.")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Failed to create robot: {err}")

    # Search & Filter
    f_col1, f_col2, f_col3 = st.columns([2, 1, 1])
    with f_col1:
        search_query = st.text_input("Search Robots", placeholder="Filter by name, serial, or model...").lower()
    with f_col2:
        mfr_filter = st.selectbox("Manufacturer", ["All"] + sorted(list(set(r.get("manufacturer", "") for r in robots if r.get("manufacturer")))))
    with f_col3:
        status_filter = st.selectbox("Status", ["All", "Active", "Maintenance", "Inactive"])

    filtered_robots = robots
    if search_query:
        filtered_robots = [
            r for r in filtered_robots
            if search_query in str(r.get("robot_name", "")).lower()
            or search_query in str(r.get("serial_number", "")).lower()
            or search_query in str(r.get("model", "")).lower()
        ]
    if mfr_filter != "All":
        filtered_robots = [r for r in filtered_robots if r.get("manufacturer") == mfr_filter]
    if status_filter != "All":
        filtered_robots = [r for r in filtered_robots if str(r.get("status", "")).lower() == status_filter.lower()]

    st.markdown(f"**Showing {len(filtered_robots)} of {len(robots)} robot arms**")

    # Table & Edit/Delete section
    if filtered_robots:
        df_robots = pd.DataFrame(filtered_robots)
        st.dataframe(df_robots, width="stretch", hide_index=True)

        st.markdown('<div class="section-header">Asset Inspection and Management</div>', unsafe_allow_html=True)
        selected_robot_id = st.selectbox(
            "Select Robot Arm",
            options=[r["robot_id"] for r in filtered_robots],
            format_func=lambda x: f"Robot {x} - {next((r['robot_name'] for r in filtered_robots if r['robot_id'] == x), '')}",
        )

        selected_robot = next((r for r in filtered_robots if r["robot_id"] == selected_robot_id), None)
        if selected_robot:
            act_col1, act_col2 = st.columns(2)
            with act_col1:
                with st.form(f"edit_robot_{selected_robot_id}"):
                    st.markdown(f"#### Edit Robot {selected_robot_id}")
                    edit_name = st.text_input("Name", value=selected_robot.get("robot_name", ""))
                    edit_mfr = st.text_input("Manufacturer", value=selected_robot.get("manufacturer", ""))
                    edit_model = st.text_input("Model", value=selected_robot.get("model", ""))
                    edit_loc = st.text_input("Location", value=selected_robot.get("location", ""))
                    edit_status = st.selectbox("Status", ["Active", "Maintenance", "Inactive"], index=["active", "maintenance", "inactive"].index(str(selected_robot.get("status", "Active")).lower()) if str(selected_robot.get("status", "Active")).lower() in ["active", "maintenance", "inactive"] else 0)
                    edit_payload = st.number_input("Payload (kg)", value=float(selected_robot.get("payload_capacity", 20.0) or 20.0))
                    edit_reach = st.number_input("Reach (m)", value=float(selected_robot.get("reach", 1.8) or 1.8))

                    save_changes = st.form_submit_button("Save Changes", width="stretch")
                    if save_changes:
                        up_payload = {
                            "robot_name": edit_name,
                            "manufacturer": edit_mfr,
                            "model": edit_model,
                            "location": edit_loc,
                            "status": edit_status,
                            "payload_capacity": edit_payload,
                            "reach": edit_reach,
                        }
                        res, err = api.update_robot(selected_robot_id, up_payload)
                        if res:
                            st.success("Robot updated successfully.")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"Failed to update: {err}")

            with act_col2:
                st.markdown(f"#### Direct Actions")
                st.write(f"Serial Number: `{selected_robot.get('serial_number')}`")
                st.write(f"Installation Date: `{selected_robot.get('installation_date')}`")

                if st.button(f"Run AI Diagnostics on Robot {selected_robot_id}", width="stretch"):
                    with st.spinner("Evaluating telemetry against Random Forest model..."):
                        diag, err = api.predict_for_robot(selected_robot_id)
                        if diag:
                            st.success(f"Result: {diag.get('predicted_fault')} ({float(diag.get('failure_probability', 0))*100:.1f}% failure probability)")
                            st.info(f"Recommendation: {diag.get('recommendation')}")
                        else:
                            st.error(f"Diagnostics error: {err}")

                st.markdown("---")
                if st.button(f"Delete Robot {selected_robot_id}", width="stretch"):
                    ok, msg = api.delete_robot(selected_robot_id)
                    if ok:
                        st.success(f"Robot {selected_robot_id} deleted successfully.")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Delete failed: {msg}")
    else:
        st.info("No robots match your search criteria.")


# ============================================================
# 8. PAGE 3: SENSOR NETWORK (FULL CRUD)
# ============================================================

elif selected_page == "Sensor Network":
    st.markdown(
        """
        <div class="main-header">
            <div>
                <h1 class="main-title">Sensor Network</h1>
                <p class="main-subtitle">Monitor and configure multi-modal sensors mapped across robot arms</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    s_total = len(sensors)
    s_active = sum(1 for s in sensors if str(s.get("status", "")).lower() == "active")
    s_col1, s_col2, s_col3 = st.columns(3)
    with s_col1:
        st.metric("Total Sensors", s_total)
    with s_col2:
        st.metric("Active Sensors", s_active)
    with s_col3:
        st.metric("Unique Types", len(set(s.get("sensor_type") for s in sensors if s.get("sensor_type"))))

    # Add Sensor Expander
    with st.expander("Provision New Sensor", expanded=False):
        with st.form("create_sensor_form"):
            sc1, sc2 = st.columns(2)
            with sc1:
                s_robot_id = st.selectbox("Assign to Robot", [r["robot_id"] for r in robots], format_func=lambda x: f"Robot {x}") if robots else st.number_input("Robot ID", min_value=1, value=1)
                s_name = st.text_input("Sensor Name", placeholder="e.g. Joint 0 Thermal Probe")
                s_type = st.selectbox("Sensor Type", ["Temperature", "Vibration", "Current", "Voltage", "Humidity", "Pressure", "Torque"])
            with sc2:
                s_mfr = st.selectbox("Sensor Manufacturer", ["Bosch", "Honeywell", "Siemens", "ABB", "Omron", "Other"])
                s_unit = st.text_input("Engineering Unit", value="°C" if s_type == "Temperature" else ("mm/s" if s_type == "Vibration" else "A"))
                s_status = st.selectbox("Initial Status", ["Active", "Calibration", "Inactive"])

            submit_sensor = st.form_submit_button("Provision Sensor", width="stretch")
            if submit_sensor:
                if not s_name:
                    st.warning("Please provide a Sensor Name.")
                else:
                    s_payload = {
                        "robot_id": s_robot_id,
                        "sensor_name": s_name,
                        "sensor_type": s_type,
                        "manufacturer": s_mfr,
                        "unit": s_unit,
                        "status": s_status,
                    }
                    res, err = api.create_sensor(s_payload)
                    if res:
                        st.success(f"Sensor '{s_name}' provisioned with ID {res.get('sensor_id')}.")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Failed to create sensor: {err}")

    if sensors:
        df_sensors = pd.DataFrame(sensors)
        st.dataframe(df_sensors, width="stretch", hide_index=True)

        st.markdown('<div class="section-header">Sensor Modification and Management</div>', unsafe_allow_html=True)
        sel_s_id = st.selectbox("Select Sensor ID", [s["sensor_id"] for s in sensors], format_func=lambda x: f"Sensor {x} - {next((s['sensor_name'] for s in sensors if s['sensor_id'] == x), '')}")
        sel_s = next((s for s in sensors if s["sensor_id"] == sel_s_id), None)

        if sel_s:
            s_edit_col, s_del_col = st.columns([2, 1])
            with s_edit_col:
                with st.form(f"edit_sensor_{sel_s_id}"):
                    st.markdown(f"#### Edit Sensor {sel_s_id}")
                    e_s_name = st.text_input("Sensor Name", value=sel_s.get("sensor_name", ""))
                    e_s_type = st.text_input("Sensor Type", value=sel_s.get("sensor_type", ""))
                    e_s_mfr = st.text_input("Manufacturer", value=sel_s.get("manufacturer", ""))
                    e_s_unit = st.text_input("Unit", value=sel_s.get("unit", ""))
                    e_s_stat = st.selectbox("Status", ["Active", "Inactive", "Calibration"], index=["active", "inactive", "calibration"].index(str(sel_s.get("status", "Active")).lower()) if str(sel_s.get("status", "Active")).lower() in ["active", "inactive", "calibration"] else 0)

                    if st.form_submit_button("Update Sensor", width="stretch"):
                        up_s_payload = {
                            "sensor_name": e_s_name,
                            "sensor_type": e_s_type,
                            "manufacturer": e_s_mfr,
                            "unit": e_s_unit,
                            "status": e_s_stat,
                        }
                        res, err = api.update_sensor(sel_s_id, up_s_payload)
                        if res:
                            st.success("Sensor updated successfully.")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"Update failed: {err}")

            with s_del_col:
                st.markdown(f"#### Remove Sensor")
                st.write(f"Robot ID: **{sel_s.get('robot_id')}**")
                st.write(f"Type: **{sel_s.get('sensor_type')}**")
                if st.button(f"Delete Sensor {sel_s_id}", width="stretch"):
                    ok, msg = api.delete_sensor(sel_s_id)
                    if ok:
                        st.success("Sensor deleted successfully.")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Delete failed: {msg}")
    else:
        st.info("No sensors registered yet.")


# ============================================================
# 9. PAGE 4: TELEMETRY & CHARTS
# ============================================================

elif selected_page in ["Telemetry", "Telemetry and Charts"]:
    st.markdown(
        """
        <div class="main-header">
            <div>
                <h1 class="main-title">Joint Telemetry and Waveform Analytics</h1>
                <p class="main-subtitle">High-frequency joint currents, thermal curves, speeds (J0-J5), and tool cycle metrics</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Ingest Field Telemetry Data Point", expanded=False):
        with st.form("ingest_telemetry_form"):
            st.markdown("#### Submit 6-Axis Joint Metrics to Pipeline")
            t_robot_id = st.selectbox("Target Robot", [r["robot_id"] for r in robots], format_func=lambda x: f"Robot {x}") if robots else st.number_input("Robot ID", min_value=1, value=1)
            
            c1, c2, c3 = st.columns(3)
            with c1:
                st.caption("Joint Currents (Amperes)")
                in_cj0 = st.number_input("Current J0", value=1.85, step=0.05)
                in_cj1 = st.number_input("Current J1", value=2.40, step=0.05)
                in_cj2 = st.number_input("Current J2", value=3.10, step=0.05)
                in_cj3 = st.number_input("Current J3", value=1.20, step=0.05)
                in_cj4 = st.number_input("Current J4", value=0.95, step=0.05)
                in_cj5 = st.number_input("Current J5", value=0.80, step=0.05)
            with c2:
                st.caption("Joint Temperatures (°C)")
                in_tt0 = st.number_input("Temperature T0", value=45.2, step=0.5)
                in_tj1 = st.number_input("Temperature J1", value=48.0, step=0.5)
                in_tj2 = st.number_input("Temperature J2", value=52.3, step=0.5)
                in_tj3 = st.number_input("Temperature J3", value=44.1, step=0.5)
                in_tj4 = st.number_input("Temperature J4", value=41.5, step=0.5)
                in_tj5 = st.number_input("Temperature J5", value=39.8, step=0.5)
            with c3:
                st.caption("Joint Speeds (deg/s) and Tool Load")
                in_sj0 = st.number_input("Speed J0", value=120.0, step=1.0)
                in_sj1 = st.number_input("Speed J1", value=95.0, step=1.0)
                in_sj2 = st.number_input("Speed J2", value=110.0, step=1.0)
                in_sj3 = st.number_input("Speed J3", value=140.0, step=1.0)
                in_sj4 = st.number_input("Speed J4", value=160.0, step=1.0)
                in_sj5 = st.number_input("Speed J5", value=180.0, step=1.0)
                in_tc = st.number_input("Tool Current (A)", value=0.45, step=0.05)
                in_cyc = st.number_input("Cycle Index", value=125.0, step=1.0)

            submit_telemetry = st.form_submit_button("Ingest Reading", width="stretch")
            if submit_telemetry:
                t_payload = {
                    "robot_id": t_robot_id,
                    "Current_J0": in_cj0, "Current_J1": in_cj1, "Current_J2": in_cj2, "Current_J3": in_cj3, "Current_J4": in_cj4, "Current_J5": in_cj5,
                    "Temperature_T0": in_tt0, "Temperature_J1": in_tj1, "Temperature_J2": in_tj2, "Temperature_J3": in_tj3, "Temperature_J4": in_tj4, "Temperature_J5": in_tj5,
                    "Speed_J0": in_sj0, "Speed_J1": in_sj1, "Speed_J2": in_sj2, "Speed_J3": in_sj3, "Speed_J4": in_sj4, "Speed_J5": in_sj5,
                    "Tool_current": in_tc, "cycle": in_cyc
                }
                res, err = api.create_telemetry(t_payload)
                if res:
                    st.success(f"Telemetry record ingested with ID {res.get('telemetry_id')}.")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"Ingestion failed: {err}")

    if telemetry:
        df_tel = pd.DataFrame(telemetry)

        available_rids = sorted(list(set(df_tel["robot_id"].dropna())))
        selected_tel_robot = st.selectbox("Select Target Robot", ["All Robots"] + [f"Robot {rid}" for rid in available_rids])

        if selected_tel_robot != "All Robots":
            target_rid = int(selected_tel_robot.replace("Robot ", ""))
            plot_df = df_tel[df_tel["robot_id"] == target_rid].copy()
        else:
            plot_df = df_tel.copy()

        total_records = len(plot_df)

        # --- Performance Cap: limit rows sent to chart renderer ---
        MAX_CHART_ROWS = 300
        if total_records > MAX_CHART_ROWS:
            plot_df = plot_df.tail(MAX_CHART_ROWS).reset_index(drop=True)
            st.info(
                f"Showing the latest {MAX_CHART_ROWS} of {total_records} records for smooth performance. "
                f"Use the Raw Feed tab to export all data."
            )
        else:
            st.markdown(f"**{total_records} telemetry entries**")

        tab_current, tab_temp, tab_speed, tab_raw = st.tabs([
            "Currents (J0-J5)",
            "Thermal Profiles (T0-J5)",
            "Joint Speeds (J0-J5)",
            "Raw Telemetry Feed"
        ])

        with tab_current:
            current_cols = [c for c in ["Current_J0", "Current_J1", "Current_J2", "Current_J3", "Current_J4", "Current_J5", "Tool_current"] if c in plot_df.columns]
            if current_cols:
                st.line_chart(plot_df[current_cols], width="stretch")

        with tab_temp:
            temp_cols = [c for c in ["Temperature_T0", "Temperature_J1", "Temperature_J2", "Temperature_J3", "Temperature_J4", "Temperature_J5"] if c in plot_df.columns]
            if temp_cols:
                st.line_chart(plot_df[temp_cols], width="stretch")

        with tab_speed:
            speed_cols = [c for c in ["Speed_J0", "Speed_J1", "Speed_J2", "Speed_J3", "Speed_J4", "Speed_J5"] if c in plot_df.columns]
            if speed_cols:
                st.line_chart(plot_df[speed_cols], width="stretch")

        with tab_raw:
            # For raw table, allow up to 500 rows with pagination-friendly display
            raw_df = df_tel if selected_tel_robot == "All Robots" else df_tel[df_tel["robot_id"] == int(selected_tel_robot.replace("Robot ", ""))]
            st.caption(f"Showing {min(500, len(raw_df))} of {len(raw_df)} total records")
            st.dataframe(raw_df.tail(500).reset_index(drop=True), width="stretch", hide_index=True)

            st.markdown("#### Remove Telemetry Entry")
            tel_del_id = st.number_input("Telemetry ID to Delete", min_value=1, step=1)
            if st.button("Delete Record"):
                ok, msg = api.delete_telemetry(tel_del_id)
                if ok:
                    st.success(f"Telemetry record {tel_del_id} deleted.")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"Delete failed: {msg}")
    else:
        st.info("No telemetry records recorded.")


# ============================================================
# 10. PAGE 5: PREDICTIVE ANALYTICS & ML LAB
# ============================================================

elif selected_page in ["Analytics", "Predictive Analytics"]:
    st.markdown(
        """
        <div class="main-header">
            <div>
                <h1 class="main-title">Predictive Analytics and Machine Learning</h1>
                <p class="main-subtitle">Automated protective stop forecasting, parameter simulation, and prescriptive recommendations</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    tab_auto_diag, tab_ml_sim, tab_pred_history = st.tabs([
        "Automated Robot Diagnosis",
        "Interactive ML Simulator",
        "Historical Predictions Log"
    ])

    # TAB 1: ONE CLICK AUTO DIAGNOSIS
    with tab_auto_diag:
        st.markdown("#### Model Evaluation on Latest Robot Telemetry")
        st.write("Fetches the latest real-time sensor cycle for the selected robot and runs it through the trained Random Forest classifier.")

        diag_robot_id = st.selectbox(
            "Select Target Robot",
            [r["robot_id"] for r in robots] if robots else [1],
            format_func=lambda x: f"Robot {x} - {next((r['robot_name'] for r in robots if r['robot_id'] == x), '')}"
        )

        if st.button("Evaluate Failure Risk", width="stretch"):
            with st.spinner(f"Evaluating telemetry for Robot {diag_robot_id}..."):
                diag_res, err = api.predict_for_robot(diag_robot_id)

            if diag_res:
                prob = float(diag_res.get("failure_probability", 0) or 0)
                prob_pct = prob * 100
                fault = diag_res.get("predicted_fault", "Unknown")
                recom = diag_res.get("recommendation", "No action needed.")

                banner_class = "risk-banner-critical" if prob >= 0.5 else "risk-banner-safe"

                st.markdown(
                    f"""
                    <div class="{banner_class}">
                        <div style="font-size:11px; font-weight:600; text-transform:uppercase; letter-spacing:0.04em; color:#6A6A6A;">
                            Diagnosis Result • Robot {diag_robot_id}
                        </div>
                        <h2 style="font-size:32px; margin:6px 0; color:#1A1A1A; font-weight:700;">
                            {prob_pct:.1f}% Failure Probability
                        </h2>
                        <div style="font-size:16px; font-weight:600; color:{'#D94040' if prob >= 0.8 else ('#E8A020' if prob >= 0.5 else '#4A9B6F')};">
                            Status: {fault}
                        </div>
                        <p style="font-size:13px; margin-top:10px; color:#1A1A1A;">
                            <strong>Recommended Action:</strong> {recom}
                        </p>
                    </div>
        """,
        unsafe_allow_html=True,
    )

    # TAB 2: INTERACTIVE ML SIMULATOR
    with tab_ml_sim:
        st.markdown("#### Interactive Protective-Stop Simulator")
        st.write("Adjust telemetry values to run the trained model against a simulated robot cycle.")

        sim_robot_id = st.selectbox(
            "Simulated Robot",
            [r["robot_id"] for r in robots] if robots else [1],
            format_func=lambda x: f"Robot {x} - {next((r['robot_name'] for r in robots if r['robot_id'] == x), '')}",
            key="sim_robot_id",
        )
        latest_sim_telemetry = next(
            (t for t in reversed(telemetry) if t.get("robot_id") == sim_robot_id), {}
        )

        feature_groups = [
            ["Current_J0", "Temperature_T0", "Current_J1", "Temperature_J1", "Current_J2", "Temperature_J2", "Current_J3", "Temperature_J3"],
            ["Current_J4", "Temperature_J4", "Current_J5", "Temperature_J5", "Tool_current", "cycle"],
            ["Speed_J0", "Speed_J1", "Speed_J2", "Speed_J3", "Speed_J4", "Speed_J5"],
        ]
        sim_payload = {"robot_id": sim_robot_id}
        with st.expander("Adjust simulated telemetry", expanded=True):
            sim_columns = st.columns(3)
            for column, features in zip(sim_columns, feature_groups):
                with column:
                    for feature in features:
                        default_value = float(latest_sim_telemetry.get(feature, 0) or 0)
                        sim_payload[feature] = st.number_input(
                            feature.replace("_", " "),
                            value=default_value,
                            key=f"sim_{feature}",
                        )

        if st.button("Run ML Simulation", width="stretch", key="run_ml_simulation"):
            with st.spinner("Running simulated telemetry through the ML model..."):
                sim_result, err = api.predict_protective_stop_ml(sim_payload)
            if sim_result:
                probability = float(sim_result.get("failure_probability", 0) or 0) * 100
                st.success(f"Simulation complete: {sim_result.get('predicted_fault', 'Unknown')} ({probability:.1f}% failure probability)")
                st.write(f"**Recommendation:** {sim_result.get('recommendation', 'No recommendation returned.')}")
                st.cache_data.clear()
            else:
                st.error(f"Simulation failed: {err}")

    # TAB 3: PREDICTION HISTORY
    with tab_pred_history:
        st.markdown("#### Historical Predictions")
        if predictions:
            history_df = pd.DataFrame(predictions)
            if "prediction_time" in history_df.columns:
                history_df = history_df.sort_values("prediction_time", ascending=False)
            st.caption(f"{len(history_df)} saved prediction record(s)")
            st.dataframe(history_df, width="stretch", hide_index=True)
        else:
            st.info("No saved predictions yet. Run an automated diagnosis or ML simulation to create one.")

elif selected_page == "Maintenance Scheduler":
    st.markdown(
        """
        <div class="main-header">
            <div>
                <h1 class="main-title">Maintenance Scheduler</h1>
                <p class="main-subtitle">Schedule, review, update, and manage robot maintenance operations</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Schedule Maintenance Operation", expanded=False):
        with st.form("create_maint_form"):
            mc1, mc2 = st.columns(2)
            with mc1:
                m_robot_id = st.selectbox("Robot Arm", [r["robot_id"] for r in robots], format_func=lambda x: f"Robot {x}") if robots else st.number_input("Robot ID", min_value=1, value=1)
                m_type = st.selectbox("Maintenance Type", ["Preventive", "Corrective", "Inspection", "Calibration", "Emergency"])
                m_tech = st.selectbox("Assigned Technician", ["Rahul Sharma", "Amit Verma", "Priya Singh", "Neha Gupta", "Rohit Kumar", "Other"])
            with mc2:
                m_date = st.date_input("Maintenance Date", value=datetime.date.today())
                m_next_date = st.date_input("Next Due Date", value=datetime.date.today() + datetime.timedelta(days=90))
                m_remarks = st.text_area("Remarks", placeholder="e.g. Bearing replaced and gear joint lubricated.")

            submit_maint = st.form_submit_button("Record Entry", width="stretch")
            if submit_maint:
                m_payload = {
                    "robot_id": m_robot_id,
                    "maintenance_type": m_type,
                    "technician_name": m_tech,
                    "maintenance_date": m_date.isoformat(),
                    "next_due_date": m_next_date.isoformat(),
                    "remarks": m_remarks or "Routine maintenance logged.",
                }
                res, err = api.create_maintenance(m_payload)
                if res:
                    st.success(f"Maintenance record logged successfully with ID {res.get('maintenance_id')}.")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"Failed to log maintenance: {err}")

    if maintenance:
        df_maint = pd.DataFrame(maintenance)
        st.dataframe(df_maint, width="stretch", hide_index=True)

        st.markdown('<div class="section-header">Update Maintenance Record</div>', unsafe_allow_html=True)
        sel_m_id = st.selectbox("Select Record ID", [m["maintenance_id"] for m in maintenance], format_func=lambda x: f"Record {x} - Robot {next((m['robot_id'] for m in maintenance if m['maintenance_id'] == x), '')}")
        sel_m = next((m for m in maintenance if m["maintenance_id"] == sel_m_id), None)

        if sel_m:
            medit_col, mdel_col = st.columns([2, 1])
            with medit_col:
                with st.form(f"edit_maint_{sel_m_id}"):
                    st.markdown(f"#### Modify Record {sel_m_id}")
                    e_m_type = st.selectbox("Type", ["Preventive", "Corrective", "Inspection", "Calibration", "Emergency"], index=["preventive", "corrective", "inspection", "calibration", "emergency"].index(str(sel_m.get("maintenance_type", "Preventive")).lower()) if str(sel_m.get("maintenance_type", "Preventive")).lower() in ["preventive", "corrective", "inspection", "calibration", "emergency"] else 0)
                    e_m_tech = st.text_input("Technician", value=sel_m.get("technician_name", ""))
                    e_m_rem = st.text_area("Remarks", value=sel_m.get("remarks", ""))

                    if st.form_submit_button("Update Record", width="stretch"):
                        up_m_payload = {
                            "maintenance_type": e_m_type,
                            "technician_name": e_m_tech,
                            "remarks": e_m_rem,
                        }
                        res, err = api.update_maintenance(sel_m_id, up_m_payload)
                        if res:
                            st.success("Maintenance record updated.")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"Update failed: {err}")

            with mdel_col:
                st.markdown("#### Remove Record")
                st.write(f"Robot ID: **{sel_m.get('robot_id')}**")
                st.write(f"Date: **{sel_m.get('maintenance_date')}**")
                if st.button(f"Delete Record {sel_m_id}", width="stretch"):
                    ok, msg = api.delete_maintenance(sel_m_id)
                    if ok:
                        st.success("Record deleted successfully.")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Delete failed: {msg}")
    else:
        st.info("No maintenance records registered yet.")


# ============================================================
# 12. PAGE 7: INCIDENT TRACKER
# ============================================================

elif selected_page == "Incident Tracker":
    st.markdown(
        """
        <div class="main-header">
            <div>
                <h1 class="main-title">Incident Tracker</h1>
                <p class="main-subtitle">Track industrial hardware anomalies, severity classifications, and resolution status</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Log New Incident", expanded=False):
        with st.form("create_incident_form"):
            ic1, ic2 = st.columns(2)
            with ic1:
                inc_robot_id = st.selectbox("Target Robot", [r["robot_id"] for r in robots], format_func=lambda x: f"Robot {x}") if robots else st.number_input("Robot ID", min_value=1, value=1)
                inc_type = st.selectbox("Incident Type", ["Motor Failure", "Bearing Wear", "Power Failure", "Sensor Failure", "Overheating", "Communication Error", "Other"])
                inc_sev = st.selectbox("Severity Level", ["Low", "Medium", "High", "Critical"])
            with ic2:
                inc_desc = st.text_area("Incident Description", placeholder="e.g. Temperature spiked above 70°C and joint 2 experienced torque oscillation.")
                inc_resolved = st.checkbox("Resolved upon entry?", value=False)

            submit_inc = st.form_submit_button("Log Incident", width="stretch")
            if submit_inc:
                inc_payload = {
                    "robot_id": inc_robot_id,
                    "incident_type": inc_type,
                    "severity": inc_sev,
                    "description": inc_desc or "No description provided.",
                    "resolved": inc_resolved,
                }
                res, err = api.create_incident(inc_payload)
                if res:
                    st.success(f"Incident logged with Ticket {res.get('incident_id')}.")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"Failed to log incident: {err}")

    if incidents:
        df_inc = pd.DataFrame(incidents)
        
        res_filter = st.radio("Filter Status", ["All Incidents", "Open Issues Only", "Resolved Issues Only"], horizontal=True)
        if res_filter == "Open Issues Only":
            df_inc = df_inc[df_inc["resolved"] == False]
        elif res_filter == "Resolved Issues Only":
            df_inc = df_inc[df_inc["resolved"] == True]

        st.dataframe(df_inc, width="stretch", hide_index=True)

        st.markdown('<div class="section-header">Resolve or Update Incident Ticket</div>', unsafe_allow_html=True)
        sel_inc_id = st.selectbox("Select Ticket", [i["incident_id"] for i in incidents], format_func=lambda x: f"Ticket {x} - Robot {next((i['robot_id'] for i in incidents if i['incident_id'] == x), '')} ({next((i['severity'] for i in incidents if i['incident_id'] == x), '')})")
        sel_inc = next((i for i in incidents if i["incident_id"] == sel_inc_id), None)

        if sel_inc:
            i_col1, i_col2 = st.columns(2)
            with i_col1:
                cur_resolved = sel_inc.get("resolved", False)
                st.write(f"Current Status: **{'Resolved' if cur_resolved else 'Open / Active'}**")
                st.write(f"Fault: **{sel_inc.get('incident_type')}** ({sel_inc.get('severity')})")
                st.write(f"Description: {sel_inc.get('description')}")

                toggle_action = "Mark as Resolved" if not cur_resolved else "Reopen Ticket"
                if st.button(toggle_action, width="stretch"):
                    up_payload = {"resolved": not cur_resolved}
                    res, err = api.update_incident(sel_inc_id, up_payload)
                    if res:
                        st.success("Incident status updated.")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Status update failed: {err}")

            with i_col2:
                st.markdown("#### Remove Ticket")
                if st.button(f"Delete Ticket {sel_inc_id}", width="stretch"):
                    ok, msg = api.delete_incident(sel_inc_id)
                    if ok:
                        st.success("Incident ticket deleted.")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Delete failed: {msg}")
    else:
        st.info("No incident records logged.")


# ============================================================
# 13. PAGE 8: NOTIFICATION CENTER
# ============================================================

elif selected_page == "Notification Center":
    st.markdown(
        """
        <div class="main-header">
            <div>
                <h1 class="main-title">Notification Center</h1>
                <p class="main-subtitle">Review automated threshold alerts, priority feeds, and dispatch system broadcasts</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Dispatch System Broadcast", expanded=False):
        with st.form("create_notif_form"):
            nc1, nc2 = st.columns(2)
            with nc1:
                n_robot_id = st.selectbox("Target Robot", [r["robot_id"] for r in robots], format_func=lambda x: f"Robot {x}") if robots else st.number_input("Robot ID", min_value=1, value=1)
                n_type = st.selectbox("Alert Type", ["Temperature Alert", "Maintenance Reminder", "Voltage Alert", "Motor Alert", "Sensor Failure", "Prediction Alert", "General Notice"])
                n_prio = st.selectbox("Priority Level", ["Low", "Medium", "High", "Critical"])
            with nc2:
                n_msg = st.text_area("Alert Message", placeholder="e.g. Scheduled maintenance due for joint assembly.")
                n_stat = st.selectbox("Status", ["Unread", "Read"])

            submit_notif = st.form_submit_button("Send Notification", width="stretch")
            if submit_notif:
                n_payload = {
                    "robot_id": n_robot_id,
                    "alert_type": n_type,
                    "message": n_msg or "System notification broadcast.",
                    "priority": n_prio,
                    "status": n_stat,
                }
                res, err = api.create_notification(n_payload)
                if res:
                    st.success(f"Notification broadcasted with ID {res.get('notification_id')}.")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"Failed to create notification: {err}")

    if notifications:
        prio_filter = st.selectbox("Filter Priority", ["All", "Critical", "High", "Medium", "Low"])
        stat_filter = st.selectbox("Filter Status", ["All", "Unread Only", "Read Only"])

        filtered_notifs = notifications
        if prio_filter != "All":
            filtered_notifs = [n for n in filtered_notifs if str(n.get("priority", "")).lower() == prio_filter.lower()]
        if stat_filter == "Unread Only":
            filtered_notifs = [n for n in filtered_notifs if str(n.get("status", "")).lower() == "unread"]
        elif stat_filter == "Read Only":
            filtered_notifs = [n for n in filtered_notifs if str(n.get("status", "")).lower() == "read"]

        st.markdown(f"**Showing {len(filtered_notifs)} alerts**")

        for n in filtered_notifs[:15]:
            nid = n.get("notification_id")
            prio = n.get("priority", "Low")
            status = n.get("status", "Unread")
            
            prio_color = "#D94040" if prio.lower() == "critical" else ("#E8A020" if prio.lower() == "high" else "#E05C1A")
            
            col_msg, col_actions = st.columns([3, 1])
            with col_msg:
                st.markdown(
                    f"""
                    <div style="background:#FFFFFF; border:1px solid #EEECE8; border-left:4px solid {prio_color}; border-radius:6px; padding:12px 16px; margin-bottom:8px; box-shadow:0 1px 2px rgba(0,0,0,0.02);">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <strong style="color:#1A1A1A; font-size:14px;">Robot {n.get('robot_id')} &bull; {n.get('alert_type')}</strong>
                            <span style="font-size:11px; font-weight:700; color:{prio_color}; text-transform:uppercase;">{prio} &bull; {status}</span>
                        </div>
                        <div style="font-size:13px; color:#6A6A6A; margin-top:4px;">{n.get('message')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_actions:
                btn_c1, btn_c2 = st.columns(2)
                with btn_c1:
                    if status.lower() == "unread":
                        if st.button("Read", key=f"read_{nid}", width="stretch"):
                            api.update_notification(nid, {"status": "Read"})
                            st.cache_data.clear()
                            st.rerun()
                with btn_c2:
                    if st.button("Delete", key=f"del_{nid}", width="stretch"):
                        api.delete_notification(nid)
                        st.cache_data.clear()
                        st.rerun()
    else:
        st.info("No notifications in the system feed.")


# ============================================================
# 14. PAGE 9: HEALTH DIAGNOSTICS
# ============================================================

elif selected_page in ["AI Insights", "Health Diagnostics"]:
    st.markdown(
        """
        <div class="main-header">
            <div>
                <h1 class="main-title">Health Diagnostic Station</h1>
                <p class="main-subtitle">Compute real-time health scores from all joint temperatures, currents, speeds, tool load, and ML failure risk</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if robots:
        target_h_robot = st.selectbox(
            "Select Robot Arm",
            [r["robot_id"] for r in robots],
            format_func=lambda x: f"Robot {x} - {next((r['robot_name'] for r in robots if r['robot_id'] == x), '')}"
        )

        if st.button("Calculate Health Score", width="stretch"):
            with st.spinner(f"Computing diagnostic health matrix for Robot {target_h_robot}..."):
                health_data, health_err = api.get_robot_health(target_h_robot)

            if health_data:
                score = float(health_data.get("health_score", 100))
                status_text = health_data.get("health_status", "Optimal")

                if score >= 75:
                    h_banner = "risk-banner-safe"
                    status_color = "#2E7D4E"
                elif score >= 50:
                    h_banner = "risk-banner-warning"
                    status_color = "#E05C1A"
                else:
                    h_banner = "risk-banner-critical"
                    status_color = "#C53030"

                pred_fault = health_data.get("predicted_fault")
                ml_prob = health_data.get("failure_probability", 0.0) * 100

                st.markdown(
                    f"""
                    <div class="{h_banner}">
                        <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                            <div>
                                <div style="font-size:11px; font-weight:700; text-transform:uppercase; letter-spacing:0.06em; color:#6A6A6A;">
                                    Robot {target_h_robot} Operational Health Index
                                </div>
                                <div style="font-size:42px; margin:4px 0 2px 0; color:#1A1A1A; font-weight:800; letter-spacing:-0.03em;">
                                    {score:.1f} <span style="font-size:18px; font-weight:500; color:#6A6A6A;">/ 100</span>
                                </div>
                                <div style="font-size:15px; font-weight:600; color:{status_color};">
                                    Condition: {status_text}
                                </div>
                            </div>
                            <div style="text-align: right;">
                                <div style="font-size:11px; font-weight:600; color:#6A6A6A; text-transform: uppercase; letter-spacing: 0.04em;">ML Failure Risk</div>
                                <div style="font-size:22px; font-weight:700; color:{'#C53030' if ml_prob > 50 else ('#E05C1A' if ml_prob > 20 else '#2E7D4E')}; margin-top: 2px;">
                                    {ml_prob:.1f}%
                                </div>
                                <div style="font-size:12px; color:#6A6A6A; margin-top: 2px;">
                                    Fault: <b>{pred_fault or 'Normal Operation'}</b>
                                </div>
                            </div>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                sm1, sm2, sm3, sm4 = st.columns(4)
                with sm1:
                    st.metric("Peak Joint Temp", f"{health_data.get('temperature', 0):.1f} °C")
                with sm2:
                    st.metric("Avg Joint Speed", f"{health_data.get('joint_speed', 0):.3f} rad/s")
                with sm3:
                    st.metric("Peak Motor Current", f"{health_data.get('motor_current', 0):.2f} A")
                with sm4:
                    st.metric("Tool Load Current", f"{health_data.get('tool_current', 0):.3f} A")

                st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
                diag1, diag2, diag3 = st.columns(3)
                with diag1:
                    st.metric("Average Joint Temp", f"{health_data.get('avg_temperature', 0):.1f} °C")
                with diag2:
                    st.metric("Active Incidents", f"{health_data.get('open_incidents_count', 0)}")
                with diag3:
                    st.metric("Scheduled Maintenance", f"{health_data.get('active_maintenance_count', 0)}")

            else:
                st.error(f"Health score computation failed: {health_err}")
    else:
        st.info("No robots available to run health diagnostics.")


# ============================================================
# 15. PAGE 10: USER MANAGEMENT
# ============================================================

elif selected_page in ["Settings", "User Management"]:
    st.markdown(
        """
        <div class="main-header">
            <div>
                <h1 class="main-title">User Management</h1>
                <p class="main-subtitle">Manage plant operators, technicians, supervisors, and administrators</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    with st.expander("Register New User Profile", expanded=False):
        with st.form("create_user_admin_form"):
            uc1, uc2 = st.columns(2)
            with uc1:
                u_name = st.text_input("Full Name", placeholder="e.g. Vikram Verma")
                u_email = st.text_input("Work Email", placeholder="e.g. v.verma@factoryops.com")
                u_phone = st.text_input("Phone Number", placeholder="e.g. +91 9876543210")
            with uc2:
                u_role = st.selectbox("Role Assignment", ["Admin", "Supervisor", "Technician", "Operator"])
                u_pwd = st.text_input("Initial Password", type="password", placeholder="••••••••")

            submit_u = st.form_submit_button("Create User Profile", width="stretch")
            if submit_u:
                if not u_name or not u_email or not u_pwd:
                    st.warning("Please provide Full Name, Email, and Password.")
                else:
                    u_payload = {
                        "full_name": u_name,
                        "email": u_email,
                        "phone": u_phone,
                        "role": u_role,
                        "password_hash": u_pwd,
                    }
                    res, err = api.create_user(u_payload)
                    if res:
                        st.success(f"User '{u_name}' created with ID {res.get('user_id')}.")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Failed to create user: {err}")

    if users:
        df_users = pd.DataFrame(users)
        st.dataframe(df_users, width="stretch", hide_index=True)

        st.markdown('<div class="section-header">Edit User Profile</div>', unsafe_allow_html=True)
        sel_u_id = st.selectbox("Select User ID", [u["user_id"] for u in users], format_func=lambda x: f"User {x} - {next((u['full_name'] for u in users if u['user_id'] == x), '')} ({next((u['role'] for u in users if u['user_id'] == x), '')})")
        sel_u = next((u for u in users if u["user_id"] == sel_u_id), None)

        if sel_u:
            u_edit_col, u_del_col = st.columns([2, 1])
            with u_edit_col:
                with st.form(f"edit_user_{sel_u_id}"):
                    st.markdown(f"#### Modify User {sel_u_id}")
                    e_u_name = st.text_input("Full Name", value=sel_u.get("full_name", ""))
                    e_u_email = st.text_input("Email", value=sel_u.get("email", ""))
                    e_u_phone = st.text_input("Phone", value=sel_u.get("phone", "") or "")
                    e_u_role = st.selectbox("Role", ["Admin", "Supervisor", "Technician", "Operator"], index=["admin", "supervisor", "technician", "operator"].index(str(sel_u.get("role", "Operator")).lower()) if str(sel_u.get("role", "Operator")).lower() in ["admin", "supervisor", "technician", "operator"] else 0)

                    if st.form_submit_button("Update User Profile", width="stretch"):
                        up_u_payload = {
                            "full_name": e_u_name,
                            "email": e_u_email,
                            "phone": e_u_phone,
                            "role": e_u_role,
                        }
                        res, err = api.update_user(sel_u_id, up_u_payload)
                        if res:
                            st.success("User profile updated.")
                            st.cache_data.clear()
                            st.rerun()
                        else:
                            st.error(f"Update failed: {err}")

            with u_del_col:
                st.markdown("#### Remove User Profile")
                st.write(f"Email: **{sel_u.get('email')}**")
                st.write(f"Role: **{sel_u.get('role')}**")
                if st.button(f"Delete User {sel_u_id}", width="stretch"):
                    ok, msg = api.delete_user(sel_u_id)
                    if ok:
                        st.success("User deleted.")
                        st.cache_data.clear()
                        st.rerun()
                    else:
                        st.error(f"Delete failed: {msg}")
    else:
        st.info("No user records found.")


# ============================================================
# 16. PAGE 11: PRODUCT OVERVIEW (LANDING PAGE)
# ============================================================

elif selected_page == "Product Overview":
    show_landing()


# ============================================================
# 17. FOOTER
# ============================================================

st.markdown(
    """
    <div style="margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #1C152B; text-align: center; font-size: 12px; color: #737373;">
        RoboPulse AI • Predictive Robot Arm Monitoring and Maintenance Platform
    </div>
    """,
    unsafe_allow_html=True,
)
