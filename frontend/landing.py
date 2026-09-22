import streamlit as st
import pandas as pd
import numpy as np


def show_landing():
    # -----------------------------
    # Apple Landing Page Styling
    # -----------------------------
    st.markdown(
        """
        <style>
        /* Apple typography & light canvas */
        html, body, [class*="css"] {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            letter-spacing: -0.01em;
        }

        /* Hide Streamlit's accessibility shortcut and heading permalink controls. */
        [data-testid="stHeaderActionElements"],
        .stHeadingWithActionElements a,
        a.header-anchor,
        a[aria-label="Link to this heading"],
        button[aria-label="Copy link to heading"],
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

        .stApp {
            background-color: #FFFFFF !important;
            color: #1A1A1A !important;
        }

        /* Top Navigation Bar */
        .apple-nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 24px;
            background: #FFFFFF;
            border-bottom: 1px solid #EEECE8;
            position: sticky;
            top: 0;
            z-index: 100;
            margin-bottom: 2rem;
            border-radius: 6px;
        }
        .apple-nav-logo {
            font-size: 18px;
            font-weight: 700;
            color: #1A1A1A !important;
            letter-spacing: -0.02em;
            display: flex;
            align-items: center;
            gap: 8px;
        }
        .apple-nav-links {
            display: flex;
            gap: 24px;
            font-size: 13px;
            font-weight: 500;
            color: #6A6A6A;
        }

        /* Hero Section */
        .hero-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            text-align: center;
            max-width: 860px;
            margin: 2rem auto 2.5rem auto;
            padding: 0 20px;
            width: 100%;
        }
        .hero-badge {
            display: inline-block;
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: #E05C1A !important;
            background: #FFF4EC;
            border: 1px solid #F4D2B8;
            padding: 4px 10px;
            border-radius: 4px;
            margin-bottom: 14px;
            text-align: center;
        }
        .hero-headline {
            font-size: 46px;
            font-weight: 700;
            color: #1A1A1A !important;
            letter-spacing: -0.03em;
            line-height: 1.15;
            margin: 0 0 16px 0;
            text-align: center;
        }
        .hero-subhead {
            font-size: 17px;
            color: #6A6A6A !important;
            font-weight: 400;
            line-height: 1.5;
            margin: 0 auto 28px auto;
            max-width: 720px;
            text-align: center;
            width: 100%;
        }

        /* Primary Action Buttons (Burnt Industrial Orange) */
        .btn-apple-primary {
            display: inline-block;
            background-color: #E05C1A !important;
            color: #FFFFFF !important;
            padding: 10px 24px;
            border-radius: 6px;
            font-size: 14px;
            font-weight: 600;
            text-decoration: none;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05);
            transition: all 0.15s ease;
            border: 1px solid #E05C1A;
            cursor: pointer;
        }
        .btn-apple-primary:hover {
            background-color: #C84E12 !important;
            border-color: #C84E12 !important;
            transform: none;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
        }

        /* Bento Grid Section */
        .bento-section {
            background-color: #FFFFFF;
            padding: 3.5rem 2rem;
            border-radius: 8px;
            border: 1px solid #EEECE8;
            margin: 3rem 0;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
        }
        .bento-header {
            text-align: center;
            margin-bottom: 2.5rem;
        }
        .bento-title {
            font-size: 32px;
            font-weight: 700;
            color: #1A1A1A !important;
            letter-spacing: -0.025em;
            margin: 0 0 8px 0;
        }
        .bento-subtitle {
            font-size: 15px;
            color: #6A6A6A !important;
            margin: 0;
        }

        /* Bento Card */
        .bento-card {
            background: #FFFFFF !important;
            border: 1px solid #EEECE8 !important;
            border-radius: 8px;
            padding: 24px;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
            height: 270px;
            min-height: 270px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: border-color 0.15s ease, box-shadow 0.15s ease;
        }
        .bento-card:hover {
            border-color: #E05C1A !important;
            box-shadow: 0 2px 6px rgba(198, 93, 33, 0.08);
        }
        .bento-tag {
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: #E05C1A !important;
            margin-bottom: 6px;
        }
        .bento-card-title {
            font-size: 18px;
            font-weight: 700;
            color: #1A1A1A !important;
            letter-spacing: -0.02em;
            margin: 0 0 6px 0;
        }
        .bento-card-desc {
            font-size: 13px;
            color: #6A6A6A !important;
            line-height: 1.5;
            margin: 0 0 14px 0;
        }
        .bento-stat-huge {
            font-size: 40px;
            font-weight: 700;
            color: #1A1A1A !important;
            letter-spacing: -0.03em;
            margin: 6px 0;
        }
        .bento-stat-label {
            font-size: 12px;
            color: #4A9B6F !important;
            font-weight: 600;
        }

        /* Floating Hero Metric Cards */
        .hero-metric-row {
            display: flex;
            justify-content: center;
            gap: 16px;
            margin: 2rem 0 1.5rem 0;
            flex-wrap: wrap;
        }
        .hero-card {
            background: #FFFFFF !important;
            border: 1px solid #EEECE8 !important;
            border-radius: 8px;
            padding: 14px 20px;
            text-align: left;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.03);
            min-width: 170px;
        }
        .hero-card-label {
            font-size: 11px;
            color: #6A6A6A !important;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.04em;
        }
        .hero-card-val {
            font-size: 24px;
            font-weight: 700;
            color: #1A1A1A !important;
            margin: 4px 0 2px 0;
        }
        .hero-card-sub {
            font-size: 12px;
            color: #4A9B6F !important;
            font-weight: 500;
        }

        /* Footer */
        .apple-footer {
            border-top: 1px solid #EEECE8;
            padding: 2.5rem 0 2rem 0;
            text-align: center;
            font-size: 12px;
            color: #6A6A6A;
        }
        .apple-footer {
            border-top: 1px solid #262626;
            padding: 3rem 0 2rem 0;
            text-align: center;
            font-size: 12px;
            color: #737373;
            margin-top: 4rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------
    # 1. TOP NAVIGATION
    # -----------------------------
    st.markdown(
        """
        <div style="display:flex; align-items:center; justify-content:space-between; padding:14px 24px; background:#FFFFFF; border:1px solid #EEECE8; margin-bottom:1.5rem; border-radius:6px;">
        <div style="display:flex; align-items:center; gap:8px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <rect width="24" height="24" rx="4" fill="#E05C1A"/>
                <circle cx="12" cy="12" r="4" fill="#FFFFFF"/>
                <path d="M12 4v4m0 8v4m-8-8h4m8 0h4" stroke="#FFFFFF" stroke-width="2"/>
            </svg>
            <span style="font-size:18px; font-weight:700; color:#1A1A1A; letter-spacing:-0.02em;">RoboPulse</span>
        </div>
        <div style="font-size:13px; color:#6A6A6A;">Industrial Robotics Predictive Intelligence Platform</div>
    </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------
    # 2. HERO SECTION
    # -----------------------------
    st.markdown(
        """
        <div class="hero-container">
            <div class="hero-badge">Predictive Intelligence Platform</div>
            <h1 class="hero-headline">RoboPulse<br>Intelligent robotics maintenance</h1>
            <p class="hero-subhead">Advanced multi-axis predictive telemetry powered by real-time machine learning</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Hero Action Buttons
    c_btn1, c_btn2, c_btn3 = st.columns([1.5, 1.2, 1.5])
    with c_btn2:
        if st.button("Open Platform", key="hero_open_platform", use_container_width=True):
            st.session_state["auth_mode"] = "signin"
            st.rerun()

    # Hero Telemetry Metric Highlights
    st.markdown(
        """
        <div class="hero-metric-row">
            <div class="hero-card">
                <div class="hero-card-label">Hardware Precision</div>
                <div class="hero-card-val">6 Joints</div>
                <div class="hero-card-sub">Synchronized</div>
            </div>
            <div class="hero-card">
                <div class="hero-card-label">ML Accuracy</div>
                <div class="hero-card-val">99.4%</div>
                <div class="hero-card-sub">Random Forest</div>
            </div>
            <div class="hero-card">
                <div class="hero-card-label">Failure Prevention</div>
                <div class="hero-card-val">0 Fault</div>
                <div class="hero-card-sub">Protective Stop Prevention</div>
            </div>
            <div class="hero-card">
                <div class="hero-card-label">Health Index</div>
                <div class="hero-card-val">99.8%</div>
                <div class="hero-card-sub">Fleet Reliability</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # -----------------------------
    # 3. BENTO GRID FEATURES SECTION
    # -----------------------------
    st.markdown(
        """
        <div class="bento-section">
            <div class="bento-header">
                <h2 class="bento-title">Engineered for continuous reliability</h2>
                <p class="bento-subtitle">Every joint. Every millisecond. Measured and forecasted</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    b_col1, b_col2 = st.columns(2)

    with b_col1:
        # Card 1: Waveforms embedded directly in card
        st.markdown(
            """
            <div class="bento-card">
                <div>
                    <div class="bento-tag">High Frequency Waveforms</div>
                    <div class="bento-card-title">6-Joint Sinusoidal Telemetry</div>
                    <div class="bento-card-desc">Continuous monitoring of joint currents, thermal curves, angular speeds, and tool load parameters.</div>
                </div>
                <div style="margin-top: 10px;">
                    <svg viewBox="0 0 380 65" width="100%" height="65" style="overflow: visible;">
                        <defs>
                            <linearGradient id="wave1" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stop-color="#E05C1A" stop-opacity="0.9"/>
                                <stop offset="100%" stop-color="#E8A020" stop-opacity="0.9"/>
                            </linearGradient>
                            <linearGradient id="wave2" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stop-color="#4A9B6F" stop-opacity="0.9"/>
                                <stop offset="100%" stop-color="#84A98C" stop-opacity="0.85"/>
                            </linearGradient>
                            <linearGradient id="wave3" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stop-color="#D94040" stop-opacity="0.8"/>
                                <stop offset="100%" stop-color="#E05C1A" stop-opacity="0.8"/>
                            </linearGradient>
                        </defs>
                        <path d="M 0 32 Q 45 5, 95 32 T 190 32 T 285 32 T 380 32" fill="none" stroke="url(#wave1)" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M 0 42 Q 45 60, 95 42 T 190 42 T 285 42 T 380 42" fill="none" stroke="url(#wave2)" stroke-width="2" stroke-linecap="round" stroke-dasharray="4 2"/>
                        <path d="M 0 25 Q 45 45, 95 25 T 190 25 T 285 25 T 380 25" fill="none" stroke="url(#wave3)" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                    <div style="display: flex; gap: 14px; font-size: 11px; color: #6A6A6A; margin-top: 6px;">
                        <span><span style="color:#FFFFFF;">●</span> Joint 1 Current</span>
                        <span><span style="color: #E5E5E5;">●</span> Joint 2 Current</span>
                        <span><span style="color:#737373;">●</span> Joint 3 Current</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with b_col2:
        # Card 2: ML Diagnostic Engine
        st.markdown(
            """
            <div class="bento-card">
                <div>
                    <div class="bento-tag">Predictive Inference</div>
                    <div class="bento-card-title">Random Forest AI Engine</div>
                    <div class="bento-card-desc">Scikit-Learn classifier trained on real industrial stop datasets, projecting protective stops before hardware wear occurs.</div>
                </div>
                <div>
                    <div class="bento-stat-huge" style="color: #1A1A1A;">&lt; 0.05s</div>
                    <div class="bento-stat-label" style="color: #6A6A6A; font-weight: 500;">Inference Latency</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)

    b_sub1, b_sub2 = st.columns(2)

    with b_sub1:
        # Card 3: Maintenance Operations
        st.markdown(
            """
            <div class="bento-card">
                <div>
                    <div class="bento-tag">Lifecycle Management</div>
                    <div class="bento-card-title">Scheduled Maintenance and Timelines</div>
                    <div class="bento-card-desc">Comprehensive technician assignment, calibration queues, and automated incident resolution workflows.</div>
                </div>
                <div style="margin-top: 6px;">
                    <div style="display:flex; justify-content:space-between; font-size:12px; color: #6A6A6A; margin-bottom:6px; font-weight:500;">
                        <span>Next Target: Joint Calibration</span>
                        <span style="color:#E05C1A; font-weight:600;">94% On Schedule</span>
                    </div>
                    <div style="width:100%; height:6px; background:#EAE8E4; border-radius:3px; overflow:hidden; display:flex; margin-bottom:12px;">
                        <div style="width:65%; background:#4A9B6F;"></div>
                        <div style="width:20%; background:#E8A020;"></div>
                        <div style="width:15%; background:#E05C1A;"></div>
                    </div>
                    <div style="display:flex; flex-wrap:wrap; gap:6px;">
                        <span style="background:#EBF5EE; color:#2E7D4E; padding:4px 10px; border-radius:4px; font-size:11px; font-weight:600; border:1px solid #B8E0C8;">Preventive</span>
                        <span style="background:#FFF4EC; color:#E05C1A; padding:4px 10px; border-radius:4px; font-size:11px; font-weight:600; border:1px solid #F4D2B8;">Calibration</span>
                        <span style="background:#FEF6E9; color:#B26A00; padding:4px 10px; border-radius:4px; font-size:11px; font-weight:600; border:1px solid #F8D8A0;">Inspection</span>
                        <span style="background:#F8F7F4; color:#6A6A6A; padding:4px 10px; border-radius:4px; font-size:11px; font-weight:600; border:1px solid #E2E0DA;">Active Queue</span>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with b_sub2:
        # Card 4: Health Scoring
        st.markdown(
            """
            <div class="bento-card">
                <div>
                    <div class="bento-tag">Holistic Condition</div>
                    <div class="bento-card-title">Precision Health Scoring</div>
                    <div class="bento-card-desc">Dynamic multi-factor health matrix evaluating thermal limits, vibration frequencies, and motor current draw.</div>
                </div>
                <div>
                    <div class="bento-stat-huge" style="color: #1A1A1A;">99.8%</div>
                    <div class="bento-stat-label">Fleet Operational Health</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # -----------------------------
    # 4. BOTTOM CTA SECTION
    # -----------------------------
    st.markdown(
        """
        <div style="text-align: center; max-width: 600px; margin: 5rem auto 3rem auto; padding: 0 16px;">
            <h2 style="font-size: 32px; font-weight: 700; color: #1A1A1A; letter-spacing: -0.03em; margin-bottom: 12px;">
                Ready to monitor your fleet?
            </h2>
            <p style="font-size: 16px; color: #6A6A6A; margin-bottom: 24px;">
                Sign in with your operator credentials to access real-time telemetry, predictive analytics, and automated maintenance.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    c_foot1, c_foot2, c_foot3 = st.columns([1.5, 1.2, 1.5])
    with c_foot2:
        if st.button("Sign In to Platform", key="footer_signin_btn", use_container_width=True):
            st.session_state["auth_mode"] = "signin"
            st.rerun()

    # Footer
    st.markdown(
        """
        <div class="apple-footer">
            RoboPulse AI • Predictive Intelligence for Industrial Robotics
        </div>
        """,
        unsafe_allow_html=True,
    )
