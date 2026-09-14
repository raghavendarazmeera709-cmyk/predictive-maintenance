import datetime
from typing import Any, Dict, List, Optional
import pandas as pd
import streamlit as st

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
    /* Apple SF Pro typography & clean canvas */
    html, body, [class*="css"] {
        font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", "SF Pro Display", "Helvetica Neue", Helvetica, Arial, sans-serif;
        letter-spacing: -0.015em;
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
    
    .stApp {
        background-color: #f5f5f7;
        color: #1d1d1f;
    }

    /* Sidebar Clean Styling */
    section[data-testid="stSidebar"] {
        background-color: #ffffff;
        border-right: 1px solid #e5e5ea;
    }
    section[data-testid="stSidebar"] .stMarkdown h3 {
        font-size: 20px;
        font-weight: 700;
        color: #1d1d1f;
        letter-spacing: -0.02em;
    }

    /* Header */
    .main-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 1.5rem 0 1rem 0;
        border-bottom: 1px solid #e5e5ea;
        margin-bottom: 1.5rem;
    }
    .main-title {
        font-size: 28px;
        font-weight: 700;
        color: #1d1d1f;
        margin: 0;
        letter-spacing: -0.03em;
        line-height: 1.2;
    }
    .main-subtitle {
        font-size: 15px;
        color: #86868b;
        margin: 4px 0 0 0;
        font-weight: 400;
    }

    /* Apple Metric Cards */
    .metric-box {
        background: #ffffff;
        border: 1px solid #e5e5ea;
        border-radius: 16px;
        padding: 18px 20px;
        min-height: 110px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.02);
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        transition: transform 0.15s ease, box-shadow 0.15s ease;
    }
    .metric-box:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(0, 0, 0, 0.05);
    }
    .metric-box-title {
        font-size: 12px;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        color: #86868b;
    }
    .metric-box-val {
        font-size: 32px;
        font-weight: 700;
        color: #1d1d1f;
        line-height: 1.1;
        margin: 6px 0;
        letter-spacing: -0.03em;
    }
    .metric-box-desc {
        font-size: 12px;
        color: #86868b;
    }

    /* Apple Status Badges */
    .status-badge {
        display: inline-block;
        padding: 4px 10px;
        font-size: 11px;
        font-weight: 600;
        border-radius: 980px;
        letter-spacing: 0.02em;
        text-transform: uppercase;
    }
    .badge-active { background: #e8f5e9; color: #1b5e20; border: 1px solid #c8e6c9; }
    .badge-warning { background: #fff8e1; color: #b78103; border: 1px solid #ffe082; }
    .badge-critical { background: #ffebee; color: #c62828; border: 1px solid #ffcdd2; }
    .badge-neutral { background: #f5f5f7; color: #515154; border: 1px solid #e5e5ea; }

    /* Minimalist Asset Cards */
    .robot-card {
        background: #ffffff;
        border: 1px solid #e5e5ea;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 16px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }

    /* Clean Banners */
    .risk-banner-critical {
        background: #ffffff;
        border: 1px solid #ffcdd2;
        border-left: 5px solid #c62828;
        border-radius: 16px;
        padding: 22px;
        color: #1d1d1f;
        margin-bottom: 16px;
        box-shadow: 0 4px 14px rgba(198, 40, 40, 0.06);
    }
    .risk-banner-safe {
        background: #ffffff;
        border: 1px solid #c8e6c9;
        border-left: 5px solid #1b5e20;
        border-radius: 16px;
        padding: 22px;
        color: #1d1d1f;
        margin-bottom: 16px;
        box-shadow: 0 4px 14px rgba(27, 94, 32, 0.06);
    }

    /* Section Subheadings */
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #1d1d1f;
        margin: 1.5rem 0 1rem 0;
        letter-spacing: -0.02em;
    }

    /* Inputs and Forms */
    .stTextInput > div > div > input,
    .stSelectbox > div > div > div,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        background-color: #ffffff !important;
        color: #1d1d1f !important;
        border: 1px solid #d2d2d7 !important;
        border-radius: 10px !important;
        font-size: 14px !important;
    }

    /* Buttons */
    .stButton > button, .stFormSubmitButton > button {
        background-color: #0071e3 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 980px !important;
        font-size: 14px !important;
        font-weight: 500 !important;
        padding: 8px 20px !important;
        box-shadow: 0 2px 6px rgba(0, 113, 227, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    .stButton > button:hover, .stFormSubmitButton > button:hover {
        background-color: #0077ed !important;
        box-shadow: 0 4px 12px rgba(0, 113, 227, 0.3) !important;
    }

    /* Secondary / Danger Buttons */
    button[kind="secondary"], button[data-testid="baseButton-secondary"] {
        background-color: #f5f5f7 !important;
        color: #1d1d1f !important;
        border: 1px solid #d2d2d7 !important;
    }

    /* Clean Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: #e5e5ea;
        padding: 4px;
        border-radius: 12px;
        margin-bottom: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 6px 16px;
        font-weight: 500;
        font-size: 14px;
        color: #86868b;
        background-color: transparent;
        border: none !important;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ffffff !important;
        color: #1d1d1f !important;
        box-shadow: 0 2px 6px rgba(0, 0, 0, 0.06);
    }

    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #ffffff !important;
        border: 1px solid #e5e5ea !important;
        border-radius: 12px !important;
        font-weight: 600 !important;
        color: #1d1d1f !important;
    }
    .streamlit-expanderContent {
        background-color: #ffffff !important;
        border: 1px solid #e5e5ea !important;
        border-top: none !important;
        border-bottom-left-radius: 12px !important;
        border-bottom-right-radius: 12px !important;
        padding: 16px !important;
    }

    /* Dataframe wrapper */
    [data-testid="stDataFrame"] {
        background: #ffffff;
        border: 1px solid #e5e5ea;
        border-radius: 14px;
        padding: 6px;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.02);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# ============================================================
# 4. SIDEBAR NAVIGATION
# ============================================================

with st.sidebar:
    st.markdown("### RoboPulse AI")
    st.caption("Predictive Intelligence Platform • Version 1.0")

    st.markdown("---")

    # Navigation menu (No Emojis)
    selected_page = st.radio(
        "Navigation",
        [
            "Fleet Overview",
            "Robotic Assets",
            "Sensor Network",
            "Telemetry and Charts",
            "Predictive Analytics",
            "Maintenance Scheduler",
            "Incident Tracker",
            "Notification Center",
            "Health Diagnostics",
            "User Management",
            "Product Overview",
        ],
        index=0,
    )

    st.markdown("---")

    # Operator Profile
    st.markdown(
        f"""
        <div style="background: #f5f5f7; border: 1px solid #e5e5ea; border-radius: 12px; padding: 14px; margin-bottom: 14px;">
            <div style="font-size: 11px; color: #86868b; text-transform: uppercase; font-weight: 600; letter-spacing: 0.04em;">Signed In Operator</div>
            <div style="font-size: 14px; font-weight: 600; color: #1d1d1f; margin-top: 2px;">{st.session_state['full_name']}</div>
            <div style="font-size: 12px; color: #0071e3; margin-top: 2px;">Role: {st.session_state['role']}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Actions
    col_em, col_out = st.columns(2)
    with col_em:
        if st.button("Emergency Stop", use_container_width=True, help="Trigger emergency stop protocol"):
            st.toast("Emergency Stop signal dispatched to all active controllers.")
    with col_out:
        if st.button("Sign Out", use_container_width=True):
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
if selected_page == "Telemetry and Charts":
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

if selected_page == "Fleet Overview":
    st.markdown(
        """
        <div class="main-header">
            <div>
                <h1 class="main-title">Fleet Overview</h1>
                <p class="main-subtitle">Real-time status, health metrics, and automated failure detection across all robotic assets</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    total_r = len(robots)
    active_r = sum(1 for r in robots if str(r.get("status", "")).lower() in ["active", "operational", "normal", "online"])
    open_incidents = sum(1 for inc in incidents if not inc.get("resolved", False))
    unread_notifs = sum(1 for n in notifications if str(n.get("status", "")).lower() == "unread")

    critical_pred = sum(1 for p in predictions if float(p.get("failure_probability", 0) or 0) >= 0.80)
    warning_pred = sum(1 for p in predictions if 0.50 <= float(p.get("failure_probability", 0) or 0) < 0.80)

    # Top KPI Row
    kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)
    with kpi1:
        st.markdown(f'<div class="metric-box"><div class="metric-box-title">Total Fleet</div><div class="metric-box-val">{total_r}</div><div class="metric-box-desc">Registered Arms</div></div>', unsafe_allow_html=True)
    with kpi2:
        st.markdown(f'<div class="metric-box"><div class="metric-box-title">Operational</div><div class="metric-box-val" style="color:#1b5e20;">{active_r}</div><div class="metric-box-desc">Online and Active</div></div>', unsafe_allow_html=True)
    with kpi3:
        st.markdown(f'<div class="metric-box"><div class="metric-box-title">Warning Risk</div><div class="metric-box-val" style="color:#b78103;">{warning_pred}</div><div class="metric-box-desc">50% - 80% Probability</div></div>', unsafe_allow_html=True)
    with kpi4:
        st.markdown(f'<div class="metric-box"><div class="metric-box-title">Critical Stops</div><div class="metric-box-val" style="color:#c62828;">{critical_pred}</div><div class="metric-box-desc">Over 80% Probability</div></div>', unsafe_allow_html=True)
    with kpi5:
        st.markdown(f'<div class="metric-box"><div class="metric-box-title">Open Incidents</div><div class="metric-box-val" style="color:#b78103;">{open_incidents}</div><div class="metric-box-desc">Pending Resolution</div></div>', unsafe_allow_html=True)
    with kpi6:
        st.markdown(f'<div class="metric-box"><div class="metric-box-title">Unread Alerts</div><div class="metric-box-val" style="color:#0071e3;">{unread_notifs}</div><div class="metric-box-desc">Notification Feed</div></div>', unsafe_allow_html=True)

    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    # Main split layout
    col_left, col_right = st.columns([1.6, 1])

    with col_left:
        st.markdown('<div class="section-header">Robotic Asset Fleet Status</div>', unsafe_allow_html=True)
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
                status_class = "badge-active" if status.lower() == "active" else ("badge-warning" if status.lower() == "maintenance" else "badge-neutral")

                with card_cols[idx % 2]:
                    st.markdown(
                        f"""
                        <div class="robot-card">
                            <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                                <strong style="font-size:16px; color:#1d1d1f;">{r.get('robot_name')}</strong>
                                <span class="status-badge {status_class}">{status}</span>
                            </div>
                            <div style="font-size:13px; color:#86868b; margin-bottom:4px;">
                                {r.get('manufacturer')} • {r.get('model')} • {r.get('location', 'Sector 1')}
                            </div>
                            <div style="font-size:13px; color:#86868b; margin-bottom:12px;">
                                Payload: {r.get('payload_capacity', 'N/A')} kg | Reach: {r.get('reach', 'N/A')} m
                            </div>
                            <div style="display:flex; justify-content:space-between; align-items:center; padding-top:10px; border-top:1px solid #f2f2f7;">
                                <span style="font-size:13px; color:#86868b;">Failure Risk:</span>
                                <strong style="font-size:14px; color:{'#c62828' if prob >= 0.8 else ('#b78103' if prob >= 0.5 else '#1b5e20')};">{prob_pct:.1f}%</strong>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
        else:
            st.info("No robotic assets registered yet.")

    with col_right:
        st.markdown('<div class="section-header">Recent High-Risk Predictions</div>', unsafe_allow_html=True)
        if predictions:
            recent_high_risk = [p for p in predictions if float(p.get("failure_probability", 0) or 0) >= 0.50]
            if not recent_high_risk:
                recent_high_risk = predictions[-4:]
            
            for pred in recent_high_risk[:4]:
                p_prob = float(pred.get("failure_probability", 0) or 0) * 100
                st.markdown(
                    f"""
                    <div style="background:#ffffff; border:1px solid #e5e5ea; border-radius:14px; padding:14px; margin-bottom:12px; box-shadow:0 2px 6px rgba(0,0,0,0.02);">
                        <div style="display:flex; justify-content:space-between;">
                            <strong style="color:#1d1d1f;">Robot {pred.get('robot_id')}</strong>
                            <span style="font-weight:600; color:{'#c62828' if p_prob >= 80 else '#b78103'};">{p_prob:.1f}% Risk</span>
                        </div>
                        <div style="font-size:13px; color:#b78103; margin-top:4px; font-weight:500;">Fault: {pred.get('predicted_fault', 'Protective Stop')}</div>
                        <div style="font-size:12px; color:#86868b; margin-top:4px;">{pred.get('recommendation', 'Inspect operating conditions.')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
        else:
            st.info("No prediction records generated yet.")

        st.markdown('<div class="section-header">Latest Telemetry Summary</div>', unsafe_allow_html=True)
        if telemetry:
            latest_t = telemetry[-1]
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                st.metric("Target Asset", f"Robot {latest_t.get('robot_id')}")
                st.metric("Joint 0 Current", f"{latest_t.get('Current_J0', 0):.2f} A")
                st.metric("Joint 0 Speed", f"{latest_t.get('Speed_J0', 0):.1f} deg/s")
            with t_col2:
                st.metric("Joint 0 Temperature", f"{latest_t.get('Temperature_T0', 0):.1f} °C")
                st.metric("Tool Current", f"{latest_t.get('Tool_current', 0):.2f} A")
                st.metric("Cycle Count", f"{latest_t.get('cycle', 0)}")
        else:
            st.info("No telemetry records available.")


# ============================================================
# 7. PAGE 2: ROBOTIC ASSETS (FULL CRUD)
# ============================================================

elif selected_page == "Robotic Assets":
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

            submit_new_robot = st.form_submit_button("Register Robot Arm", use_container_width=True)

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
        st.dataframe(df_robots, use_container_width=True, hide_index=True)

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

                    save_changes = st.form_submit_button("Save Changes", use_container_width=True)
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

                if st.button(f"Run AI Diagnostics on Robot {selected_robot_id}", use_container_width=True):
                    with st.spinner("Evaluating telemetry against Random Forest model..."):
                        diag, err = api.predict_for_robot(selected_robot_id)
                        if diag:
                            st.success(f"Result: {diag.get('predicted_fault')} ({float(diag.get('failure_probability', 0))*100:.1f}% failure probability)")
                            st.info(f"Recommendation: {diag.get('recommendation')}")
                        else:
                            st.error(f"Diagnostics error: {err}")

                st.markdown("---")
                if st.button(f"Delete Robot {selected_robot_id}", use_container_width=True):
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

            submit_sensor = st.form_submit_button("Provision Sensor", use_container_width=True)
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
        st.dataframe(df_sensors, use_container_width=True, hide_index=True)

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

                    if st.form_submit_button("Update Sensor", use_container_width=True):
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
                if st.button(f"Delete Sensor {sel_s_id}", use_container_width=True):
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

elif selected_page == "Telemetry and Charts":
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

            submit_telemetry = st.form_submit_button("Ingest Reading", use_container_width=True)
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
                st.line_chart(plot_df[current_cols], use_container_width=True)

        with tab_temp:
            temp_cols = [c for c in ["Temperature_T0", "Temperature_J1", "Temperature_J2", "Temperature_J3", "Temperature_J4", "Temperature_J5"] if c in plot_df.columns]
            if temp_cols:
                st.line_chart(plot_df[temp_cols], use_container_width=True)

        with tab_speed:
            speed_cols = [c for c in ["Speed_J0", "Speed_J1", "Speed_J2", "Speed_J3", "Speed_J4", "Speed_J5"] if c in plot_df.columns]
            if speed_cols:
                st.line_chart(plot_df[speed_cols], use_container_width=True)

        with tab_raw:
            # For raw table, allow up to 500 rows with pagination-friendly display
            raw_df = df_tel if selected_tel_robot == "All Robots" else df_tel[df_tel["robot_id"] == int(selected_tel_robot.replace("Robot ", ""))]
            st.caption(f"Showing {min(500, len(raw_df))} of {len(raw_df)} total records")
            st.dataframe(raw_df.tail(500).reset_index(drop=True), use_container_width=True, hide_index=True)

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

elif selected_page == "Predictive Analytics":
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

        if st.button("Evaluate Failure Risk", use_container_width=True):
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
                        <div style="font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.04em; color:#86868b;">
                            Diagnosis Result • Robot {diag_robot_id}
                        </div>
                        <h2 style="font-size:36px; margin:8px 0; color:#1d1d1f; font-weight:700;">
                            {prob_pct:.1f}% Failure Probability
                        </h2>
                        <div style="font-size:18px; font-weight:600; color:{'#c62828' if prob >= 0.8 else ('#b78103' if prob >= 0.5 else '#1b5e20')};">
                            Status: {fault}
                        </div>
                        <p style="font-size:14px; margin-top:12px; color:#515154;">
                            <strong>Recommendation:</strong> {recom}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                st.cache_data.clear()
            else:
                st.error(f"Evaluation failed: {err}")

    # TAB 2: INTERACTIVE ML SIMULATOR
    with tab_ml_sim:
        st.markdown("#### Interactive 20-Feature Random Forest Simulator")
        st.write("Tune arbitrary joint current, temperature, and speed parameters to observe model thresholds.")

        with st.form("ml_simulator_form"):
            sim_r_id = st.selectbox("Simulation Target Robot ID", [r["robot_id"] for r in robots] if robots else [1])

            scol1, scol2, scol3 = st.columns(3)
            with scol1:
                st.caption("Joint Currents (Amperes)")
                sim_cj0 = st.slider("Current J0", 0.0, 15.0, 3.2, 0.1)
                sim_cj1 = st.slider("Current J1", 0.0, 15.0, 4.5, 0.1)
                sim_cj2 = st.slider("Current J2", 0.0, 15.0, 5.0, 0.1)
                sim_cj3 = st.slider("Current J3", 0.0, 15.0, 2.1, 0.1)
                sim_cj4 = st.slider("Current J4", 0.0, 15.0, 1.8, 0.1)
                sim_cj5 = st.slider("Current J5", 0.0, 15.0, 1.2, 0.1)
            with scol2:
                st.caption("Joint Temperatures (°C)")
                sim_tt0 = st.slider("Temp T0", 20.0, 100.0, 55.0, 0.5)
                sim_tj1 = st.slider("Temp J1", 20.0, 100.0, 58.0, 0.5)
                sim_tj2 = st.slider("Temp J2", 20.0, 100.0, 62.0, 0.5)
                sim_tj3 = st.slider("Temp J3", 20.0, 100.0, 50.0, 0.5)
                sim_tj4 = st.slider("Temp J4", 20.0, 100.0, 48.0, 0.5)
                sim_tj5 = st.slider("Temp J5", 20.0, 100.0, 45.0, 0.5)
            with scol3:
                st.caption("Joint Speeds (deg/s) and Tool Load")
                sim_sj0 = st.slider("Speed J0", 0.0, 300.0, 150.0, 5.0)
                sim_sj1 = st.slider("Speed J1", 0.0, 300.0, 120.0, 5.0)
                sim_sj2 = st.slider("Speed J2", 0.0, 300.0, 130.0, 5.0)
                sim_sj3 = st.slider("Speed J3", 0.0, 300.0, 180.0, 5.0)
                sim_sj4 = st.slider("Speed J4", 0.0, 300.0, 200.0, 5.0)
                sim_sj5 = st.slider("Speed J5", 0.0, 300.0, 220.0, 5.0)
                sim_tc = st.slider("Tool Current", 0.0, 10.0, 1.5, 0.1)
                sim_cyc = st.slider("Cycle Number", 1.0, 500.0, 200.0, 1.0)

            run_sim = st.form_submit_button("Run Simulation", use_container_width=True)

            if run_sim:
                ml_payload = {
                    "robot_id": sim_r_id,
                    "Current_J0": sim_cj0, "Current_J1": sim_cj1, "Current_J2": sim_cj2, "Current_J3": sim_cj3, "Current_J4": sim_cj4, "Current_J5": sim_cj5,
                    "Temperature_T0": sim_tt0, "Temperature_J1": sim_tj1, "Temperature_J2": sim_tj2, "Temperature_J3": sim_tj3, "Temperature_J4": sim_tj4, "Temperature_J5": sim_tj5,
                    "Speed_J0": sim_sj0, "Speed_J1": sim_sj1, "Speed_J2": sim_sj2, "Speed_J3": sim_sj3, "Speed_J4": sim_sj4, "Speed_J5": sim_sj5,
                    "Tool_current": sim_tc, "cycle": sim_cyc
                }
                with st.spinner("Calculating ML inference..."):
                    sim_out, sim_err = api.predict_protective_stop_ml(ml_payload)

                if sim_out:
                    s_prob = float(sim_out.get("failure_probability", 0) or 0)
                    s_pct = s_prob * 100
                    st.markdown(
                        f"""
                        <div class="{'risk-banner-critical' if s_prob >= 0.5 else 'risk-banner-safe'}">
                            <h3 style="margin:0 0 8px 0; color:#1d1d1f;">Result: {sim_out.get('predicted_fault')}</h3>
                            <div style="font-size:28px; font-weight:700; color:{'#c62828' if s_prob >= 0.8 else ('#b78103' if s_prob >= 0.5 else '#1b5e20')};">
                                {s_pct:.1f}% Probability of Protective Stop
                            </div>
                            <p style="margin-top:10px; color:#515154;">Recommendation: {sim_out.get('recommendation')}</p>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    st.cache_data.clear()
                else:
                    st.error(f"Simulation failed: {sim_err}")

    # TAB 3: HISTORICAL PREDICTIONS LOG
    with tab_pred_history:
        st.markdown("#### Historical Predictions Audit Table")
        if predictions:
            df_pred = pd.DataFrame(predictions)
            st.dataframe(df_pred, use_container_width=True, hide_index=True)

            st.bar_chart(df_pred.set_index("robot_id")["failure_probability"], use_container_width=True)

            st.markdown("#### Remove Prediction Log")
            del_p_id = st.number_input("Prediction ID to Delete", min_value=1, step=1)
            if st.button("Delete Prediction"):
                ok, msg = api.delete_prediction(del_p_id)
                if ok:
                    st.success(f"Prediction {del_p_id} deleted.")
                    st.cache_data.clear()
                    st.rerun()
                else:
                    st.error(f"Delete failed: {msg}")
        else:
            st.info("No historical prediction logs.")


# ============================================================
# 11. PAGE 6: MAINTENANCE SCHEDULER
# ============================================================

elif selected_page == "Maintenance Scheduler":
    st.markdown(
        """
        <div class="main-header">
            <div>
                <h1 class="main-title">Maintenance Scheduler</h1>
                <p class="main-subtitle">Log preventive servicing, schedule calibrations, and manage technician assignments</p>
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

            submit_maint = st.form_submit_button("Record Entry", use_container_width=True)
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
        st.dataframe(df_maint, use_container_width=True, hide_index=True)

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

                    if st.form_submit_button("Update Record", use_container_width=True):
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
                if st.button(f"Delete Record {sel_m_id}", use_container_width=True):
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

            submit_inc = st.form_submit_button("Log Incident", use_container_width=True)
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

        st.dataframe(df_inc, use_container_width=True, hide_index=True)

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
                if st.button(toggle_action, use_container_width=True):
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
                if st.button(f"Delete Ticket {sel_inc_id}", use_container_width=True):
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

            submit_notif = st.form_submit_button("Send Notification", use_container_width=True)
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
            
            prio_color = "#c62828" if prio.lower() == "critical" else ("#b78103" if prio.lower() == "high" else "#0071e3")
            
            col_msg, col_actions = st.columns([3, 1])
            with col_msg:
                st.markdown(
                    f"""
                    <div style="background:#ffffff; border:1px solid #e5e5ea; border-left:4px solid {prio_color}; border-radius:12px; padding:14px; margin-bottom:10px; box-shadow:0 2px 6px rgba(0,0,0,0.02);">
                        <div style="display:flex; justify-content:space-between;">
                            <strong style="color:#1d1d1f;">Robot {n.get('robot_id')} • {n.get('alert_type')}</strong>
                            <span style="font-size:11px; font-weight:600; color:{prio_color}; text-transform:uppercase;">{prio} • {status}</span>
                        </div>
                        <div style="font-size:13px; color:#515154; margin-top:4px;">{n.get('message')}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            with col_actions:
                btn_c1, btn_c2 = st.columns(2)
                with btn_c1:
                    if status.lower() == "unread":
                        if st.button("Read", key=f"read_{nid}", use_container_width=True):
                            api.update_notification(nid, {"status": "Read"})
                            st.cache_data.clear()
                            st.rerun()
                with btn_c2:
                    if st.button("Delete", key=f"del_{nid}", use_container_width=True):
                        api.delete_notification(nid)
                        st.cache_data.clear()
                        st.rerun()
    else:
        st.info("No notifications in the system feed.")


# ============================================================
# 14. PAGE 9: HEALTH DIAGNOSTICS
# ============================================================

elif selected_page == "Health Diagnostics":
    st.markdown(
        """
        <div class="main-header">
            <div>
                <h1 class="main-title">Health Diagnostic Station</h1>
                <p class="main-subtitle">Compute real-time holistic health scores based on thermal, vibration, current, and torque telemetry</p>
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

        if st.button("Calculate Health Score", use_container_width=True):
            with st.spinner(f"Computing diagnostic health matrix for Robot {target_h_robot}..."):
                health_data, health_err = api.get_robot_health(target_h_robot)

            if health_data:
                score = float(health_data.get("health_score", 100))
                status_text = health_data.get("health_status", "Excellent")

                h_banner = "risk-banner-safe" if score >= 75 else "risk-banner-critical"

                st.markdown(
                    f"""
                    <div class="{h_banner}">
                        <div style="font-size:12px; font-weight:600; text-transform:uppercase; letter-spacing:0.04em; color:#86868b;">
                            Robot {target_h_robot} Health Diagnosis
                        </div>
                        <h1 style="font-size:44px; margin:8px 0; color:#1d1d1f; font-weight:700;">
                            {score:.0f} / 100
                        </h1>
                        <div style="font-size:18px; font-weight:600; color:{'#1b5e20' if score >= 75 else ('#b78103' if score >= 60 else '#c62828')};">
                            Condition: {status_text}
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

                sm1, sm2, sm3, sm4 = st.columns(4)
                with sm1:
                    st.metric("Thermal Reading", f"{health_data.get('temperature', 0):.1f} °C")
                with sm2:
                    st.metric("Vibration", f"{health_data.get('vibration', 0):.2f} mm/s")
                with sm3:
                    st.metric("Motor Current", f"{health_data.get('motor_current', 0):.2f} A")
                with sm4:
                    st.metric("Torque / Load", f"{health_data.get('torque', 0):.1f} Nm")

            else:
                st.error(f"Health score computation failed: {health_err}")
    else:
        st.info("No robots available to run health diagnostics.")


# ============================================================
# 15. PAGE 10: USER MANAGEMENT
# ============================================================

elif selected_page == "User Management":
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

            submit_u = st.form_submit_button("Create User Profile", use_container_width=True)
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
        st.dataframe(df_users, use_container_width=True, hide_index=True)

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

                    if st.form_submit_button("Update User Profile", use_container_width=True):
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
                if st.button(f"Delete User {sel_u_id}", use_container_width=True):
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
    <div style="margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid #e5e5ea; text-align: center; font-size: 12px; color: #86868b;">
        RoboPulse AI • Predictive Robot Arm Monitoring and Maintenance Platform
    </div>
    """,
    unsafe_allow_html=True,
)