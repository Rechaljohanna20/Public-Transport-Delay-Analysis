# import streamlit as st
# import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go

# # ======================================================
# # PAGE CONFIG
# # ======================================================

# st.set_page_config(
#     page_title="Operational Dashboard",
#     layout="wide"
# )
# st.write(" ")

# # ======================================================
# # DARK VIOLET THEME
# # ======================================================

# st.markdown("""
# <style>

# /* ---- Sidebar Title ---- */
# section[data-testid="stSidebar"]::before {
#     content: "🚍 Route Analytics";
#     display: block;
#     margin-top: 70px;
#     padding: 0px 20px 15px 20px;
#     font-size: 26px;
#     font-weight: bold;
#     color: #e2d9f3;
#     border-bottom: 1px solid #4a3470;
# }

# /* ---- Sidebar Background ---- */
# section[data-testid="stSidebar"] {
#     background-color: #1a0f2e;
# }

# /* ---- App Background ---- */
# .stApp {
#     background-color: #120a24;
#     color: #e2d9f3;
# }

# /* ---- Metric Tiles ---- */
# [data-testid="stMetric"] {
#     background: linear-gradient(135deg, #2d1b5e 0%, #3d2275 100%);
#     border: 1px solid #6b3fa0;
#     padding: 16px;
#     border-radius: 12px;
#     text-align: center;
#     box-shadow: 0 4px 15px rgba(107, 63, 160, 0.3);
# }

# [data-testid="stMetricLabel"] {
#     color: #c4b0e8 !important;
#     font-size: 0.85rem;
#     letter-spacing: 0.05em;
#     text-transform: uppercase;
# }

# [data-testid="stMetricValue"] {
#     color: #f0eaff !important;
#     font-weight: 700;
# }

# /* ---- Headings ---- */
# h1, h2, h3 {
#     color: #c084fc !important;
# }

# /* ---- Plotly Chart Container ---- */
# div[data-testid="stPlotlyChart"] {
#     background: linear-gradient(135deg, #1e0f3d 0%, #2a1555 100%);
#     padding: 10px;
#     border-radius: 14px;
#     border: 1px solid #4a3470;
#     box-shadow: 0 4px 20px rgba(90, 40, 160, 0.2);
# }

# /* ---- Sidebar multiselect labels ---- */
# .stMultiSelect label, .stMultiSelect span {
#     color: #c4b0e8 !important;
# }

# /* ---- Sidebar filter pills ---- */
# [data-testid="stMultiSelect"] span[data-baseweb="tag"] {
#     background-color: #5b21b6 !important;
#     color: #f0eaff !important;
# }

# /* ---- Divider ---- */
# hr {
#     border-color: #4a3470 !important;
# }

# /* ---- General text ---- */
# p, span, label {
#     color: #d8cef0;
# }

# /* ---- Caption ---- */
# .stCaption {
#     color: #9d86c4 !important;
# }

# </style>
# """, unsafe_allow_html=True)

# # ======================================================
# # LOAD DATA
# # ======================================================

# trips = pd.read_excel("data/Fact_Trips_Cleaned.xlsx")
# routes = pd.read_excel("data/Dim_Routes_cleaned.xlsx")

# # ======================================================
# # DATA CLEANING
# # ======================================================

# trips["Delay_Minutes"] = pd.to_numeric(
#     trips["Delay_Minutes"],
#     errors="coerce"
# )

# trips["Hour"] = pd.to_datetime(
#     trips["Time"],
#     errors="coerce"
# ).dt.hour

# trips["VehicleType"] = (
#     trips["VehicleType"]
#     .astype(str)
#     .str.strip()
# )

# trips["WeatherCondition"] = (
#     trips["WeatherCondition"]
#     .astype(str)
#     .str.strip()
# )

# trips["Status"] = (
#     trips["Status"]
#     .astype(str)
#     .str.strip()
# )

# # ======================================================
# # MERGE ROUTE DATA
# # ======================================================

# if "RouteID" in routes.columns:
#     df = trips.merge(routes, on="RouteID", how="left")
# else:
#     df = trips.copy()

# # ======================================================
# # SIDEBAR FILTERS
# # ======================================================

# vehicle_options = sorted(df["VehicleType"].dropna().unique())
# weather_options = sorted(df["WeatherCondition"].dropna().unique())
# status_options = sorted(df["Status"].dropna().unique())

# vehicle_filter = st.sidebar.multiselect(
#     "Vehicle Type", vehicle_options, default=vehicle_options, key="vehicle_filter"
# )

# weather_filter = st.sidebar.multiselect(
#     "Weather Condition", weather_options, default=weather_options, key="weather_filter"
# )

# status_filter = st.sidebar.multiselect(
#     "Trip Status", status_options, default=status_options, key="status_filter"
# )

# # ======================================================
# # FILTER DATA
# # ======================================================

# filtered_df = df[
#     df["VehicleType"].isin(vehicle_filter) &
#     df["WeatherCondition"].isin(weather_filter) &
#     df["Status"].isin(status_filter)
# ].copy()

# if filtered_df.empty:
#     st.warning("No data available.")
#     st.stop()

# # ======================================================
# # PAGE TITLE
# # ======================================================

# st.title("📊 Operational Transport Dashboard")

# st.markdown("""
# Monitor public transport performance,
# delay patterns, congestion levels,
# weather impact, and district-wise operations.
# """)

# st.divider()

# # ======================================================
# # KPI SECTION
# # ======================================================

# avg_delay = filtered_df["Delay_Minutes"].mean()
# otp = ((filtered_df["Status"] == "On-Time").sum() / len(filtered_df)) * 100
# network_health = max(0, 100 - avg_delay)
# trip_count = len(filtered_df)

# k1, k2, k3, k4 = st.columns(4)
# k1.metric("Trips", f"{trip_count}")
# k2.metric("OTP %", f"{otp:.1f}%")
# k3.metric("Avg Delay", f"{avg_delay:.1f} mins")
# k4.metric("Network Health", f"{network_health:.1f}%")

# st.divider()

# # ======================================================
# # CHART DATA
# # ======================================================

# hourly_delay = (
#     filtered_df.groupby("Hour")["Delay_Minutes"].mean().reset_index()
# )

# route_delay = (
#     filtered_df.groupby("RouteID")["Delay_Minutes"]
#     .mean().reset_index()
#     .sort_values(by="Delay_Minutes", ascending=False)
# )

# weather_delay = (
#     filtered_df.groupby("WeatherCondition")["Delay_Minutes"].mean().reset_index()
# )

# congestion_delay = (
#     filtered_df.groupby("CongestionLevel")["Delay_Minutes"].mean().reset_index()
# )

# vehicle_data = (
#     filtered_df.groupby("VehicleType").size().reset_index(name="Trips")
# )

# district_data = (
#     filtered_df.groupby(["Origin", "Destination", "Status", "VehicleType"])
#     .size().reset_index(name="Trips")
# )

# filtered_df["Day"] = pd.to_datetime(
#     filtered_df["Date"], errors="coerce"
# ).dt.day_name()

# heatmap_data = filtered_df.pivot_table(
#     values="Delay_Minutes", index="Day", columns="Hour", aggfunc="mean"
# )

# # ======================================================
# # VIOLET COLOR PALETTE
# # ======================================================

# VIOLET_SEQ = [
#     "#3b0764", "#5b21b6", "#7c3aed", "#a855f7",
#     "#c084fc", "#d8b4fe", "#ede9fe"
# ]

# BG_TILE   = "#1e0f3d"
# BG_PLOT   = "#150b2e"
# FONT_CLR  = "#e2d9f3"
# BORDER    = "#4a3470"

# COMMON_LAYOUT = dict(
#     height=320,
#     paper_bgcolor=BG_TILE,
#     plot_bgcolor=BG_PLOT,
#     font_color=FONT_CLR,
#     margin=dict(l=10, r=10, t=45, b=10),
#     title_font=dict(color="#c084fc", size=14),
#     legend=dict(
#         bgcolor="rgba(30,15,61,0.7)",
#         bordercolor=BORDER,
#         borderwidth=1,
#         font=dict(color=FONT_CLR)
#     )
# )

# # ======================================================
# # CHARTS
# # ======================================================

# # Hourly Delay Trend
# fig_line = px.line(
#     hourly_delay, x="Hour", y="Delay_Minutes",
#     markers=True, title="⏰ Hourly Delay Trend",
#     color_discrete_sequence=["#a855f7"]
# )
# fig_line.update_traces(
#     line=dict(width=2.5),
#     marker=dict(size=7, color="#c084fc", line=dict(color="#7c3aed", width=1.5))
# )
# fig_line.update_layout(**COMMON_LAYOUT)
# fig_line.update_xaxes(gridcolor="#2d1b5e", zerolinecolor="#2d1b5e")
# fig_line.update_yaxes(gridcolor="#2d1b5e", zerolinecolor="#2d1b5e")

# # Top Delayed Routes
# fig_bar = px.bar(
#     route_delay.head(10), x="RouteID", y="Delay_Minutes",
#     color="Delay_Minutes", title="🚦 Top Delayed Routes",
#     color_continuous_scale=VIOLET_SEQ
# )
# fig_bar.update_layout(**COMMON_LAYOUT)
# fig_bar.update_xaxes(gridcolor="#2d1b5e")
# fig_bar.update_yaxes(gridcolor="#2d1b5e")

# # Weather Impact
# fig_weather = px.bar(
#     weather_delay, x="WeatherCondition", y="Delay_Minutes",
#     color="WeatherCondition", title="🌦️ Weather Impact",
#     color_discrete_sequence=VIOLET_SEQ
# )
# fig_weather.update_layout(**COMMON_LAYOUT)
# fig_weather.update_xaxes(gridcolor="#2d1b5e")
# fig_weather.update_yaxes(gridcolor="#2d1b5e")

# # Congestion Distribution
# fig_congestion = px.pie(
#     congestion_delay, names="CongestionLevel", values="Delay_Minutes",
#     title="🚗 Congestion Distribution",
#     color_discrete_sequence=VIOLET_SEQ,
#     hole=0.35
# )
# fig_congestion.update_traces(
#     textfont_color=FONT_CLR,
#     marker=dict(line=dict(color=BG_TILE, width=2))
# )
# fig_congestion.update_layout(**COMMON_LAYOUT)

# # Vehicle Distribution
# fig_vehicle = px.bar(
#     vehicle_data, x="VehicleType", y="Trips",
#     color="VehicleType", title="🚍 Vehicle Distribution",
#     color_discrete_sequence=VIOLET_SEQ
# )
# fig_vehicle.update_layout(**COMMON_LAYOUT)
# fig_vehicle.update_xaxes(gridcolor="#2d1b5e")
# fig_vehicle.update_yaxes(gridcolor="#2d1b5e")

# # Delay Heatmap
# fig_heatmap = px.imshow(
#     heatmap_data, text_auto=True, aspect="auto",
#     title="🔥 Delay Heatmap",
#     color_continuous_scale=VIOLET_SEQ
# )
# fig_heatmap.update_layout(**COMMON_LAYOUT)

# # District-wise Map
# fig_map = px.scatter(
#     district_data, x="Origin", y="Destination",
#     size="Trips", color="Status", symbol="VehicleType",
#     hover_data=["Trips", "VehicleType"],
#     title="🗺️ District-wise Delay & Vehicle Analysis",
#     color_discrete_sequence=VIOLET_SEQ
# )
# fig_map.update_layout(**COMMON_LAYOUT)
# fig_map.update_xaxes(gridcolor="#2d1b5e")
# fig_map.update_yaxes(gridcolor="#2d1b5e")

# # ======================================================
# # DASHBOARD LAYOUT
# # ======================================================

# # ROW 1
# r1c1, r1c2, r1c3 = st.columns(3)
# with r1c1:
#     st.plotly_chart(fig_line, use_container_width=True)
# with r1c2:
#     st.plotly_chart(fig_weather, use_container_width=True)
# with r1c3:
#     st.plotly_chart(fig_vehicle, use_container_width=True)

# # ROW 2
# r2c1, r2c2, r2c3 = st.columns(3)
# with r2c1:
#     st.plotly_chart(fig_bar, use_container_width=True)
# with r2c2:
#     st.plotly_chart(fig_congestion, use_container_width=True)
# with r2c3:
#     st.plotly_chart(fig_heatmap, use_container_width=True)

# # ROW 3
# st.plotly_chart(fig_map, use_container_width=True)

# # ======================================================
# # FOOTER
# # ======================================================

# st.markdown("---")
# st.caption("🚍 Operational Analytics Dashboard • Public Transport Delay Analysis")





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
# DARK VIOLET THEME
# ======================================================

st.markdown("""
<style>

/* ---- Sidebar Title ---- */
section[data-testid="stSidebar"]::before {
    content: "🚍 Route Analytics";
    display: block;
    margin-top: 70px;
    padding: 0px 20px 15px 20px;
    font-size: 26px;
    font-weight: bold;
    color: #e2d9f3;
    border-bottom: 1px solid #4a3470;
}



/* ---- App Background ---- */
.stApp {
    color: #e2d9f3;
}

/* ---- Metric Tiles ---- */
[data-testid="stMetric"] {
    border: 1px solid #6b3fa0;
    padding: 16px;
    border-radius: 12px;
    text-align: center;
}

[data-testid="stMetricLabel"] {
    color: #c4b0e8 !important;
    font-size: 0.85rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

[data-testid="stMetricValue"] {
    color: #f0eaff !important;
    font-weight: 700;
}

/* ---- Headings ---- */
h1, h2, h3 {
    color: #c084fc !important;
}

/* ---- Plotly Chart Container ---- */
div[data-testid="stPlotlyChart"] {
    background: linear-gradient(135deg, #1e0f3d 0%, #2a1555 100%);
    padding: 10px;
    border-radius: 14px;
    border: 1px solid #4a3470;
    box-shadow: 0 4px 20px rgba(90, 40, 160, 0.2);
}

/* ---- Sidebar multiselect labels ---- */
.stMultiSelect label, .stMultiSelect span {
    color: #c4b0e8 !important;
}

/* ---- Sidebar filter pills ---- */
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background-color: #5b21b6 !important;
    color: #f0eaff !important;
}

/* ---- Divider ---- */
hr {
    border-color: #4a3470 !important;
}

/* ---- General text ---- */
p, span, label {
    color: #d8cef0;
}

/* ---- Caption ---- */
.stCaption {
    color: #9d86c4 !important;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATA
# ======================================================

trips = pd.read_excel("data/Fact_Trips_Cleaned.xlsx")
routes = pd.read_excel("data/Dim_Routes_cleaned.xlsx")

# ======================================================
# DATA CLEANING
# ======================================================

trips["Delay_Minutes"] = pd.to_numeric(
    trips["Delay_Minutes"],
    errors="coerce"
)

trips["Hour"] = pd.to_datetime(
    trips["Time"],
    errors="coerce"
).dt.hour

trips["VehicleType"] = (
    trips["VehicleType"]
    .astype(str)
    .str.strip()
)

trips["WeatherCondition"] = (
    trips["WeatherCondition"]
    .astype(str)
    .str.strip()
)

trips["Status"] = (
    trips["Status"]
    .astype(str)
    .str.strip()
)

# ======================================================
# MERGE ROUTE DATA
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
status_options = sorted(df["Status"].dropna().unique())

vehicle_filter = st.sidebar.multiselect(
    "Vehicle Type", vehicle_options, default=vehicle_options, key="vehicle_filter"
)

weather_filter = st.sidebar.multiselect(
    "Weather Condition", weather_options, default=weather_options, key="weather_filter"
)

status_filter = st.sidebar.multiselect(
    "Trip Status", status_options, default=status_options, key="status_filter"
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
# PAGE TITLE
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

avg_delay = filtered_df["Delay_Minutes"].mean()
otp = ((filtered_df["Status"] == "On-Time").sum() / len(filtered_df)) * 100
network_health = max(0, 100 - avg_delay)
trip_count = len(filtered_df)

k1, k2, k3, k4 = st.columns(4)
k1.metric("Trips", f"{trip_count}")
k2.metric("OTP %", f"{otp:.1f}%")
k3.metric("Avg Delay", f"{avg_delay:.1f} mins")
k4.metric("Overall Performance", f"{network_health:.1f}%")

st.divider()

# ======================================================
# CHART DATA
# ======================================================

hourly_delay = (
    filtered_df.groupby("Hour")["Delay_Minutes"].mean().reset_index()
)

route_delay = (
    filtered_df.groupby("RouteID")["Delay_Minutes"]
    .mean().reset_index()
    .sort_values(by="Delay_Minutes", ascending=False)
)

weather_delay = (
    filtered_df.groupby("WeatherCondition")["Delay_Minutes"].mean().reset_index()
)

congestion_delay = (
    filtered_df.groupby("CongestionLevel")["Delay_Minutes"].mean().reset_index()
)

vehicle_data = (
    filtered_df.groupby("VehicleType").size().reset_index(name="Trips")
)

district_data = (
    filtered_df.groupby(["Origin", "Destination", "Status", "VehicleType"])
    .size().reset_index(name="Trips")
)

filtered_df["Day"] = pd.to_datetime(
    filtered_df["Date"], errors="coerce"
).dt.day_name()

heatmap_data = filtered_df.pivot_table(
    values="Delay_Minutes", index="Day", columns="Hour", aggfunc="mean"
)

# ======================================================
# VIOLET COLOR PALETTE
# ======================================================

VIOLET_SEQ = [
    "#3b0764", "#5b21b6", "#7c3aed", "#a855f7",
    "#c084fc", "#d8b4fe", "#ede9fe"
]

BG_TILE   = "#1e0f3d"
BG_PLOT   = "#150b2e"
FONT_CLR  = "#e2d9f3"
BORDER    = "#4a3470"

COMMON_LAYOUT = dict(
    height=320,
    paper_bgcolor=BG_TILE,
    plot_bgcolor=BG_PLOT,
    font_color=FONT_CLR,
    margin=dict(l=10, r=10, t=45, b=10),
    title_font=dict(color="#c084fc", size=14),
    legend=dict(
        bgcolor="rgba(30,15,61,0.7)",
        bordercolor=BORDER,
        borderwidth=1,
        font=dict(color=FONT_CLR)
    )
)

# ======================================================
# CHARTS
# ======================================================

# Hourly Delay Trend
fig_line = px.line(
    hourly_delay, x="Hour", y="Delay_Minutes",
    markers=True, title="⏰ Hourly Delay Trend",
    color_discrete_sequence=["#a855f7"]
)
fig_line.update_traces(
    line=dict(width=2.5),
    marker=dict(size=7, color="#c084fc", line=dict(color="#7c3aed", width=1.5))
)
fig_line.update_layout(**COMMON_LAYOUT)
fig_line.update_xaxes(gridcolor="#2d1b5e", zerolinecolor="#2d1b5e")
fig_line.update_yaxes(gridcolor="#2d1b5e", zerolinecolor="#2d1b5e")

# Top Delayed Routes
fig_bar = px.bar(
    route_delay.head(10), x="RouteID", y="Delay_Minutes",
    color="Delay_Minutes", title="🚦 Top Delayed Routes",
    color_continuous_scale=VIOLET_SEQ
)
fig_bar.update_layout(**COMMON_LAYOUT)
fig_bar.update_xaxes(gridcolor="#2d1b5e")
fig_bar.update_yaxes(gridcolor="#2d1b5e")

# Weather Impact
fig_weather = px.bar(
    weather_delay, x="WeatherCondition", y="Delay_Minutes",
    color="WeatherCondition", title="🌦️ Weather Impact",
    color_discrete_sequence=VIOLET_SEQ
)
fig_weather.update_layout(**COMMON_LAYOUT)
fig_weather.update_xaxes(gridcolor="#2d1b5e")
fig_weather.update_yaxes(gridcolor="#2d1b5e")

# Congestion Distribution
fig_congestion = px.pie(
    congestion_delay, names="CongestionLevel", values="Delay_Minutes",
    title="🚗 Congestion Distribution",
    color_discrete_sequence=VIOLET_SEQ,
    hole=0.35
)
fig_congestion.update_traces(
    textfont_color=FONT_CLR,
    marker=dict(line=dict(color=BG_TILE, width=2))
)
fig_congestion.update_layout(**COMMON_LAYOUT)

# Vehicle Distribution
fig_vehicle = px.bar(
    vehicle_data, x="VehicleType", y="Trips",
    color="VehicleType", title="🚍 Vehicle Distribution",
    color_discrete_sequence=VIOLET_SEQ
)
fig_vehicle.update_layout(**COMMON_LAYOUT)
fig_vehicle.update_xaxes(gridcolor="#2d1b5e")
fig_vehicle.update_yaxes(gridcolor="#2d1b5e")

# Delay Heatmap
fig_heatmap = px.imshow(
    heatmap_data, text_auto=True, aspect="auto",
    title="🔥 Delay Heatmap",
    color_continuous_scale=VIOLET_SEQ
)
fig_heatmap.update_layout(**COMMON_LAYOUT)

# District-wise Map
fig_map = px.scatter(
    district_data, x="Origin", y="Destination",
    size="Trips", color="Status", symbol="VehicleType",
    hover_data=["Trips", "VehicleType"],
    title="🗺️ District-wise Delay & Vehicle Analysis",
    color_discrete_sequence=VIOLET_SEQ
)
fig_map.update_layout(**COMMON_LAYOUT)
fig_map.update_xaxes(gridcolor="#2d1b5e")
fig_map.update_yaxes(gridcolor="#2d1b5e")

# ======================================================
# DASHBOARD LAYOUT
# ======================================================

# ROW 1
r1c1, r1c2, r1c3 = st.columns(3)
with r1c1:
    st.plotly_chart(fig_line, use_container_width=True)
with r1c2:
    st.plotly_chart(fig_weather, use_container_width=True)
with r1c3:
    st.plotly_chart(fig_vehicle, use_container_width=True)

# ROW 2
r2c1, r2c2, r2c3 = st.columns(3)
with r2c1:
    st.plotly_chart(fig_bar, use_container_width=True)
with r2c2:
    st.plotly_chart(fig_congestion, use_container_width=True)
with r2c3:
    st.plotly_chart(fig_heatmap, use_container_width=True)

# ROW 3
st.plotly_chart(fig_map, use_container_width=True)

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")
st.caption("🚍 Operational Analytics Dashboard • Public Transport Delay Analysis")