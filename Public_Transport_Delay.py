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
# USER STORE
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

def generate_txn_id():
    return "TXN" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

# ======================================================
# SESSION STATE
# ======================================================

for key, val in [
    ("logged_in", False),
    ("role", None),
    ("username", None),
    ("name", None),
    ("plan", "Free"),
    ("payment_step", "select"),      # select | details | confirm | success
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
            pages = ["Home", "Operational Dashboard", "Route Insights", "Insights", "My Profile", "Payments", "About Us"]

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
    # Load data — wrapped in try/except so missing files don't crash the app
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

    # FIX: Sidebar filters placed BEFORE the main content, not nested inside another with st.sidebar block
    st.title("📊 Operational Transport Dashboard")
    st.markdown("Monitor public transport performance, delay patterns, congestion levels, weather impact, and district-wise operations.")

    if plan != "Premium":
        st.info(f"📦 **{plan} Plan** — Showing **{len(allowed_routes)} of {len(all_routes)} routes** and **{max_charts} charts**. Upgrade for full access.")

    # Sidebar filters
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

    # FIX: Safely check for Groq availability without crashing
    groq_ok = False
    try:
        from groq import Groq
        if "API_KEY" in st.secrets:
            groq_ok = True
    except Exception:
        pass

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

    route_label = "All Routes" if route_filter == "All" else f"Route {route_filter}"

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
    k3.metric("Trips",         len(filt))
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

    def summary_box(pts):
        items = "".join(f"<li>{p}</li>" for p in pts)
        st.markdown(f'<div class="chart-summary"><ul>{items}</ul></div>', unsafe_allow_html=True)

    time_order = ["Morning Rush", "Afternoon", "Evening Rush", "Night"]

    seas_df = filt.groupby(["Season","WeatherCondition"]).agg(
        AvgDelay=("Delay_Minutes","mean"), Trips=("Delay_Minutes","count")
    ).reset_index()
    seas_df = seas_df[seas_df["Trips"] >= 15]
    seas_df["ImpactScore"] = seas_df["AvgDelay"] * seas_df["Trips"]

    cong_df = filt.groupby(["TimePeriod","CongestionLevel"]).agg(
        AvgDelay=("Delay_Minutes","mean"), Trips=("Delay_Minutes","count")
    ).reset_index()
    cong_df["ImpactScore"] = cong_df["AvgDelay"] * cong_df["Trips"]

    top_cong_df = pd.DataFrame()
    if not cong_df.empty:
        top_cong_df = cong_df.loc[cong_df.groupby("TimePeriod")["ImpactScore"].idxmax()].copy()
        top_cong_df["TimePeriod"] = pd.Categorical(top_cong_df["TimePeriod"], categories=time_order, ordered=True)
        top_cong_df = top_cong_df.sort_values("TimePeriod")
        top_cong_df["Reason"] = (
            top_cong_df["CongestionLevel"] + " congestion caused " +
            top_cong_df["AvgDelay"].round(1).astype(str) + " mins"
        )

    sc_df = filt.groupby(["WeatherCondition","TimePeriod"])["Delay_Minutes"].mean().reset_index()
    sc_df.columns = ["WeatherCondition","TimePeriod","AvgDelay"]
    if not sc_df.empty:
        sc_df["TimePeriod"] = pd.Categorical(sc_df["TimePeriod"], categories=time_order, ordered=True)
        sc_df = sc_df.sort_values("TimePeriod")

    hour_df = filt.groupby(["Hour","CongestionLevel"])["Delay_Minutes"].mean().reset_index()

    fig_s = px.bar(seas_df, x="Season", y="ImpactScore", color="WeatherCondition", barmode="group",
                   title=f"🌦️ Seasonal Delay Causes — {route_label}")
    fig_c = px.bar(top_cong_df, x="TimePeriod", y="ImpactScore", color="CongestionLevel",
                   text="Reason", title=f"🚦 Congestion Cause Across Day — {route_label}")
    if not top_cong_df.empty:
        fig_c.update_traces(textposition="outside")
    fig_sc = px.bar(sc_df, x="TimePeriod", y="AvgDelay", color="WeatherCondition", barmode="group",
                    text=sc_df["AvgDelay"].round(1).astype(str) + " m",
                    title=f"🔥 Weather vs Time Period — {route_label}")
    if not sc_df.empty:
        fig_sc.update_traces(textposition="outside", opacity=0.85)
    fig_h = px.line(hour_df, x="Hour", y="Delay_Minutes", color="CongestionLevel", markers=True,
                    title=f"⏰ Hour-wise Instability — {route_label}")

    chart_bg = dict(height=360, paper_bgcolor="#111827", plot_bgcolor="#111827",
                    font_color="white", margin=dict(l=10, r=10, t=50, b=10))
    for fig in [fig_s, fig_c, fig_sc, fig_h]:
        fig.update_layout(**chart_bg)

    # Summary bullets — guard against empty data
    if not seas_df.empty:
        ss = [
            f"<b>{seas_df.loc[seas_df['ImpactScore'].idxmax(), 'Season']}</b> most delay-prone.",
            f"<b>{seas_df.loc[seas_df['ImpactScore'].idxmin(), 'Season']}</b> lowest delay."
        ]
    else:
        ss = ["Insufficient seasonal data.", "Adjust filters."]

    if not top_cong_df.empty:
        hi = top_cong_df.loc[top_cong_df["ImpactScore"].idxmax()]
        lo = top_cong_df.loc[top_cong_df["ImpactScore"].idxmin()]
        cg = [
            f"<b>{hi['TimePeriod']}</b> highest — {str(hi['CongestionLevel']).lower()} congestion ({hi['AvgDelay']:.1f} mins).",
            f"<b>{lo['TimePeriod']}</b> least affected — {str(lo['CongestionLevel']).lower()} congestion ({lo['AvgDelay']:.1f} mins)."
        ]
    else:
        cg = ["Insufficient congestion data.", "Adjust filters."]

    if not sc_df.empty:
        sc = [
            f"Worst: <b>{sc_df.loc[sc_df['AvgDelay'].idxmax(), 'WeatherCondition']}</b> at <b>{sc_df.loc[sc_df['AvgDelay'].idxmax(), 'TimePeriod']}</b>.",
            f"Best: <b>{sc_df.loc[sc_df['AvgDelay'].idxmin(), 'WeatherCondition']}</b> at <b>{sc_df.loc[sc_df['AvgDelay'].idxmin(), 'TimePeriod']}</b>."
        ]
    else:
        sc = ["Insufficient data.", "Adjust filters."]

    if not hour_df.empty:
        pk = hour_df.loc[hour_df["Delay_Minutes"].idxmax()]
        lw = hour_df.loc[hour_df["Delay_Minutes"].idxmin()]
        hr = [
            f"Peak at <b>{int(pk['Hour'])}:00</b> — {str(pk['CongestionLevel']).lower()} congestion ({pk['Delay_Minutes']:.1f} mins).",
            f"Stable at <b>{int(lw['Hour'])}:00</b> — {str(lw['CongestionLevel']).lower()} congestion ({lw['Delay_Minutes']:.1f} mins)."
        ]
    else:
        hr = ["Insufficient hourly data.", "Adjust filters."]

    r1c1, r1c2 = st.columns(2)
    with r1c1:
        st.plotly_chart(fig_s,  use_container_width=True)
        summary_box(ss)
    with r1c2:
        st.plotly_chart(fig_c,  use_container_width=True)
        summary_box(cg)
    r2c1, r2c2 = st.columns(2)
    with r2c1:
        st.plotly_chart(fig_sc, use_container_width=True)
        summary_box(sc)
    with r2c2:
        st.plotly_chart(fig_h,  use_container_width=True)
        summary_box(hr)

    st.divider()
    st.header("🤖 AI Operational Assistant")

    ai_limit = limits["ai_queries"]
    if ai_limit == 0:
        lock_banner("AI Operational Assistant", "Basic")
    else:
        if ai_limit < 9999:
            st.caption(f"📦 Your plan allows **{ai_limit} AI queries/day**.")
        user_q = st.text_area(
            "Ask anything about delays, congestion, timings, or route performance",
            placeholder="e.g. When is congestion highest? How can delays be reduced?",
            height=150
        )
        if st.button("Ask AI"):
            if not user_q.strip():
                st.warning("Please enter a question.")
            elif not groq_ok:
                st.info("💡 Add your Groq API key in `.streamlit/secrets.toml` as `API_KEY` to enable AI.")
            else:
                with st.spinner("Analyzing..."):
                    from groq import Groq
                    gc = Groq(api_key=st.secrets["API_KEY"])
                    ctx = (
                        f"Route: {route_label} | Avg: {filt['Delay_Minutes'].mean():.2f} | "
                        f"Max: {filt['Delay_Minutes'].max():.2f} | Trips: {len(filt)} | "
                        f"Worst weather: {top_wx} | Peak: {top_tp}\nQ: {user_q}\nAnswer concisely."
                    )
                    res = gc.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": "You are an AI transport operations analyst."},
                            {"role": "user",   "content": ctx}
                        ],
                        temperature=0.3,
                        max_tokens=400
                    )
                    st.markdown(f'<div class="insight-box">{res.choices[0].message.content}</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.caption("🛣️ Route Insights Dashboard • AI-Powered Operational Analytics")

# ======================================================
# PAGE: INSIGHTS
# ======================================================

def page_insights():
    limits = plan_limits()
    if not limits["insights"]:
        st.title("📌 Insights")
        lock_banner("Insights Page", "Premium")
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

    for col in ["VehicleType", "Status", "WeatherCondition", "CongestionLevel"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()

    df["Delay_Minutes"] = pd.to_numeric(df["Delay_Minutes"], errors="coerce")
    df["Hour"]          = pd.to_datetime(df["Time"], errors="coerce").dt.hour

    with st.sidebar:
        st.subheader("🎛️ Filters")
        route_options  = ["ALL"] + sorted(df["RouteID"].dropna().unique().tolist())
        route_filter   = st.selectbox("Select Route",     route_options, key="ins_route")
        vehicle_filter = st.multiselect("Vehicle Type",   sorted(df["VehicleType"].dropna().unique()), default=sorted(df["VehicleType"].dropna().unique()), key="ins_vehicle")
        status_filter  = st.multiselect("Trip Status",    sorted(df["Status"].dropna().unique()),      default=sorted(df["Status"].dropna().unique()), key="ins_status")
        weather_filter = st.multiselect("Weather Condition", sorted(df["WeatherCondition"].dropna().unique()), default=sorted(df["WeatherCondition"].dropna().unique()), key="ins_weather")

    rm  = df["RouteID"].isin(df["RouteID"].unique()) if route_filter == "ALL" else (df["RouteID"] == route_filter)
    fdf = df[
        rm &
        df["VehicleType"].isin(vehicle_filter) &
        df["Status"].isin(status_filter) &
        df["WeatherCondition"].isin(weather_filter)
    ].copy()

    if fdf.empty:
        st.warning("No data available for the selected filters.")
        return

    st.title("📌 Insights")
    st.write("Overall analytical observations and operational findings from public transport datasets.")
    st.divider()

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Trips",         len(fdf))
    m2.metric("Total Routes",        fdf["RouteID"].nunique())
    m3.metric("Average Delay",       f"{fdf['Delay_Minutes'].mean():.2f} mins")
    m4.metric("On-Time Performance", f"{(fdf['Status']=='On-Time').sum() / len(fdf) * 100:.1f}%")
    st.divider()

    rl  = "All Routes" if route_filter == "ALL" else f"Route {route_filter}"
    ad  = fdf["Delay_Minutes"].mean()
    mx  = fdf["Delay_Minutes"].max()
    tc  = len(fdf)
    otp = (fdf["Status"] == "On-Time").sum() / tc * 100

    tc_ = fdf.groupby("CongestionLevel")["Delay_Minutes"].mean().idxmax() if "CongestionLevel" in fdf.columns and not fdf["CongestionLevel"].dropna().empty else "N/A"
    tcd = fdf.groupby("CongestionLevel")["Delay_Minutes"].mean().max()    if "CongestionLevel" in fdf.columns and not fdf["CongestionLevel"].dropna().empty else 0

    ops = [
        f"<b>{rl}</b> — <b>{tc}</b> trips, avg delay <b>{ad:.1f} mins</b>, OTP <b>{otp:.1f}%</b>.",
        f"Highest single-trip delay: <b>{mx:.1f} mins</b>.",
        f"<b>{str(tc_).lower()} congestion</b> is the leading pressure — <b>{tcd:.1f} mins</b> avg."
    ]

    bins = [0, 5, 10, 20, 30, 50, float("inf")]
    lbls = ["<5", "5–10", "10–20", "20–30", "30–50", "50+"]
    fdf["DB"] = pd.cut(fdf["Delay_Minutes"], bins=bins, labels=lbls)
    bc = fdf["DB"].value_counts().sort_index()
    sev = [
        f"Most frequent range: <b>{bc.idxmax()} mins</b> — <b>{bc.max()}</b> trips.",
        f"Only <b>{bc.get('50+', 0)}</b> trips >50 mins.",
        "Medium-range delays (10–30 mins) dominate — consistent moderate congestion."
    ]

    hourly = fdf.groupby("Hour")["Delay_Minutes"].mean() if "Hour" in fdf.columns else pd.Series([ad])
    ph = int(hourly.idxmax())
    sh = int(hourly.idxmin())
    tim = [
        f"Peak at <b>{ph}:00</b> — <b>{hourly.max():.1f} mins</b> avg.",
        f"Most stable at <b>{sh}:00</b> — <b>{hourly.min():.1f} mins</b> avg.",
        f"Extra vehicles at <b>{ph-1}:00–{ph+1}:00</b> would improve punctuality most."
    ]

    vd = fdf.groupby("VehicleType")["Delay_Minutes"].mean()
    vc = fdf["VehicleType"].value_counts()
    veh = [
        f"<b>{vc.idxmax()}</b> handles most trips (<b>{vc.max()}</b>).",
        f"<b>{vd.idxmax()}</b> highest avg delay <b>{vd.max():.1f} mins</b>; <b>{vd.idxmin()}</b> best at <b>{vd.min():.1f} mins</b>.",
        f"Prioritise <b>{vd.idxmin()}</b> during peak congestion."
    ]

    wd = fdf.groupby("WeatherCondition")["Delay_Minutes"].mean()
    wth = [
        f"<b>{wd.idxmax()}</b> weather — highest delays at <b>{wd.max():.1f} mins</b>.",
        f"<b>{wd.idxmin()}</b> — smoothest at <b>{wd.min():.1f} mins</b>.",
        f"<b>{wd.max() - wd.min():.1f} min gap</b> confirms weather as major risk factor."
    ]

    ara  = df.groupby("RouteID")["Delay_Minutes"].mean()
    na   = ara.mean()
    ra   = fdf["Delay_Minutes"].mean()
    diff = ra - na
    cr   = (fdf["Status"] == "Cancelled").sum() / tc * 100
    rte  = [
        f"Avg delay <b>{ra:.1f} mins</b> vs network avg <b>{na:.1f} mins</b>.",
        f"Delay is <b>{abs(diff):.1f} mins {'above' if diff > 0 else 'below'}</b> network avg.",
        f"Cancellation rate: <b>{cr:.1f}%</b> — {'significant concern.' if cr > 5 else 'within acceptable limits.'}"
    ]

    def dyn_box(title, pts):
        items = "".join(f"<li>{p}</li>" for p in pts)
        st.markdown(f'<div class="dyn-box"><h4>{title}</h4><ul>{items}</ul></div>', unsafe_allow_html=True)

    st.header(f"📊 Key Insights — {'All Routes' if route_filter == 'ALL' else f'Route {route_filter}'}")
    lc, rc = st.columns(2)
    with lc:
        with st.container(border=True):
            dyn_box("🚍 Transport Operations",    ops)
            dyn_box("🚦 Delay Severity",          sev)
            dyn_box("⏰ Time-Based Observations", tim)
    with rc:
        with st.container(border=True):
            dyn_box("🚆 Vehicle Performance",         veh)
            dyn_box("🌦️ Weather and Traffic Impact",  wth)
            dyn_box("🛣️ Route Performance",           rte)

    st.divider()
    st.caption("Public Transport Delay Analytics Dashboard • Operational Insights Module")

# ======================================================
# PAGE: PAYMENTS  (NEW)
# ======================================================

def page_payments():
    st.title("💳 Payments & Subscription")
    st.markdown("Manage your subscription plan and view payment history.")
    st.divider()

    current_plan = get_plan()
    fresh_users  = load_users()
    user_data    = fresh_users.get(st.session_state.username, {})
    transactions = user_data.get("transactions", [])

    # ── Step router ──────────────────────────────────────
    step = st.session_state.get("payment_step", "select")

    # ─────────────────────────────────────────────────────
    # STEP 1: Plan selection
    # ─────────────────────────────────────────────────────
    if step == "select":
        st.subheader("📦 Choose Your Plan")
        c1, c2, c3 = st.columns(3)
        for col, plan_name in zip([c1, c2, c3], ["Free", "Basic", "Premium"]):
            p          = PLANS[plan_name]
            is_current = (plan_name == current_plan)
            border     = f"border: 2px solid {p['color']};" if is_current else f"border: 1px solid {p['color']}40;"
            feats      = "".join(f"<li style='padding:4px 0;font-size:13px;'>{f}</li>" for f in p["features"])
            badge      = ("<br><span style='background:#22c55e;color:white;padding:2px 10px;"
                          "border-radius:20px;font-size:12px;'>✓ Current Plan</span>") if is_current else ""

            col.markdown(f"""
            <div class="plan-card" style="background:{p['badge_bg']};{border}">
                <h3 style="color:{p['badge_text']};">{plan_name}{badge}</h3>
                <div style="color:{p['color']};font-size:20px;font-weight:700;margin-bottom:14px;">{p['price']}</div>
                <ul style="list-style:none;padding:0;text-align:left;">{feats}</ul>
            </div>
            """, unsafe_allow_html=True)

            if not is_current:
                label = "Downgrade" if PLANS[plan_name]["monthly_revenue"] < PLANS[current_plan]["monthly_revenue"] else "Upgrade"
                if col.button(f"{label} to {plan_name}", key=f"pay_select_{plan_name}"):
                    st.session_state.payment_step        = "details" if plan_name != "Free" else "confirm"
                    st.session_state.payment_target_plan = plan_name
                    st.rerun()
            else:
                col.markdown(
                    "<div style='text-align:center;color:#22c55e;font-weight:600;padding:8px;'>✓ Active</div>",
                    unsafe_allow_html=True
                )

        st.divider()

        # Transaction history
        st.subheader("🧾 Transaction History")
        if not transactions:
            st.info("No transactions yet. Upgrade to a paid plan to see payment history here.")
        else:
            txn_df = pd.DataFrame(transactions)
            txn_df = txn_df.sort_values("date", ascending=False).reset_index(drop=True)
            for _, row in txn_df.iterrows():
                status_color = "#22c55e" if row.get("status") == "Success" else "#ef4444"
                st.markdown(f"""
                <div style="background:rgba(255,255,255,0.03);border:1px solid rgba(139,92,246,0.15);
                border-radius:10px;padding:14px 20px;margin-bottom:8px;display:flex;
                justify-content:space-between;align-items:center;">
                <div>
                  <span style="color:#c4b5fd;font-weight:600;">#{row.get('txn_id','N/A')}</span>
                  &nbsp;&nbsp;
                  <span style="color:#a0aec0;font-size:13px;">{row.get('date','N/A')}</span>
                </div>
                <div>
                  <span style="color:#e2d9f3;font-weight:600;margin-right:20px;">
                    {row.get('plan','N/A')} Plan — ₹{row.get('amount',0):,}
                  </span>
                  <span style="color:{status_color};font-weight:600;">{row.get('status','N/A')}</span>
                </div>
                </div>
                """, unsafe_allow_html=True)

    # ─────────────────────────────────────────────────────
    # STEP 2: Payment details (paid plans only)
    # ─────────────────────────────────────────────────────
    elif step == "details":
        target  = st.session_state.payment_target_plan
        p       = PLANS[target]
        amount  = p["monthly_revenue"]

        st.subheader(f"💳 Payment Details — {target} Plan")
        st.markdown(f"""
        <div class="payment-card">
        <div style="display:flex;justify-content:space-between;margin-bottom:20px;">
          <div>
            <div style="color:#a0aec0;font-size:13px;">Upgrading to</div>
            <div style="color:{p['color']};font-size:22px;font-weight:700;">{target} Plan</div>
          </div>
          <div style="text-align:right;">
            <div style="color:#a0aec0;font-size:13px;">Amount</div>
            <div style="color:#22c55e;font-size:26px;font-weight:800;">₹{amount:,}/month</div>
          </div>
        </div>
        </div>
        """, unsafe_allow_html=True)

        method = st.radio(
            "Select Payment Method",
            ["💳 Credit / Debit Card", "🏦 UPI / Net Banking", "📱 Wallets (Paytm, PhonePe, GPay)"],
            key="pay_method_radio"
        )
        st.session_state.payment_method = method

        if method == "💳 Credit / Debit Card":
            st.markdown("#### Card Details")
            col1, col2 = st.columns([2, 1])
            with col1:
                card_num = st.text_input("Card Number", placeholder="1234  5678  9012  3456", max_chars=19)
            with col2:
                card_name = st.text_input("Cardholder Name", placeholder="Full Name")
            col3, col4, col5 = st.columns(3)
            with col3:
                expiry = st.text_input("Expiry (MM/YY)", placeholder="MM/YY", max_chars=5)
            with col4:
                cvv = st.text_input("CVV", placeholder="•••", type="password", max_chars=3)
            with col5:
                st.write("")

            ready = all([card_num, card_name, expiry, cvv])

        elif method == "🏦 UPI / Net Banking":
            st.markdown("#### UPI Details")
            upi_id = st.text_input("UPI ID", placeholder="yourname@upi")
            ready  = bool(upi_id and "@" in upi_id)

        else:
            st.markdown("#### Wallet")
            wallet  = st.selectbox("Select Wallet", ["Paytm", "PhonePe", "Google Pay", "Amazon Pay"])
            mobile  = st.text_input("Registered Mobile Number", placeholder="10-digit mobile number", max_chars=10)
            ready   = bool(mobile and len(mobile) == 10 and mobile.isdigit())

        st.markdown("")
        col_back, col_pay = st.columns([1, 2])
        with col_back:
            if st.button("← Back"):
                st.session_state.payment_step = "select"
                st.rerun()
        with col_pay:
            if st.button(f"Pay ₹{amount:,} →", disabled=not ready):
                st.session_state.payment_step = "confirm"
                st.rerun()

        if not ready:
            st.caption("⚠️ Please fill in all payment details to continue.")

    # ─────────────────────────────────────────────────────
    # STEP 3: Confirm
    # ─────────────────────────────────────────────────────
    elif step == "confirm":
        target = st.session_state.payment_target_plan
        p      = PLANS[target]
        amount = p["monthly_revenue"]

        st.subheader("✅ Confirm Your Order")
        st.markdown(f"""
        <div class="payment-card">
        <table style="width:100%;color:#e2d9f3;font-size:15px;line-height:2.2;">
          <tr><td style="color:#a0aec0;">Plan</td><td style="font-weight:700;color:{p['color']}">{target}</td></tr>
          <tr><td style="color:#a0aec0;">Billing</td><td>Monthly</td></tr>
          <tr><td style="color:#a0aec0;">Amount</td><td style="font-weight:700;color:#22c55e;">₹{amount:,}</td></tr>
          <tr><td style="color:#a0aec0;">Payment Method</td>
              <td>{st.session_state.get("payment_method", "—") if amount > 0 else "Free — No payment needed"}</td></tr>
          <tr><td style="color:#a0aec0;">Date</td><td>{datetime.now().strftime('%d %b %Y, %I:%M %p')}</td></tr>
        </table>
        </div>
        """, unsafe_allow_html=True)

        if amount > 0:
            st.info("🔒 This is a demo environment. No real payment will be processed.")

        col_back, col_confirm = st.columns([1, 2])
        with col_back:
            if st.button("← Edit"):
                st.session_state.payment_step = "details" if amount > 0 else "select"
                st.rerun()
        with col_confirm:
            btn_label = f"✅ Confirm & Activate {target} Plan"
            if st.button(btn_label):
                # Record transaction
                txn = {
                    "txn_id": generate_txn_id(),
                    "plan":   target,
                    "amount": amount,
                    "method": st.session_state.get("payment_method", "Free"),
                    "status": "Success",
                    "date":   datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                fresh = load_users()
                if "transactions" not in fresh[st.session_state.username]:
                    fresh[st.session_state.username]["transactions"] = []
                fresh[st.session_state.username]["transactions"].append(txn)
                fresh[st.session_state.username]["plan"] = target
                save_users(fresh)

                st.session_state.plan         = target
                st.session_state.payment_step = "success"
                st.rerun()

    # ─────────────────────────────────────────────────────
    # STEP 4: Success
    # ─────────────────────────────────────────────────────
    elif step == "success":
        target = st.session_state.payment_target_plan
        p      = PLANS[target]
        fresh  = load_users()
        txns   = fresh[st.session_state.username].get("transactions", [])
        last   = txns[-1] if txns else {}

        st.markdown(f"""
        <div class="payment-success">
            <div style="font-size:60px;margin-bottom:10px;">🎉</div>
            <h2 style="color:#86efac;margin-bottom:8px;">Payment Successful!</h2>
            <p style="color:#d1fae5;font-size:16px;">
                You are now on the <b>{target} Plan</b>.<br>
                Your new features are active immediately.
            </p>
            <br>
            <div style="background:rgba(0,0,0,0.2);border-radius:10px;padding:14px 24px;display:inline-block;text-align:left;">
                <div style="color:#6ee7b7;font-size:13px;">Transaction ID: <b>{last.get('txn_id','N/A')}</b></div>
                <div style="color:#6ee7b7;font-size:13px;">Amount Paid: <b>₹{last.get('amount', 0):,}</b></div>
                <div style="color:#6ee7b7;font-size:13px;">Date: <b>{last.get('date','N/A')}</b></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🏠 Go to Home"):
                st.session_state.payment_step = "select"
                st.session_state.payment_target_plan = None
                st.rerun()
        with col2:
            if st.button("📊 Open Dashboard"):
                st.session_state.payment_step = "select"
                st.session_state.payment_target_plan = None
                st.rerun()

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

    st.subheader("📊 Feature Comparison")
    comp = pd.DataFrame({
        "Feature":  ["Routes visible", "Dashboard charts", "Route Insights", "Insights Page", "AI queries/day", "Price"],
        "Free":     ["3", "2", "❌", "❌", "0", "₹0/month"],
        "Basic":    ["10", "5", "✅", "❌", "5", "₹199/month"],
        "Premium":  ["All", "All (7)", "✅", "✅", "Unlimited", "₹499/month"],
    })
    st.dataframe(comp.set_index("Feature"), use_container_width=True)

    st.divider()
    st.markdown("To upgrade or change your plan, visit the **Payments** page from the sidebar.")

# ======================================================
# PAGE: ABOUT US
# ======================================================

def page_about():
    st.header("📌 About the Project")
    st.markdown("""
The **Public Transport Delay Analysis System** transforms raw transport data into meaningful
insights for both passengers and transport organizations.

- Route-wise delay patterns
- Congestion trends & seasonal impacts
- On-Time Performance (OTP)
- AI-powered travel insights
    """)
    st.divider()
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Routes",    "20+")
    c2.metric("Trips",     "20K+")
    c3.metric("Avg Delay", "7 mins")
    c4.metric("OTP",       "89%")
    st.divider()
    st.subheader("🚍 How It Helps Passengers")
    st.markdown("- Find frequently delayed routes\n- Know crowded timings\n- Get AI-generated travel insights")
    st.divider()
    st.subheader("🏢 How It Helps Transport Organizations")
    st.markdown("- Detect routes with repeated delays\n- Analyze congestion hotspots\n- Support data-driven planning")
    st.divider()

# ======================================================
# ADMIN: REVENUE DASHBOARD
# ======================================================

def page_revenue():
    st.title("💰 Subscription Revenue Dashboard")
    st.caption("Admin-only view — Revenue generated from user subscription plans")
    st.divider()

    sub_df = get_subscription_revenue_data()

    if sub_df.empty:
        st.info("No users have signed up yet. Revenue will appear here once users register.")
        return

    total_users       = len(sub_df)
    total_monthly_rev = sub_df["monthly_revenue"].sum()
    paying_users      = sub_df[sub_df["monthly_revenue"] > 0]
    free_users        = len(sub_df[sub_df["plan"] == "Free"])
    basic_users       = len(sub_df[sub_df["plan"] == "Basic"])
    premium_users     = len(sub_df[sub_df["plan"] == "Premium"])
    basic_rev         = basic_users   * PLANS["Basic"]["monthly_revenue"]
    premium_rev       = premium_users * PLANS["Premium"]["monthly_revenue"]
    projected_annual  = total_monthly_rev * 12

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Total Users",          total_users)
    k2.metric("Monthly Revenue",      f"₹{total_monthly_rev:,}")
    k3.metric("Paying Users",         len(paying_users))
    k4.metric("Projected Annual Rev", f"₹{projected_annual:,}")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("📦 Users per Plan")
    pc1, pc2, pc3 = st.columns(3)
    for col, pname, count, rev in zip(
        [pc1, pc2, pc3],
        ["Free", "Basic", "Premium"],
        [free_users, basic_users, premium_users],
        [0, basic_rev, premium_rev]
    ):
        p = PLANS[pname]
        col.markdown(f"""
        <div style="background:{p['badge_bg']};border:1px solid {p['color']};
        border-radius:16px;padding:22px;text-align:center;">
        <div style="color:{p['badge_text']};font-size:14px;font-weight:700;">{pname} Plan</div>
        <div style="color:white;font-size:38px;font-weight:800;margin:6px 0;">{count}</div>
        <div style="color:{p['badge_text']};font-size:13px;">users</div>
        <div style="color:{p['color']};font-size:15px;font-weight:700;margin-top:8px;">₹{rev:,}/month</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.divider()

    col1, col2 = st.columns(2)
    with col1:
        plan_counts = sub_df["plan"].value_counts().reset_index()
        plan_counts.columns = ["Plan", "Users"]
        fig1 = px.pie(plan_counts, names="Plan", values="Users",
                      title="👥 User Distribution by Plan", color="Plan",
                      color_discrete_map={"Free":"#4a5568","Basic":"#2b6cb0","Premium":"#6b21a8"})
        fig1.update_traces(textinfo="label+percent+value")
        fig1.update_layout(**COMMON_LAYOUT)
        st.plotly_chart(fig1, use_container_width=True)

    with col2:
        rev_data = pd.DataFrame({
            "Plan":    ["Free",   "Basic",    "Premium"],
            "Users":   [free_users, basic_users, premium_users],
            "Revenue": [0,          basic_rev,   premium_rev]
        })
        fig2 = px.bar(rev_data, x="Plan", y="Revenue", title="💰 Monthly Revenue by Plan",
                      color="Plan", text=rev_data["Revenue"].apply(lambda x: f"₹{x:,}"),
                      color_discrete_map={"Free":"#4a5568","Basic":"#2b6cb0","Premium":"#6b21a8"})
        fig2.update_traces(textposition="outside")
        fig2.update_layout(**COMMON_LAYOUT)
        st.plotly_chart(fig2, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        rev_share = pd.DataFrame({"Plan": ["Basic","Premium"], "Revenue": [basic_rev, premium_rev]})
        if rev_share["Revenue"].sum() > 0:
            fig3 = px.pie(rev_share, names="Plan", values="Revenue",
                          title="📊 Revenue Share (Paying Plans)", hole=0.45, color="Plan",
                          color_discrete_map={"Basic":"#2b6cb0","Premium":"#6b21a8"})
            fig3.update_traces(textinfo="label+percent")
            fig3.update_layout(**COMMON_LAYOUT)
            st.plotly_chart(fig3, use_container_width=True)
        else:
            st.info("No paying users yet.")

    with col4:
        arpu_data = pd.DataFrame({
            "Plan": ["Free","Basic","Premium"],
            "ARPU": [0, PLANS["Basic"]["monthly_revenue"], PLANS["Premium"]["monthly_revenue"]]
        })
        fig4 = px.bar(arpu_data, x="Plan", y="ARPU", title="💡 Revenue per User (ARPU) by Plan",
                      color="Plan", text=arpu_data["ARPU"].apply(lambda x: f"₹{x}"),
                      color_discrete_map={"Free":"#4a5568","Basic":"#2b6cb0","Premium":"#6b21a8"})
        fig4.update_traces(textposition="outside")
        fig4.update_layout(**COMMON_LAYOUT)
        st.plotly_chart(fig4, use_container_width=True)

    st.divider()
    st.subheader("🚀 Upgrade Revenue Potential")
    pot1, pot2, pot3 = st.columns(3)
    potential_if_all_basic   = total_users * PLANS["Basic"]["monthly_revenue"]
    potential_if_all_premium = total_users * PLANS["Premium"]["monthly_revenue"]
    revenue_gap              = potential_if_all_premium - total_monthly_rev
    pot1.metric("If all users → Basic",   f"₹{potential_if_all_basic:,}/mo")
    pot2.metric("If all users → Premium", f"₹{potential_if_all_premium:,}/mo")
    pot3.metric("Current Revenue Gap",    f"₹{revenue_gap:,}/mo")

    st.divider()
    st.subheader("👤 User Subscription Details")

    # Also show transaction totals per user
    fresh = load_users()
    rows  = []
    for uname, udata in fresh.items():
        if udata["role"] == "user":
            txns       = udata.get("transactions", [])
            total_paid = sum(t.get("amount", 0) for t in txns if t.get("status") == "Success")
            rows.append({
                "Name":              udata["name"],
                "Username":          uname,
                "Plan":              udata.get("plan", "Free"),
                "Monthly Rev (₹)":   PLANS[udata.get("plan","Free")]["monthly_revenue"],
                "Total Paid (₹)":    total_paid,
                "Transactions":      len(txns),
                "Joined":            udata.get("created_at","")[:10]
            })
    if rows:
        st.dataframe(pd.DataFrame(rows).sort_values("Monthly Rev (₹)", ascending=False), use_container_width=True)

    st.markdown("---")
    st.caption("💰 Subscription Revenue Dashboard • Admin View")

# ======================================================
# ADMIN: USER MANAGEMENT
# ======================================================

def page_user_management():
    st.title("👥 User Management")
    st.caption("Manage all registered users and their subscription plans")
    st.divider()

    fresh = load_users()
    plan_counts = {"Free": 0, "Basic": 0, "Premium": 0}
    for u, d in fresh.items():
        if d["role"] == "user":
            p = d.get("plan", "Free")
            plan_counts[p] = plan_counts.get(p, 0) + 1

    c1, c2, c3 = st.columns(3)
    for col, pname in zip([c1, c2, c3], ["Free", "Basic", "Premium"]):
        p = PLANS[pname]
        col.markdown(f"""
        <div style="background:{p['badge_bg']};border:1px solid {p['color']};
        border-radius:14px;padding:16px;text-align:center;">
        <div style="color:{p['badge_text']};font-size:12px;font-weight:600;">{pname}</div>
        <div style="color:white;font-size:30px;font-weight:800;">{plan_counts.get(pname, 0)}</div>
        <div style="color:{p['badge_text']};font-size:11px;">users</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    user_list = [
        {
            "Username": u,
            "Name":     d["name"],
            "Role":     d["role"],
            "Plan":     d.get("plan", "Free"),
            "Transactions": len(d.get("transactions", [])),
            "Joined":   d["created_at"][:10]
        }
        for u, d in fresh.items()
    ]
    st.dataframe(pd.DataFrame(user_list), use_container_width=True)
# ======================================================
# MAIN ROUTER
# ======================================================

if not st.session_state.logged_in:
    login_page()
else:
    page = render_sidebar()

    if st.session_state.role == "admin":
        if   page == "Revenue Dashboard":     page_revenue()
        elif page == "User Management":       page_user_management()
    else:
        if   page == "Home":                  page_home()
        elif page == "Operational Dashboard": page_operational_dashboard()
        elif page == "Route Insights":        page_route_insights()
        elif page == "Insights":              page_insights()
        elif page == "My Profile":            page_profile()
        elif page == "Payments":              page_payments()
        elif page == "About Us":              page_about()
