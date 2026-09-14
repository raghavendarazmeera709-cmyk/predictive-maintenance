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
            background-color: #ffffff;
            color: #1d1d1f;
        }

        /* Top Navigation Bar */
        .apple-nav {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 24px;
            background: rgba(255, 255, 255, 0.85);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border-bottom: 1px solid #e5e5ea;
            position: sticky;
            top: 0;
            z-index: 100;
            margin-bottom: 2rem;
        }
        .apple-nav-logo {
            font-size: 17px;
            font-weight: 700;
            color: #1d1d1f;
            letter-spacing: -0.02em;
        }
        .apple-nav-links {
            display: flex;
            gap: 28px;
            font-size: 13px;
            font-weight: 400;
            color: #515154;
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
            font-size: 12px;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: #86868b;
            margin-bottom: 12px;
            text-align: center;
        }
        .hero-headline {
            font-size: 54px;
            font-weight: 700;
            color: #1d1d1f;
            letter-spacing: -0.035em;
            line-height: 1.1;
            margin: 0 0 16px 0;
            text-align: center;
        }
        .hero-subhead {
            font-size: 19px;
            color: #86868b;
            font-weight: 400;
            line-height: 1.5;
            margin: 0 auto 28px auto;
            max-width: 720px;
            text-align: center;
            width: 100%;
        }

        /* Apple Action Buttons */
        .btn-apple-primary {
            display: inline-block;
            background-color: #0071e3;
            color: #ffffff !important;
            padding: 11px 26px;
            border-radius: 980px;
            font-size: 15px;
            font-weight: 500;
            text-decoration: none;
            box-shadow: 0 2px 8px rgba(0, 113, 227, 0.25);
            transition: all 0.2s ease;
            border: none;
            cursor: pointer;
        }
        .btn-apple-primary:hover {
            background-color: #0077ed;
            box-shadow: 0 4px 14px rgba(0, 113, 227, 0.35);
        }

        /* Bento Grid Section */
        .bento-section {
            background-color: #f5f5f7;
            padding: 4.5rem 2rem;
            border-radius: 30px;
            margin: 3rem 0;
        }
        .bento-header {
            text-align: center;
            margin-bottom: 3rem;
        }
        .bento-title {
            font-size: 38px;
            font-weight: 700;
            color: #1d1d1f;
            letter-spacing: -0.03em;
            margin: 0 0 10px 0;
        }
        .bento-subtitle {
            font-size: 17px;
            color: #86868b;
            margin: 0;
        }

        /* Bento Card */
        .bento-card {
            background: #ffffff;
            border: 1px solid #e5e5ea;
            border-radius: 20px;
            padding: 28px;
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.02);
            height: 270px;
            min-height: 270px;
            box-sizing: border-box;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .bento-card:hover {
            transform: translateY(-3px);
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.05);
        }
        .bento-tag {
            font-size: 11px;
            font-weight: 600;
            letter-spacing: 0.04em;
            text-transform: uppercase;
            color: #86868b;
            margin-bottom: 8px;
        }
        .bento-card-title {
            font-size: 20px;
            font-weight: 700;
            color: #1d1d1f;
            letter-spacing: -0.02em;
            margin: 0 0 8px 0;
        }
        .bento-card-desc {
            font-size: 14px;
            color: #86868b;
            line-height: 1.5;
            margin: 0 0 16px 0;
        }
        .bento-stat-huge {
            font-size: 46px;
            font-weight: 800;
            color: #1d1d1f;
            letter-spacing: -0.03em;
            margin: 8px 0;
        }
        .bento-stat-label {
            font-size: 13px;
            color: #1b5e20;
            font-weight: 600;
        }

        /* Floating Hero Metric Cards */
        .hero-metric-row {
            display: flex;
            justify-content: center;
            gap: 18px;
            margin: 2.5rem 0 1.5rem 0;
            flex-wrap: wrap;
        }
        .hero-card {
            background: #ffffff;
            border: 1px solid #e5e5ea;
            border-radius: 16px;
            padding: 16px 22px;
            text-align: left;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.04);
            min-width: 170px;
        }
        .hero-card-label {
            font-size: 11px;
            color: #86868b;
            text-transform: uppercase;
            font-weight: 600;
            letter-spacing: 0.04em;
        }
        .hero-card-val {
            font-size: 24px;
            font-weight: 700;
            color: #1d1d1f;
            margin: 4px 0 2px 0;
        }
        .hero-card-sub {
            font-size: 12px;
            color: #1b5e20;
            font-weight: 500;
        }

        /* Footer */
        .apple-footer {
            border-top: 1px solid #e5e5ea;
            padding: 3rem 0 2rem 0;
            text-align: center;
            font-size: 12px;
            color: #86868b;
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
        <div style="display:flex; align-items:center; justify-content:space-between; padding:12px 0 20px 0; border-bottom:1px solid #f2f2f7; margin-bottom:1.5rem;">
            <div style="font-size: 19px; font-weight: 700; color: #1d1d1f; letter-spacing: -0.02em;">
                RoboPulse
            </div>
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
                                <stop offset="0%" stop-color="#0071e3" stop-opacity="0.8"/>
                                <stop offset="100%" stop-color="#30b0c7" stop-opacity="0.9"/>
                            </linearGradient>
                            <linearGradient id="wave2" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stop-color="#30b0c7" stop-opacity="0.7"/>
                                <stop offset="100%" stop-color="#34c759" stop-opacity="0.8"/>
                            </linearGradient>
                            <linearGradient id="wave3" x1="0%" y1="0%" x2="100%" y2="0%">
                                <stop offset="0%" stop-color="#ff9500" stop-opacity="0.7"/>
                                <stop offset="100%" stop-color="#ff3b30" stop-opacity="0.8"/>
                            </linearGradient>
                        </defs>
                        <path d="M 0 32 Q 45 5, 95 32 T 190 32 T 285 32 T 380 32" fill="none" stroke="url(#wave1)" stroke-width="2.5" stroke-linecap="round"/>
                        <path d="M 0 42 Q 45 60, 95 42 T 190 42 T 285 42 T 380 42" fill="none" stroke="url(#wave2)" stroke-width="2" stroke-linecap="round" stroke-dasharray="4 2"/>
                        <path d="M 0 25 Q 45 45, 95 25 T 190 25 T 285 25 T 380 25" fill="none" stroke="url(#wave3)" stroke-width="2" stroke-linecap="round"/>
                    </svg>
                    <div style="display: flex; gap: 14px; font-size: 11px; color: #86868b; margin-top: 6px;">
                        <span><span style="color:#0071e3;">●</span> Joint 1 Current</span>
                        <span><span style="color:#30b0c7;">●</span> Joint 2 Current</span>
                        <span><span style="color:#ff3b30;">●</span> Joint 3 Current</span>
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
                    <div class="bento-stat-huge" style="color: #0071e3;">&lt; 0.05s</div>
                    <div class="bento-stat-label" style="color: #86868b; font-weight: 500;">Inference Latency</div>
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
                    <div style="display:flex; justify-content:space-between; font-size:12px; color:#515154; margin-bottom:6px; font-weight:500;">
                        <span>Next Target: Joint Calibration</span>
                        <span style="color:#0071e3; font-weight:600;">94% On Schedule</span>
                    </div>
                    <div style="width:100%; height:6px; background:#e5e5ea; border-radius:980px; overflow:hidden; display:flex; margin-bottom:12px;">
                        <div style="width:65%; background:#0071e3;"></div>
                        <div style="width:20%; background:#34c759;"></div>
                        <div style="width:15%; background:#e5e5ea;"></div>
                    </div>
                    <div style="display:flex; flex-wrap:wrap; gap:6px;">
                        <span style="background:#e8f5e9; color:#1b5e20; padding:4px 10px; border-radius:980px; font-size:11px; font-weight:600; border:1px solid #c8e6c9;">Preventive</span>
                        <span style="background:#fff8e1; color:#b78103; padding:4px 10px; border-radius:980px; font-size:11px; font-weight:600; border:1px solid #ffe082;">Calibration</span>
                        <span style="background:#f5f5f7; color:#515154; padding:4px 10px; border-radius:980px; font-size:11px; font-weight:600; border:1px solid #e5e5ea;">Inspection</span>
                        <span style="background:#f0f7ff; color:#0071e3; padding:4px 10px; border-radius:980px; font-size:11px; font-weight:600; border:1px solid #bae0ff;">Active Queue</span>
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
                    <div class="bento-stat-huge" style="color: #1b5e20;">99.8%</div>
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
            <h2 style="font-size: 36px; font-weight: 700; color: #1d1d1f; letter-spacing: -0.03em; margin-bottom: 12px;">
                Ready to monitor your fleet?
            </h2>
            <p style="font-size: 16px; color: #86868b; margin-bottom: 24px;">
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
