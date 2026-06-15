
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import hashlib
import os
import random
import string
from datetime import datetime
from supabase import create_client
# This reads the keys from your hidden .env file locally, 
# or from the deployment platform settings when hosted!
URL = os.environ.get("SUPABASE_URL")
KEY = os.environ.get("SUPABASE_KEY")

supabase = create_client(URL, KEY)
try:
    supabase = create_client(URL, KEY)
except Exception as e:
    st.error(f"Failed to connect to Supabase: {e}")

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Public Transport Delay Analytics",
    page_icon="🚍",
    layout="wide"
)

st.write(" ")

# ======================================================
# SUBSCRIPTION PLAN DEFINITIONS
# ======================================================

PLANS = {
    "Free": {
        "price": "₹0/month",
        "monthly_revenue": 0,
        "color": "#4a5568",
        "badge_bg": "#2d3748",
        "badge_text": "#a0aec0",
        "routes": 3,
        "charts": 2,
        "ai_queries": 0,
        "insights": False,
        "route_insights": False,
        "features": [
            "✅ 3 routes",
            "✅ 2 dashboard charts",
            "❌ Route Insights",
            "❌ Insights page",
            "❌ AI Assistant",
        ]
    },
    "Basic": {
        "price": "₹199/month",
        "monthly_revenue": 199,
        "color": "#2b6cb0",
        "badge_bg": "#1a365d",
        "badge_text": "#90cdf4",
        "routes": 10,
        "charts": 5,
        "ai_queries": 5,
        "insights": False,
        "route_insights": True,
        "features": [
            "✅ 10 routes",
            "✅ 5 dashboard charts",
            "✅ Route Insights",
            "❌ Insights page",
            "✅ 5 AI queries/day",
        ]
    },
    "Premium": {
        "price": "₹499/month",
        "monthly_revenue": 499,
        "color": "#6b21a8",
        "badge_bg": "#3b0764",
        "badge_text": "#e9d8fd",
        "routes": 9999,
        "charts": 9999,
        "ai_queries": 9999,
        "insights": True,
        "route_insights": True,
        "features": [
            "✅ All routes",
            "✅ All dashboard charts",
            "✅ Route Insights",
            "✅ Insights page",
            "✅ Unlimited AI queries",
        ]
    }
}

# ======================================================
# GLOBAL CSS
# ======================================================

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #1e1b4b 100%);
    color: #f8fafc;
}
section[data-testid="stSidebar"] {
    background: #0b1120;
    border-right: 1px solid #312e81;
}
section[data-testid="stSidebar"]::before {
    content: "🚍 Public Transport Delay Analytics";
    display: block;
    padding: 22px 20px;
    font-size: 18px;
    font-weight: 700;
    color: white;
    border-bottom: 1px solid #312e81;
}
h1 { color: white !important; font-size: 42px !important; font-weight: 800 !important; }
h2, h3 { color: #c4b5fd !important; }
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(139,92,246,0.35);
    backdrop-filter: blur(12px);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
    transition: all 0.3s ease;
}
[data-testid="stMetric"]:hover { transform: translateY(-4px); border-color: #8b5cf6; }
[data-testid="stMetricLabel"] { color: #d8b4fe !important; font-size: 15px !important; }
[data-testid="stMetricValue"] { color: white !important; font-size: 32px !important; font-weight: 700 !important; }
div[data-testid="stPlotlyChart"] {
    background: rgba(17,24,39,0.75);
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 18px;
    padding: 12px;
}
.insight-box {
    background: rgba(91,33,182,0.15);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 16px;
    padding: 20px;
    margin-top: 10px;
    line-height: 1.8;
}
.chart-summary {
    background: rgba(139,92,246,0.08);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 12px;
    padding: 12px 18px;
    margin-top: 8px;
    margin-bottom: 18px;
    font-size: 13px;
    color: #d8b4fe;
    line-height: 1.75;
}
.chart-summary ul { margin: 0; padding-left: 18px; }
.chart-summary li { margin-bottom: 5px; }
.dyn-box {
    background: rgba(91,33,182,0.12);
    border: 1px solid rgba(139,92,246,0.28);
    border-radius: 14px;
    padding: 16px 20px;
    margin-bottom: 14px;
    line-height: 1.8;
    font-size: 14px;
    color: #e2d9f3;
}
.dyn-box ul { margin: 6px 0 0 0; padding-left: 20px; }
.dyn-box li { margin-bottom: 5px; }
.dyn-box h4 { color: #c4b5fd; margin: 0 0 8px 0; font-size: 15px; }
.hero-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 24px;
    padding: 45px;
    margin-top: 30px;
}
.center-text {
    text-align: center;
    font-size: 18px;
    color: #d1d5db;
    max-width: 950px;
    margin: auto;
    line-height: 1.8;
    padding-top: 20px;
}
.hero-title {
    font-size: 52px !important;
    font-weight: 800 !important;
    color: white !important;
    text-align: center;
}
.plan-card {
    border-radius: 18px;
    padding: 24px 20px;
    margin-bottom: 10px;
    text-align: center;
}
.profile-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 18px;
    padding: 28px;
    margin-bottom: 20px;
}
.lock-banner {
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.3);
    border-radius: 12px;
    padding: 16px 20px;
    color: #fca5a5;
    font-size: 14px;
    margin-bottom: 16px;
}
.payment-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 20px;
    padding: 32px;
    margin-bottom: 20px;
}
.payment-success {
    background: rgba(34,197,94,0.1);
    border: 1px solid rgba(34,197,94,0.4);
    border-radius: 16px;
    padding: 28px;
    text-align: center;
    color: #86efac;
    margin: 20px 0;
}
.txn-row {
    background: rgba(255,255,255,0.03);
    border: 1px solid rgba(139,92,246,0.15);
    border-radius: 10px;
    padding: 12px 18px;
    margin-bottom: 8px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    font-size: 13px;
    color: #d8b4fe;
}
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #8b5cf6);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: 600;
    width: 100%;
}
.stTextInput input {
    background-color: #111827 !important;
    color: white !important;
    border: 1px solid #7c3aed !important;
    border-radius: 10px !important;
}
[data-baseweb="select"] { background-color: #111827 !important; }
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background-color: #7c3aed !important;
    color: white !important;
}
hr { border-color: rgba(255,255,255,0.08); }
div[data-testid="stAlert"] {
    border-radius: 14px;
    border: 1px solid rgba(139,92,246,0.25);
    background: rgba(255,255,255,0.04);
}
</style>
""", unsafe_allow_html=True)

# ======================================================
# USER STORE (LOCAL AUTH LOGIC)
# ======================================================

USERS_FILE = "users_db.json"

def load_users():
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, "r") as f:
            return json.load(f)
    default = {
        "admin": {
            "password": hash_password("admin123"),
            "role": "admin",
            "name": "Admin",
            "created_at": str(datetime.now()),
            "plan": "Premium"
        }
    }
    save_users(default)
    return default

def save_users(users):
    with open(USERS_FILE, "w") as f:
        json.dump(users, f, indent=2)

def hash_password(p):
    return hashlib.sha256(p.encode()).hexdigest()

def authenticate(username, password, users):
    if username in users:
        if users[username]["password"] == hash_password(password):
            return True, users[username]["role"], users[username]["name"], users[username].get("plan", "Free")
    return False, None, None, None

def register_user(username, password, name, users):
    if username in users:
        return False, "Username already exists."
    if len(password) < 6:
        return False, "Password must be at least 6 characters."
    users[username] = {
        "password": hash_password(password),
        "role": "user",
        "name": name,
        "created_at": str(datetime.now()),
        "plan": "Free",
        "transactions": []
    }
    save_users(users)
    return True, "Account created! You are on the Free plan."

# ======================================================
# NEW: SUPABASE LOG IN TRANSACTION
# ======================================================
def save_username_to_supabase(username):
    """Checks if username exists in Supabase. If not, pushes it."""
    try:
        # Check if user already exists in cloud table
        response = supabase.table("users").select("username").eq("username", username).execute()
        
        # If no entries are found, insert just the username
        if len(response.data) == 0:
            supabase.table("users").insert({"username": username}).execute()
    except Exception as e:
        # Keeps local experience intact even if Supabase network drop occurs
        st.sidebar.warning(f"Cloud Sync skipped: {e}")

# ======================================================
# SESSION STATE
# ======================================================

for key, val in [
    ("logged_in", False),
    ("role", None),
    ("username", None),
    ("name", None),
    ("plan", "Free"),
    ("payment_step", "select"),      
    ("payment_target_plan", None),
    ("payment_method", None),
]:
    if key not in st.session_state:
        st.session_state[key] = val

users_db = load_users()

def get_plan():
    return st.session_state.get("plan", "Free")

def plan_limits():
    return PLANS[get_plan()]

# ======================================================
# SUBSCRIPTION REVENUE HELPER
# ======================================================

def get_subscription_revenue_data():
    fresh = load_users()
    rows = []
    for username, data in fresh.items():
        if data["role"] == "user":
            plan = data.get("plan", "Free")
            joined = data.get("created_at", str(datetime.now()))[:10]
            rows.append({
                "username": username,
                "name": data["name"],
                "plan": plan,
                "monthly_revenue": PLANS[plan]["monthly_revenue"],
                "joined": joined
            })
    return pd.DataFrame(rows) if rows else pd.DataFrame(
        columns=["username", "name", "plan", "monthly_revenue", "joined"]
    )

# ======================================================
# COMMON CHART LAYOUT
# ======================================================

COMMON_LAYOUT = dict(
    height=320,
    paper_bgcolor="#1e0f3d",
    plot_bgcolor="#150b2e",
    font=dict(color="#e2d9f3"),
    title_font=dict(color="#c084fc", size=15),
    margin=dict(l=10, r=10, t=50, b=10),
    legend=dict(bgcolor="rgba(30,15,61,0.7)", bordercolor="#4a3470", borderwidth=1)
)

def apply_layout(fig):
    fig.update_layout(**COMMON_LAYOUT)
    fig.update_xaxes(gridcolor="#2d1b5e")
    fig.update_yaxes(gridcolor="#2d1b5e")
    return fig

# ======================================================
# LOGIN PAGE
# ======================================================

def login_page():
    st.markdown('<div style="max-width:420px;margin:3rem auto;">', unsafe_allow_html=True)
    st.markdown("## 🚍 Public Transport Delay Analytics")
    st.markdown("##### Sign in to continue")

    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    with tab_login:
        with st.form("login_form"):
            username    = st.text_input("Username", placeholder="Enter username")
            password    = st.text_input("Password", type="password", placeholder="Enter password")
            role_choice = st.selectbox("Login as", ["User", "Admin"])
            submitted   = st.form_submit_button("Login")
            if submitted:
                ok, role, name, plan = authenticate(username, password, users_db)
                if ok:
                    if role_choice.lower() != role:
                        st.error(f"This account does not have {role_choice} access.")
                    else:
                        st.session_state.logged_in = True
                        st.session_state.role      = role
                        st.session_state.username  = username
                        st.session_state.name      = name
                        st.session_state.plan      = plan
                        
                        # TRIGGER SUPABASE ACTION ON SUCCESSFUL SIGN IN
                        if role == "user":
                            save_username_to_supabase(username)
                            
                        st.rerun()
                else:
                    st.error("Invalid username or password.")

    with tab_signup:
        with st.form("signup_form"):
            new_name = st.text_input("Full Name",        placeholder="Your name")
            new_user = st.text_input("Username",         placeholder="Choose a username")
            new_pw   = st.text_input("Password",         type="password", placeholder="Min 6 characters")
            confirm  = st.text_input("Confirm Password", type="password")
            if st.form_submit_button("Create Account"):
                if new_pw != confirm:
                    st.error("Passwords do not match.")
                elif not new_name or not new_user:
                    st.error("Please fill in all fields.")
                else:
                    ok, msg = register_user(new_user, new_pw, new_name, users_db)
                    st.success(msg) if ok else st.error(msg)

    st.markdown('</div>', unsafe_allow_html=True)

# ======================================================
# SIDEBAR
# ======================================================

def render_sidebar():
    with st.sidebar:
        plan    = get_plan()
        p       = PLANS[plan]
        role_bg = "#553c9a" if st.session_state.role == "admin" else "#1a365d"
        role_fg = "#e9d8fd" if st.session_state.role == "admin" else "#90cdf4"

        st.markdown(
            f"### 👋 {st.session_state.name} "
            f"<span style='background:{role_bg};color:{role_fg};"
            f"padding:2px 10px;border-radius:20px;font-size:12px;font-weight:600;'>"
            f"{st.session_state.role.upper()}</span>",
            unsafe_allow_html=True
        )

        if st.session_state.role == "user":
            st.markdown(
                f"<div style='background:{p['badge_bg']};color:{p['badge_text']};"
                f"padding:6px 12px;border-radius:10px;font-size:13px;"
                f"font-weight:600;margin:6px 0;text-align:center;'>"
                f"📦 {plan} Plan</div>",
                unsafe_allow_html=True
            )

        st.divider()

        if st.session_state.role == "admin":
            pages = ["Revenue Dashboard", "User Management"]
        else:
            pages = ["My Profile", "Home", "Operational Dashboard", "Route Insights", "Insights", "Payments", "About Us"]

        page = st.radio("Navigation", pages, label_visibility="collapsed")
        st.divider()

        if st.button("🚪 Logout"):
            for k in ["logged_in", "role", "username", "name", "plan",
                      "payment_step", "payment_target_plan", "payment_method"]:
                st.session_state[k] = None
            st.session_state.logged_in = False
            st.rerun()

    return page

# ======================================================
# LOCK BANNER
# ======================================================

def lock_banner(feature, upgrade_to="Basic"):
    st.markdown(f"""
    <div class="lock-banner">
    🔒 <b>{feature}</b> is not available on your current plan.<br>
    Upgrade to <b>{upgrade_to}</b> or higher from <b>Payments</b> page.
    </div>
    """, unsafe_allow_html=True)

# ======================================================
# PAGE: MY PROFILE
# ======================================================

def page_profile():
    st.title("👤 My Profile")
    st.divider()

    current_plan = get_plan()
    fresh_users  = load_users()
    user_data    = fresh_users.get(st.session_state.username, {})

    st.markdown(f"""
    <div class="profile-card">
        <h3 style="margin:0 0 8px 0;">👋 {st.session_state.name}</h3>
        <p style="color:#a0aec0;margin:0;">@{st.session_state.username}</p>
        <p style="color:#a0aec0;margin:4px 0;">Member since: {user_data.get('created_at', 'N/A')[:10]}</p>
        <p style="color:#a0aec0;margin:4px 0;">Current Plan:
            <b style="color:#c4b5fd;">{current_plan}</b> — {PLANS[current_plan]['price']}
        </p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("To upgrade or change your plan, visit the **Payments** page from the sidebar.")

# ======================================================
# PAGE: HOME
# ======================================================

def page_home():
    st.markdown("""
    <div class="hero-box">
    <p class="hero-title">Public Transport Delay Analysis</p>
    <p class="center-text">
    Explore how traffic conditions, congestion levels, weather patterns,
    and peak-hour operations affect public transport delays across routes and time periods.
    </p>
    </div>
    """, unsafe_allow_html=True)

    st.divider()
    st.header("What You Can Discover")
    col1, col2 = st.columns(2)
    with col1:
        st.info("📍 Identify routes with frequent delays")
        st.info("🚦 Understand how congestion impacts travel time")
        st.info("⏱ Discover peak-hour delay patterns")
    with col2:
        st.info("🌦 Analyze weather-related transport disruptions")
        st.info("📈 Compare delay behavior across different time periods")
        st.info("🚌 Explore operational performance trends across routes")

    st.divider()
    st.header("Operational Metrics")
    m1, m2, m3, m4 = st.columns(4, gap="large")
    m1.metric("Total Records",       "20K+")
    m2.metric("Analyzed Trips",      "15K+")
    m3.metric("Average Delay",       "7 mins")
    m4.metric("On-Time Performance", "89%")
    st.write("")
    st.caption("Public Transport Analytics Dashboard")

# ======================================================
# PAGE: OPERATIONAL DASHBOARD
# ======================================================

def page_operational_dashboard():
    try:
        trips  = pd.read_excel("data/Fact_Trips_Cleaned.xlsx")
        routes = pd.read_excel("data/Dim_Routes_Cleaned.xlsx")
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}.")
        return

    trips["Delay_Minutes"]    = pd.to_numeric(trips["Delay_Minutes"], errors="coerce")
    trips["Hour"]             = pd.to_datetime(trips["Time"], errors="coerce").dt.hour
    trips["VehicleType"]      = trips["VehicleType"].astype(str).str.strip()
    trips["WeatherCondition"] = trips["WeatherCondition"].astype(str).str.strip()
    trips["Status"]           = trips["Status"].astype(str).str.strip()
    trips["CongestionLevel"]  = trips["CongestionLevel"].astype(str).str.strip()

    df = trips.merge(routes, on="RouteID", how="left") if "RouteID" in routes.columns else trips.copy()

    limits     = plan_limits()
    max_routes = limits["routes"]
    max_charts = limits["charts"]
    plan       = get_plan()

    all_routes     = sorted(df["RouteID"].dropna().unique())
    allowed_routes = all_routes[:max_routes]
    df             = df[df["RouteID"].isin(allowed_routes)]

    st.title("📊 Operational Transport Dashboard")
    st.markdown("Monitor public transport performance, delay patterns, congestion levels, weather impact, and district-wise operations.")

    if plan != "Premium":
        st.info(f"📦 **{plan} Plan** — Showing **{len(allowed_routes)} of {len(all_routes)} routes** and **{max_charts} charts**. Upgrade for full access.")

    with st.sidebar:
        st.subheader("🎛️ Filters")
        vehicle_filter = st.multiselect(
            "Vehicle Type",
            sorted(df["VehicleType"].dropna().unique()),
            default=sorted(df["VehicleType"].dropna().unique()),
            key="od_vehicle"
        )
        weather_filter = st.multiselect(
            "Weather Condition",
            sorted(df["WeatherCondition"].dropna().unique()),
            default=sorted(df["WeatherCondition"].dropna().unique()),
            key="od_weather"
        )
        status_filter = st.multiselect(
            "Trip Status",
            sorted(df["Status"].dropna().unique()),
            default=sorted(df["Status"].dropna().unique()),
            key="od_status"
        )

    filtered_df = df[
        df["VehicleType"].isin(vehicle_filter) &
        df["WeatherCondition"].isin(weather_filter) &
        df["Status"].isin(status_filter)
    ].copy()

    if filtered_df.empty:
        st.warning("No data available for the selected filters.")
        return

    st.divider()

    avg_delay      = filtered_df["Delay_Minutes"].mean()
    network_health = max(0, 100 - avg_delay)

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Trips",               len(filtered_df))
    k2.metric("OTP %",               "89%")
    k3.metric("Avg Delay",           "7 mins")
    k4.metric("Overall Performance", f"{network_health:.1f}%")
    st.divider()

    hourly_delay     = filtered_df.groupby("Hour")["Delay_Minutes"].mean().reset_index()
    route_delay      = filtered_df.groupby("RouteID")["Delay_Minutes"].mean().reset_index().sort_values("Delay_Minutes", ascending=False)
    weather_delay    = filtered_df.groupby("WeatherCondition")["Delay_Minutes"].mean().reset_index()
    vehicle_data     = filtered_df.groupby("VehicleType").size().reset_index(name="Trips")
    congestion_delay = filtered_df.groupby("CongestionLevel")["Delay_Minutes"].mean().reset_index()
    filtered_df["Day"] = pd.to_datetime(filtered_df["Date"], errors="coerce").dt.day_name()
    heatmap_data     = filtered_df.pivot_table(values="Delay_Minutes", index="Day", columns="Hour", aggfunc="mean")
    district_data    = filtered_df.groupby(["Origin", "Destination", "Status", "VehicleType"]).size().reset_index(name="Trips")

    fig_line = px.line(hourly_delay, x="Hour", y="Delay_Minutes", markers=True, title="⏰ Hourly Delay Trend")
    fig_line.update_traces(line=dict(color="#06b6d4", width=3), marker=dict(color="#67e8f9", size=8))

    fig_weather = px.bar(weather_delay, x="WeatherCondition", y="Delay_Minutes", title="🌦️ Weather Impact")
    fig_weather.update_traces(marker_color=["#2563eb", "#3b82f6", "#60a5fa", "#93c5fd", "#2563eb"][:len(weather_delay)])

    fig_vehicle = px.bar(vehicle_data, x="VehicleType", y="Trips", title="🚍 Vehicle Distribution")
    fig_vehicle.update_traces(marker_color=["#059669", "#10b981"][:len(vehicle_data)])

    fig_bar = px.bar(route_delay.head(10), x="RouteID", y="Delay_Minutes", title="🚦 Top Delayed Routes")
    colors_bar = ["#dc2626", "#ef4444", "#f87171", "#fca5a5"] * 3
    fig_bar.update_traces(marker_color=colors_bar[:len(route_delay.head(10))])

    fig_congestion = px.bar(congestion_delay, x="CongestionLevel", y="Delay_Minutes",
                             title="🚗 Avg Delay by Congestion Level", text_auto=".1f")
    congestion_colors = ["#22c55e", "#facc15", "#ef4444"]
    fig_congestion.update_traces(
        marker_color=congestion_colors[:len(congestion_delay)],
        textposition="outside"
    )

    fig_heatmap = px.imshow(
        heatmap_data, text_auto=True, aspect="auto",
        title="🔥 Delay Heatmap", color_continuous_scale="Turbo"
    )

    fig_map = px.scatter(
        district_data, x="Origin", y="Destination", size="Trips",
        color="Status", symbol="VehicleType",
        title="🗺️ District-wise Delay & Vehicle Analysis",
        color_discrete_map={"On-Time": "#38bdf8", "Delayed": "#818cf8", "Cancelled": "#c084fc"}
    )

    all_figs = [fig_line, fig_weather, fig_vehicle, fig_bar, fig_congestion, fig_heatmap, fig_map]
    for fig in all_figs:
        apply_layout(fig)

    chart_defs = [
        ("⏰ Hourly Delay Trend",   fig_line),
        ("🌦️ Weather Impact",      fig_weather),
        ("🚍 Vehicle Distribution", fig_vehicle),
        ("🚦 Top Delayed Routes",   fig_bar),
        ("🚗 Congestion Delay",     fig_congestion),
        ("🔥 Delay Heatmap",        fig_heatmap),
    ]

    r1c1, r1c2, r1c3 = st.columns(3)
    r2c1, r2c2, r2c3 = st.columns(3)
    cols = [r1c1, r1c2, r1c3, r2c1, r2c2, r2c3]

    shown = 0
    for i, (title, fig) in enumerate(chart_defs):
        if i >= len(cols):
            break
        if shown < max_charts:
            cols[i].plotly_chart(fig, use_container_width=True)
            shown += 1
        else:
            with cols[i]:
                st.markdown(f"""
                <div style='background:rgba(239,68,68,0.08);border:1px dashed rgba(239,68,68,0.4);
                border-radius:18px;padding:50px 20px;text-align:center;color:#fca5a5;'>
                🔒 <b>{title}</b><br><small>Upgrade to unlock</small></div>
                """, unsafe_allow_html=True)

    if max_charts >= 7:
        st.plotly_chart(fig_map, use_container_width=True)
    else:
        st.markdown("""
        <div style='background:rgba(239,68,68,0.08);border:1px dashed rgba(239,68,68,0.4);
        border-radius:18px;padding:30px;text-align:center;color:#fca5a5;margin-top:12px;'>
        🔒 <b>🗺️ District Analysis</b> — Upgrade to Premium to unlock</div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.caption("🚍 Operational Analytics Dashboard • Public Transport Delay Analysis")

# ======================================================
# PAGE: ROUTE INSIGHTS
# ======================================================

def page_route_insights():
    limits = plan_limits()
    if not limits["route_insights"]:
        st.title("🛣️ Route Insights Dashboard")
        lock_banner("Route Insights Dashboard", "Basic")
        return

    @st.cache_data
    def load_data():
        trips  = pd.read_excel("data/Fact_Trips_Cleaned.xlsx")
        routes = pd.read_excel("data/Dim_Routes_Cleaned.xlsx")
        return trips, routes

    try:
        trips, routes = load_data()
    except FileNotFoundError as e:
        st.error(f"Data file not found: {e}")
        return

    df = trips.merge(routes, on="RouteID", how="left") if "RouteID" in routes.columns else trips.copy()

    df["Delay_Minutes"] = pd.to_numeric(df["Delay_Minutes"], errors="coerce")
    df["Date"]          = pd.to_datetime(df["Date"], errors="coerce")
    df["Hour"]          = pd.to_datetime(df["Time"], errors="coerce").dt.hour
    df["Month"]         = df["Date"].dt.month

    def get_season(m):
        if m in [3, 4, 5]:      return "Summer"
        elif m in [6, 7, 8, 9]: return "Monsoon"
        elif m in [10, 11]:     return "Post-Monsoon"
        else:                   return "Winter"

    def get_tp(h):
        if pd.isna(h):      return "Unknown"
        elif 6  <= h < 10:  return "Morning Rush"
        elif 10 <= h < 16:  return "Afternoon"
        elif 16 <= h < 21:  return "Evening Rush"
        else:               return "Night"

    df["Season"]     = df["Month"].apply(get_season)
    df["TimePeriod"] = df["Hour"].apply(get_tp)

    for col in ["VehicleType", "Status", "WeatherCondition", "CongestionLevel"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    max_routes = limits["routes"]
    all_routes = sorted(df["RouteID"].dropna().unique())
    allowed    = all_routes[:max_routes]

    with st.sidebar:
        st.subheader("🎛️ Filters")
        route_filter   = st.selectbox("Select Route", ["All"] + list(allowed), key="ri_route")
        vehicle_filter = st.multiselect("Vehicle Type",      sorted(df["VehicleType"].dropna().unique()), default=sorted(df["VehicleType"].dropna().unique()), key="ri_vehicle")
        status_filter  = st.multiselect("Trip Status",       sorted(df["Status"].dropna().unique()),      default=sorted(df["Status"].dropna().unique()), key="ri_status")
        weather_filter = st.multiselect("Weather Condition", sorted(df["WeatherCondition"].dropna().unique()), default=sorted(df["WeatherCondition"].dropna().unique()), key="ri_weather")

    filt = df[df["RouteID"].isin(allowed)]
    if route_filter != "All":
        filt = filt[filt["RouteID"] == route_filter]
    filt = filt[
        filt["VehicleType"].isin(vehicle_filter) &
        filt["Status"].isin(status_filter) &
        filt["WeatherCondition"].isin(weather_filter)
    ]

    if filt.empty:
        st.warning("No data available for the selected filters.")
        return

    st.title("🛣️ Route Insights Dashboard")
    st.markdown("Understand WHY delays happen, WHEN operational instability occurs, and WHICH conditions create disruption.")
    st.divider()

    st.subheader("📍 Route Information")
    if route_filter == "All":
        i1, i2, i3, i4 = st.columns(4)
        i1.info(f"**Routes**\n\n{len(allowed)} Routes")
        i2.info(f"**Total Trips**\n\n{len(filt)}")
        i3.info("**Avg Distance**\n\nAll Routes")
        i4.info(f"**Vehicle Types**\n\n{', '.join(vehicle_filter)}")
    else:
        ri = filt.iloc[0]
        i1, i2, i3, i4 = st.columns(4)
        i1.info(f"**Origin**\n\n{ri.get('Origin', 'N/A')}")
        i2.info(f"**Destination**\n\n{ri.get('Destination', 'N/A')}")
        i3.info(f"**Distance**\n\n{ri.get('DistanceKM', 'N/A')} KM")
        i4.info(f"**Vehicle Types**\n\n{', '.join(vehicle_filter)}")

    st.divider()
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Average Delay", f"{filt['Delay_Minutes'].mean():.1f} mins")
    k2.metric("Maximum Delay", f"{filt['Delay_Minutes'].max():.1f} mins")
    k3.metric("Trips",           len(filt))
    otp_pct = (filt["Status"] == "On-Time").sum() / len(filt) * 100 if len(filt) > 0 else 0
    k4.metric("On-Time %",     f"{otp_pct:.1f}%")
    st.divider()

    wi = filt.groupby("WeatherCondition").agg(A=("Delay_Minutes","mean"), T=("Delay_Minutes","count"))
    wi["S"] = wi["A"] * wi["T"]
    top_wx = wi["S"].idxmax() if not wi.empty else "N/A"

    ci = filt.groupby("CongestionLevel").agg(A=("Delay_Minutes","mean"), T=("Delay_Minutes","count"))
    ci["S"] = ci["A"] * ci["T"]
    top_cg = ci["S"].idxmax() if not ci.empty else "N/A"

    ti = filt.groupby("TimePeriod").agg(A=("Delay_Minutes","mean"), T=("Delay_Minutes","count"))
    ti["S"] = ti["A"] * ti["T"]
    top_tp = ti["S"].idxmax() if not ti.empty else "N/A"

    st.subheader("🚨 Root Cause Analysis")
    st.markdown(f"""
    <div class="insight-box">
    🌦️ Major delays strongly associated with <b>{top_wx}</b> weather.<br><br>
    🚦 Route instability severe during <b>{str(top_cg).lower()}</b> congestion.<br><br>
    ⏰ Most disruptions occur during <b>{top_tp}</b>.
    </div>""", unsafe_allow_html=True)
    st.divider()

# ======================================================
# DUMMY PLACEHOLDERS FOR EXTRA PAGES
# ======================================================
def page_insights(): st.title("💡 Deep Insights"); lock_banner("Insights Engine", "Premium")
def page_payments(): st.title("💳 Plan & Payments"); st.info("Manage your subscriptions locally.")
def page_about(): st.title("ℹ️ About Us"); st.write("Public Transport Infrastructure Platform")
def page_admin_revenue(): st.title("💰 Revenue Dashboard"); st.write("Admin Overview Metrics")
def page_admin_users(): st.title("👥 User Management"); st.write("System User Profiles")

# ======================================================
# MAIN ROUTING ENGINE
# ======================================================

if not st.session_state.logged_in:
    login_page()
else:
    active_page = render_sidebar()
    
    if st.session_state.role == "admin":
        if active_page == "Revenue Dashboard": page_admin_revenue()
        elif active_page == "User Management": page_admin_users()
    else:
        if active_page == "My Profile": page_profile()
        elif active_page == "Home": page_home()
        elif active_page == "Operational Dashboard": page_operational_dashboard()
        elif active_page == "Route Insights": page_route_insights()
        elif active_page == "Insights": page_insights()
        elif active_page == "Payments": page_payments()
        elif active_page == "About Us": page_about()

