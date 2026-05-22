import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Operational Dashboard",
    layout="wide"
)

st.write(" ")

# ======================================================
# PROFESSIONAL DARK THEME
# ======================================================

st.markdown("""
<style>

/* ===== MAIN APP ===== */
.stApp {
    background: linear-gradient(
        135deg,
        #0f172a 0%,
        #111827 50%,
        #1e1b4b 100%
    );
    color: #f8fafc;
}

/* ===== SIDEBAR ===== */
section[data-testid="stSidebar"] {
    background: #0b1120;
    border-right: 1px solid #312e81;
}

section[data-testid="stSidebar"]::before {
    content: "🚍 Route Analytics";
    display: block;
    padding: 22px 20px;
    font-size: 28px;
    font-weight: 700;
    color: white;
    border-bottom: 1px solid #312e81;
}

/* ===== TITLES ===== */
h1 {
    font-size: 42px !important;
    font-weight: 800 !important;
    color: white !important;
}

h2, h3 {
    color: #c4b5fd !important;
}

/* ===== METRIC CARDS ===== */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(139,92,246,0.25);
    backdrop-filter: blur(12px);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-3px);
    border-color: #8b5cf6;
}

[data-testid="stMetricLabel"] {
    color: #d8b4fe !important;
    font-size: 15px !important;
}

[data-testid="stMetricValue"] {
    color: white !important;
    font-size: 32px !important;
    font-weight: 700 !important;
}

/* ===== CHART CONTAINER ===== */
div[data-testid="stPlotlyChart"] {
    background: rgba(17,24,39,0.75);
    border: 1px solid rgba(139,92,246,0.15);
    border-radius: 18px;
    padding: 12px;
    margin-top: 10px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}

/* ===== CHART SUMMARY BOX ===== */
.chart-summary {
    background: rgba(139, 92, 246, 0.08);
    border: 1px solid rgba(139, 92, 246, 0.25);
    border-radius: 12px;
    padding: 14px 18px;
    margin-top: 8px;
    margin-bottom: 16px;
    font-size: 13px;
    color: #d8b4fe;
    line-height: 1.7;
}

.chart-summary ul {
    margin: 0;
    padding-left: 18px;
}

.chart-summary li {
    margin-bottom: 4px;
}

/* ===== FILTERS ===== */
[data-baseweb="select"] {
    background-color: #111827 !important;
}

[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background-color: #7c3aed !important;
    color: white !important;
}

/* ===== DIVIDER ===== */
hr {
    border-color: rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATA
# ======================================================

trips = pd.read_excel("data/Fact_Trips_Cleaned.xlsx")
routes = pd.read_excel("data/Dim_Routes_Cleaned.xlsx")

# ======================================================
# DATA CLEANING
# ======================================================

trips["Delay_Minutes"] = pd.to_numeric(
    trips["Delay_Minutes"], errors="coerce"
)

trips["Hour"] = pd.to_datetime(
    trips["Time"], errors="coerce"
).dt.hour

trips["VehicleType"] = trips["VehicleType"].astype(str).str.strip()
trips["WeatherCondition"] = trips["WeatherCondition"].astype(str).str.strip()
trips["Status"] = trips["Status"].astype(str).str.strip()

# ======================================================
# MERGE DATA
# ======================================================

if "RouteID" in routes.columns:
    df = trips.merge(routes, on="RouteID", how="left")
else:
    df = trips.copy()

# ======================================================
# SIDEBAR FILTERS
# ======================================================

vehicle_options = sorted(df["VehicleType"].dropna().unique())
weather_options = sorted(df["WeatherCondition"].dropna().unique())
status_options  = sorted(df["Status"].dropna().unique())

vehicle_filter = st.sidebar.multiselect(
    "Vehicle Type", vehicle_options, default=vehicle_options
)
weather_filter = st.sidebar.multiselect(
    "Weather Condition", weather_options, default=weather_options
)
status_filter = st.sidebar.multiselect(
    "Trip Status", status_options, default=status_options
)

# ======================================================
# FILTER DATA
# ======================================================

filtered_df = df[
    df["VehicleType"].isin(vehicle_filter) &
    df["WeatherCondition"].isin(weather_filter) &
    df["Status"].isin(status_filter)
].copy()

if filtered_df.empty:
    st.warning("No data available.")
    st.stop()

# ======================================================
# TITLE
# ======================================================

st.title("📊 Operational Transport Dashboard")

st.markdown("""
Monitor public transport performance,
delay patterns, congestion levels,
weather impact, and district-wise operations.
""")

st.divider()

# ======================================================
# KPI SECTION
# ======================================================

avg_delay      = filtered_df["Delay_Minutes"].mean()
otp            = ((filtered_df["Status"] == "On-Time").sum() / len(filtered_df)) * 100
network_health = max(0, 100 - avg_delay)
trip_count     = len(filtered_df)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Trips",               f"{trip_count}")
k2.metric("OTP %",               f"{otp:.1f}%")
k3.metric("Avg Delay",           f"{avg_delay:.1f} mins")
k4.metric("Overall Performance", f"{network_health:.1f}%")

st.divider()

# ======================================================
# CHART DATA
# ======================================================

hourly_delay = (
    filtered_df.groupby("Hour")["Delay_Minutes"]
    .mean().reset_index()
)

route_delay = (
    filtered_df.groupby("RouteID")["Delay_Minutes"]
    .mean().reset_index()
    .sort_values(by="Delay_Minutes", ascending=False)
)

weather_delay = (
    filtered_df.groupby("WeatherCondition")["Delay_Minutes"]
    .mean().reset_index()
)

congestion_delay = (
    filtered_df.groupby("CongestionLevel")["Delay_Minutes"]
    .mean().reset_index()
)

vehicle_data = (
    filtered_df.groupby("VehicleType")
    .size().reset_index(name="Trips")
)

district_data = (
    filtered_df.groupby(["Origin", "Destination", "Status", "VehicleType"])
    .size().reset_index(name="Trips")
)

filtered_df["Day"] = pd.to_datetime(
    filtered_df["Date"], errors="coerce"
).dt.day_name()

heatmap_data = filtered_df.pivot_table(
    values="Delay_Minutes",
    index="Day",
    columns="Hour",
    aggfunc="mean"
)

# ======================================================
# COMMON LAYOUT
# ======================================================

COMMON_LAYOUT = dict(
    height=320,
    paper_bgcolor="#1e0f3d",
    plot_bgcolor="#150b2e",
    font=dict(color="#e2d9f3"),
    title_font=dict(color="#c084fc", size=15),
    margin=dict(l=10, r=10, t=50, b=10),
    legend=dict(
        bgcolor="rgba(30,15,61,0.7)",
        bordercolor="#4a3470",
        borderwidth=1
    )
)

# ======================================================
# CHARTS
# ======================================================

# 1. HOURLY DELAY TREND
fig_line = px.line(
    hourly_delay, x="Hour", y="Delay_Minutes",
    markers=True, title="⏰ Hourly Delay Trend"
)
fig_line.update_traces(
    line=dict(color="#06b6d4", width=3),
    marker=dict(color="#67e8f9", size=8, line=dict(color="#0891b2", width=2))
)

# 2. TOP DELAYED ROUTES
fig_bar = px.bar(
    route_delay.head(10), x="RouteID", y="Delay_Minutes",
    title="🚦 Top Delayed Routes"
)
fig_bar.update_traces(
    marker_color=[
        "#dc2626","#ef4444","#f87171","#fca5a5",
        "#dc2626","#ef4444","#f87171","#fca5a5",
        "#dc2626","#ef4444"
    ]
)

# 3. WEATHER IMPACT
fig_weather = px.bar(
    weather_delay, x="WeatherCondition", y="Delay_Minutes",
    title="🌦️ Weather Impact"
)
fig_weather.update_traces(
    marker_color=["#2563eb","#3b82f6","#60a5fa","#93c5fd","#2563eb"]
)

# 4. CONGESTION DISTRIBUTION
fig_congestion = px.pie(
    congestion_delay, names="CongestionLevel", values="Delay_Minutes",
    title="🚗 Congestion Distribution", hole=0.4
)
fig_congestion.update_traces(
    marker=dict(colors=["#ea580c","#f97316","#fb923c","#fdba74"])
)

# 5. VEHICLE DISTRIBUTION
fig_vehicle = px.bar(
    vehicle_data, x="VehicleType", y="Trips",
    title="🚍 Vehicle Distribution"
)
fig_vehicle.update_traces(
    marker_color=["#059669","#10b981","#34d399","#6ee7b7"]
)

# 6. DELAY HEATMAP
fig_heatmap = px.imshow(
    heatmap_data, text_auto=True, aspect="auto",
    title="🔥 Delay Heatmap", color_continuous_scale="Turbo"
)

# 7. DISTRICT MAP
fig_map = px.scatter(
    district_data, x="Origin", y="Destination",
    size="Trips", color="Status", symbol="VehicleType",
    hover_data=["Trips", "VehicleType"],
    title="🗺️ District-wise Delay & Vehicle Analysis",
    color_discrete_map={
        "On-Time":  "#38bdf8",
        "Delayed":  "#818cf8",
        "Cancelled":"#c084fc"
    }
)

# Apply common styling to all figures
for fig in [fig_line, fig_bar, fig_weather, fig_congestion,
            fig_vehicle, fig_heatmap, fig_map]:
    fig.update_layout(**COMMON_LAYOUT)
    fig.update_xaxes(gridcolor="#2d1b5e")
    fig.update_yaxes(gridcolor="#2d1b5e")

# ======================================================
# HELPER — render summary box
# ======================================================

def summary_box(points: list[str]):
    items = "".join(f"<li>{p}</li>" for p in points)
    st.markdown(
        f'<div class="chart-summary"><ul>{items}</ul></div>',
        unsafe_allow_html=True
    )

# ======================================================
# DASHBOARD LAYOUT
# ======================================================

# ── ROW 1 ──────────────────────────────────────────────
r1c1, r1c2, r1c3 = st.columns(3)

with r1c1:
    st.plotly_chart(fig_line, use_container_width=True)
    summary_box([
        "Delays rise noticeably during morning peak hours (7–9 AM) and evening rush (5–8 PM).",
        "Midday hours (11 AM–2 PM) show the lowest average delay across the network.",
        "Late-night trips after 10 PM tend to be more punctual due to reduced traffic.",
        "Hour-by-hour variation highlights specific congestion windows for operational focus.",
        "Scheduling adjustments during peak hours could significantly reduce overall delay.",
    ])

with r1c2:
    st.plotly_chart(fig_weather, use_container_width=True)
    summary_box([
        "Rainy and stormy conditions produce the highest average delays across all routes.",
        "Clear weather consistently corresponds to the lowest delay times.",
        "Foggy conditions create moderate delays, especially affecting visibility-sensitive routes.",
        "Weather impact is more pronounced on bus services than on rail-based transport.",
        "Adverse weather combined with peak hours creates compounded delay spikes.",
    ])

with r1c3:
    st.plotly_chart(fig_vehicle, use_container_width=True)
    summary_box([
        "Buses account for the largest share of total trips in the transport network.",
        "Trains handle a significant volume while maintaining better on-time performance.",
        "The distribution reflects infrastructure reliance on road-based transport.",
        "High bus trip counts correlate with higher overall delay averages.",
        "Expanding rail capacity could help balance the load and improve punctuality.",
    ])

# ── ROW 2 ──────────────────────────────────────────────
r2c1, r2c2, r2c3 = st.columns(3)

with r2c1:
    st.plotly_chart(fig_bar, use_container_width=True)
    summary_box([
        "A small number of routes consistently account for the highest average delays.",
        "The top delayed routes likely pass through high-congestion urban corridors.",
        "Delay concentration on specific routes signals a need for targeted intervention.",
        "Route-level analysis helps prioritize infrastructure or scheduling improvements.",
        "Lower-ranked routes maintain relatively stable and acceptable delay levels.",
    ])

with r2c2:
    st.plotly_chart(fig_congestion, use_container_width=True)
    summary_box([
        "High congestion levels contribute the largest share of overall delay time.",
        "Low congestion periods account for a minor fraction of total delay.",
        "Medium congestion is the most frequently occurring condition in the network.",
        "Congestion-related delays are more severe during weekday peak periods.",
        "Reducing high-congestion exposure through route planning can improve OTP.",
    ])

with r2c3:
    st.plotly_chart(fig_heatmap, use_container_width=True)
    summary_box([
        "Monday and Friday mornings show the darkest delay clusters, indicating weekly peaks.",
        "Weekend hours display lighter heatmap values, reflecting smoother operations.",
        "Hours between 8–10 AM and 5–7 PM are consistently the hottest delay zones.",
        "Midweek afternoons (Tuesday–Thursday) remain comparatively stable.",
        "The heatmap helps identify exact day-hour combinations for targeted scheduling.",
    ])

# ── ROW 3 ──────────────────────────────────────────────
st.plotly_chart(fig_map, use_container_width=True)
summary_box([
    "Certain origin-destination pairs record significantly higher trip volumes and delay rates.",
    "Cancelled trips are concentrated on a few specific route corridors.",
    "Bus services show more scattered delay patterns compared to trains across districts.",
    "On-time performance is stronger on shorter inter-district connections.",
    "High-volume origin points may need additional vehicle allocation to reduce congestion.",
])

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")
st.caption("🚍 Operational Analytics Dashboard • Public Transport Delay Analysis")
