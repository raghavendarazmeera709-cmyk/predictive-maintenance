import streamlit as st
from api import login_user, register_user, BASE_URL
from landing import show_landing


def show_login():
    if "auth_mode" not in st.session_state:
        st.session_state["auth_mode"] = "landing"

    # -----------------------------
    # MODE 0: LANDING PAGE
    # -----------------------------
    if st.session_state["auth_mode"] == "landing":
        show_landing()
        return

    # -----------------------------
    # Apple ID / Store Theme Styling
    # -----------------------------
    st.markdown(
        """
        <style>
                /* Light Industrial Orange Canvas */
        html, body, [class*="css"] {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            letter-spacing: -0.01em;
        }

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

        .stApp {
            background-color: #F8F7F4 !important;
            color: #1A1A1A !important;
        }

        /* Top Bar */
        .apple-topbar {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 14px 20px;
            background-color: #FFFFFF;
            border-bottom: 1px solid #EEECE8;
            margin-bottom: 2rem;
        }

        /* Top spacing */
        .login-wrapper {
            max-width: 440px;
            margin: 2.5rem auto 1rem auto;
            text-align: center;
        }

        /* Title */
        .apple-title {
            font-size: 26px;
            font-weight: 700;
            color: #1A1A1A !important;
            letter-spacing: -0.02em;
            margin-bottom: 1.5rem;
            line-height: 1.2;
            text-align: center;
        }

        /* Industrial Links */
        .apple-link {
            color: #E05C1A !important;
            text-decoration: none;
            font-size: 14px;
            font-weight: 500;
            transition: color 0.15s ease;
        }
        .apple-link:hover {
            text-decoration: underline;
            color: #C84E12 !important;
        }

        /* Form Container - Clean White Card */
        [data-testid="stForm"] {
            background: #FFFFFF !important;
            border: 1px solid #EEECE8 !important;
            border-radius: 8px !important;
            padding: 28px !important;
            box-shadow: 0 1px 3px rgba(0, 0, 0, 0.04) !important;
        }

        /* Styled Inputs */
        .stTextInput > div > div > input {
            background-color: #FFFFFF !important;
            color: #1A1A1A !important;
            border: 1px solid #EEECE8 !important;
            border-radius: 6px !important;
            font-size: 14px !important;
            padding: 10px 14px !important;
            height: 44px !important;
            transition: all 0.15s ease !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #E05C1A !important;
            box-shadow: 0 0 0 2px rgba(198, 93, 33, 0.15) !important;
        }

        /* Submit Button (Burnt Industrial Orange) */
        .stButton > button, .stFormSubmitButton > button {
            background-color: #E05C1A !important;
            color: #FFFFFF !important;
            border: 1px solid #E05C1A !important;
            border-radius: 6px !important;
            font-size: 14px !important;
            font-weight: 600 !important;
            padding: 10px 20px !important;
            height: 42px !important;
            box-shadow: 0 1px 2px rgba(0, 0, 0, 0.05) !important;
            transition: all 0.15s ease !important;
            margin-top: 6px !important;
        }

        .stButton > button:hover, .stFormSubmitButton > button:hover {
            background-color: #C84E12 !important;
            border-color: #C84E12 !important;
            transform: none !important;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08) !important;
        }

        /* Checkbox styling */
        [data-testid="stCheckbox"] {
            display: flex;
            justify-content: center;
            margin: 1rem 0;
            color: #6A6A6A !important;
            font-size: 13px !important;
        }

        /* Demo credentials subtle card */
        .demo-subtle {
            text-align: center;
            font-size: 12px;
            color: #6A6A6A;
            margin-top: 1.8rem;
            padding: 14px;
            background: #FFFFFF;
            border: 1px solid #EEECE8;
            border-radius: 6px;
            line-height: 1.6;
        }
        .demo-subtle code {
            color: #1A1A1A;
            background: #F8F7F4;
            border: 1px solid #EEECE8;
            padding: 2px 6px;
            border-radius: 4px;
            font-weight: 600;
        }
        .apple-switch-btn > div > button {
            background-color: transparent !important;
            color: #E05C1A !important;
            border: none !important;
            box-shadow: none !important;
            font-size: 14px !important;
            font-weight: 500 !important;
            padding: 8px 16px !important;
            margin-top: 4px !important;
        }
        .apple-switch-btn > div > button:hover {
            color: #C84E12 !important;
            text-decoration: underline !important;
            background-color: transparent !important;
            box-shadow: none !important;
        }</style>
        """,
        unsafe_allow_html=True,
    )

    # Clean Top Bar
    st.markdown(
        """
        <div style="display:flex; align-items:center; justify-content:space-between; padding:14px 20px; background:#FFFFFF; border-bottom:1px solid #EEECE8; margin-bottom:1.5rem; border-radius:6px;">
        <div style="display:flex; align-items:center; gap:8px;">
            <svg width="22" height="22" viewBox="0 0 24 24" fill="none">
                <rect width="24" height="24" rx="4" fill="#E05C1A"/>
                <circle cx="12" cy="12" r="4" fill="#FFFFFF"/>
                <path d="M12 4v4m0 8v4m-8-8h4m8 0h4" stroke="#FFFFFF" stroke-width="2"/>
            </svg>
            <span style="font-size:18px; font-weight:700; color:#1A1A1A; letter-spacing:-0.02em;">RoboPulse</span>
        </div>
        <span style="font-size:12px; font-weight:500; color:#6A6A6A; background:#F8F7F4; padding:4px 8px; border-radius:4px; border:1px solid #EEECE8;">Enterprise Portal</span>
    </div>
        """,
        unsafe_allow_html=True,
    )

    # Layout Column Centering
    _, col_center, _ = st.columns([1, 1.4, 1])

    with col_center:
        # -----------------------------
        # MODE 1: SIGN IN
        # -----------------------------
        if st.session_state["auth_mode"] == "signin":
            st.markdown(
                """
                <div class="login-wrapper">
                    <div class="apple-title">Sign in to RoboPulse</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.form("apple_signin_form"):
                email = st.text_input(
                    "Email or Phone Number",
                    placeholder="Email or Phone Number",
                    label_visibility="collapsed",
                )
                password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Password",
                    label_visibility="collapsed",
                )

                remember = st.checkbox("Remember me", value=True)

                submit_login = st.form_submit_button("Continue", use_container_width=True)

                if submit_login:
                    if not email or not password:
                        st.warning("Please enter your email and password.")
                    else:
                        with st.spinner("Signing in..."):
                            data, err = login_user(email, password)

                        if data and "access_token" in data:
                            st.session_state["logged_in"] = True
                            st.session_state["access_token"] = data["access_token"]
                            st.session_state["user_id"] = data.get("user_id")
                            st.session_state["full_name"] = data.get("full_name", "Operator")
                            st.session_state["email"] = data.get("email", email)
                            st.session_state["role"] = data.get("role", "Operator")

                            st.success(f"Signed in as {data.get('full_name')}")
                            st.rerun()
                        else:
                            st.error(f"Sign in failed: {err or 'Invalid email or password'}")

            # Apple ID Footer links
            st.markdown(
                """
                <div style="text-align: center; margin-top: 1.2rem; margin-bottom: 1rem;">
                    <div>
                        <a href="#forgot" class="apple-link">Forgotten your password? &#8599;</a>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            # Separate Create Account button
            if st.button("Create Account", key="switch_to_register", use_container_width=True):
                st.session_state["auth_mode"] = "register"
                st.rerun()

            # Subtle demo credentials
            st.markdown(
                """
                <div class="demo-subtle">
                    Default Credentials<br>
                    Administrator: <code>admin@test.com</code> / <code>Admin@123</code><br>
                    Operator: <code>user1@factoryops.com</code> / <code>admin123</code>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # -----------------------------
        # MODE 2: CREATE ACCOUNT
        # -----------------------------
        elif st.session_state["auth_mode"] == "register":
            st.markdown(
                """
                <div class="login-wrapper">
                    <div class="apple-title">Create Your Account</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

            with st.form("apple_register_form"):
                reg_name = st.text_input("Full Name", placeholder="Full Name", label_visibility="collapsed")
                reg_email = st.text_input("Email", placeholder="name@example.com", label_visibility="collapsed")
                reg_phone = st.text_input("Phone Number (Optional)", placeholder="Phone Number (Optional)", label_visibility="collapsed")
                reg_pwd = st.text_input("Password", type="password", placeholder="Password", label_visibility="collapsed")
                reg_confirm = st.text_input("Confirm Password", type="password", placeholder="Confirm Password", label_visibility="collapsed")

                submit_register = st.form_submit_button("Create Account", use_container_width=True)

                if submit_register:
                    if not reg_name or not reg_email or not reg_pwd:
                        st.warning("Please complete all required fields.")
                    elif reg_pwd != reg_confirm:
                        st.error("Passwords do not match.")
                    else:
                        with st.spinner("Creating account..."):
                            reg_data, reg_err = register_user(
                                full_name=reg_name,
                                email=reg_email,
                                password=reg_pwd,
                                confirm_password=reg_confirm,
                                phone=reg_phone,
                            )

                        if reg_data:
                            st.success(f"Account created for {reg_data.get('full_name')}. You can now sign in.")
                            st.session_state["auth_mode"] = "signin"
                            st.rerun()
                        else:
                            st.error(f"Registration failed: {reg_err or 'Unable to complete registration'}")

            st.markdown("<div style='height: 10px;'></div>", unsafe_allow_html=True)
            # Separate Sign In button
            if st.button("Sign In", key="switch_to_signin", use_container_width=True):
                st.session_state["auth_mode"] = "signin"
                st.rerun()

