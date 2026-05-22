import streamlit as st
import pandas as pd

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(page_title="Insights", layout="wide")

# ======================================================
# CSS
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
    content: "🚍 Route Analytics";
    display: block;
    padding: 22px 20px;
    font-size: 28px;
    font-weight: 700;
    color: white;
    border-bottom: 1px solid #312e81;
}
h1 { font-size: 42px !important; font-weight: 800 !important; color: white !important; }
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
[data-testid="stMetricLabel"]  { color: #d8b4fe !important; font-size: 15px !important; }
[data-testid="stMetricValue"]  { color: white !important; font-size: 32px !important; font-weight: 700 !important; }
div[data-testid="stPlotlyChart"] {
    background: rgba(17,24,39,0.75);
    border: 1px solid rgba(139,92,246,0.2);
    border-radius: 18px;
    padding: 12px;
    margin-top: 10px;
    box-shadow: 0 8px 25px rgba(0,0,0,0.25);
}
.stButton > button {
    background: linear-gradient(135deg, #7c3aed, #8b5cf6);
    color: white; border: none; border-radius: 12px;
    padding: 10px 20px; font-weight: 600;
}
.stTextInput input {
    background-color: #111827 !important; color: white !important;
    border: 1px solid #7c3aed !important; border-radius: 10px !important;
}
[data-baseweb="select"] { background-color: #111827 !important; }
[data-testid="stMultiSelect"] span[data-baseweb="tag"] {
    background-color: #7c3aed !important; color: white !important;
}
hr { border-color: rgba(255,255,255,0.08); }
[data-testid="stDataFrame"] { border-radius: 16px; overflow: hidden; }

/* Dynamic insight boxes */
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
</style>
""", unsafe_allow_html=True)

# ======================================================
# LOAD DATA
# ======================================================

st.write("")

@st.cache_data
def load_data():
    trips    = pd.read_excel("data/Fact_Trips_Cleaned.xlsx")
    routes   = pd.read_excel("data/Dim_Routes_Cleaned.xlsx")
    external = pd.read_excel("data/Fact_External_Cleaned.xlsx")
    calendar = pd.read_excel("data/Dim_Time_Cleaned.xlsx")
    return trips, routes, external, calendar

trips, routes, external, calendar = load_data()

df = trips.merge(routes, on="RouteID", how="left") if "RouteID" in routes.columns else trips.copy()

# Clean key columns
for col in ["VehicleType", "Status", "WeatherCondition", "CongestionLevel"]:
    if col in df.columns:
        df[col] = df[col].astype(str).str.strip()

df["Delay_Minutes"] = pd.to_numeric(df["Delay_Minutes"], errors="coerce")
df["Hour"] = pd.to_datetime(df["Time"], errors="coerce").dt.hour

# ======================================================
# SIDEBAR FILTERS
# ======================================================

st.sidebar.subheader("🎛️ Filters")

route_options = ["ALL"] + sorted(df["RouteID"].dropna().unique().tolist())
route_filter  = st.sidebar.selectbox("Select Route", route_options)
vehicle_filter = st.sidebar.multiselect(
    "Vehicle Type",
    sorted(df["VehicleType"].dropna().unique()),
    default=sorted(df["VehicleType"].dropna().unique())
)
status_filter = st.sidebar.multiselect(
    "Trip Status",
    sorted(df["Status"].dropna().unique()),
    default=sorted(df["Status"].dropna().unique())
)
weather_filter = st.sidebar.multiselect(
    "Weather Condition",
    sorted(df["WeatherCondition"].dropna().unique()),
    default=sorted(df["WeatherCondition"].dropna().unique())
)

# ======================================================
# FILTER DATA
# ======================================================

route_mask = df["RouteID"].isin(df["RouteID"].unique()) if route_filter == "ALL" else (df["RouteID"] == route_filter)

filtered_df = df[
    route_mask &
    (df["VehicleType"].isin(vehicle_filter)) &
    (df["Status"].isin(status_filter)) &
    (df["WeatherCondition"].isin(weather_filter))
].copy()

if filtered_df.empty:
    st.warning("No data available for selected filters.")
    st.stop()

# ======================================================
# TITLE
# ======================================================

st.title("📌 Insights")
st.write(
    "Overall analytical observations and operational findings "
    "generated from public transport datasets."
)
st.divider()

# ======================================================
# OVERVIEW METRICS  (whole dataset, not filtered)
# ======================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric("Total Trips", len(trips))
with m2:
    st.metric("Total Routes", routes["RouteID"].nunique())
with m3:
    st.metric("Average Delay", f"{trips['Delay_Minutes'].mean():.2f} mins")
with m4:
    ontime = ((trips["Status"] == "On-Time").sum() / len(trips)) * 100
    st.metric("On-Time Performance", f"{ontime:.1f}%")

st.divider()

# ======================================================
# DYNAMIC INSIGHT COMPUTATIONS
# ======================================================

fdf = filtered_df   # shorthand

# --- Transport Operations ---
avg_delay     = fdf["Delay_Minutes"].mean()
max_delay     = fdf["Delay_Minutes"].max()
trip_count    = len(fdf)
otp           = ((fdf["Status"] == "On-Time").sum() / trip_count) * 100

if "CongestionLevel" in fdf.columns:
    top_cong = fdf.groupby("CongestionLevel")["Delay_Minutes"].mean().idxmax()
    top_cong_delay = fdf.groupby("CongestionLevel")["Delay_Minutes"].mean().max()
else:
    top_cong = "N/A"; top_cong_delay = 0

route_label = "All Routes" if route_filter == "ALL" else f"Route {route_filter}"

ops_pt1 = (
    f"<b>{route_label}</b> recorded <b>{trip_count}</b> trips with an average delay of "
    f"<b>{avg_delay:.1f} mins</b> and an on-time performance of <b>{otp:.1f}%</b>."
)
ops_pt2 = (
    f"The highest single-trip delay on this route reached <b>{max_delay:.1f} mins</b>, "
    f"indicating occasional but significant disruptions."
)
ops_pt3 = (
    f"<b>{top_cong.lower()} congestion</b> is the leading operational pressure point, "
    f"contributing an average of <b>{top_cong_delay:.1f} mins</b> delay per affected trip."
)

# --- Delay Severity ---
bins   = [0, 5, 10, 20, 30, 50, float("inf")]
labels = ["<5", "5–10", "10–20", "20–30", "30–50", "50+"]
fdf["DelayBucket"] = pd.cut(fdf["Delay_Minutes"], bins=bins, labels=labels)
bucket_counts = fdf["DelayBucket"].value_counts().sort_index()
top_bucket    = bucket_counts.idxmax()
top_bucket_n  = bucket_counts.max()

extreme_n     = bucket_counts.get("50+", 0)
low_n         = bucket_counts.get("<5", 0)

sev_pt1 = (
    f"The most frequent delay range on <b>{route_label}</b> is "
    f"<b>{top_bucket} minutes</b>, accounting for <b>{top_bucket_n}</b> trips."
)
sev_pt2 = (
    f"Only <b>{extreme_n}</b> trips exceeded 50 minutes of delay, "
    f"while <b>{low_n}</b> trips stayed under 5 minutes — "
    f"showing that extreme delays are rare but short delays are uncommon too."
)
sev_pt3 = (
    f"Medium-range delays (10–30 mins) dominate this route, suggesting "
    f"<b>consistent moderate congestion</b> rather than isolated severe incidents."
)

# --- Time-Based ---
if "Hour" in fdf.columns:
    hourly      = fdf.groupby("Hour")["Delay_Minutes"].mean()
    peak_hour   = int(hourly.idxmax())
    peak_delay  = hourly.max()
    stable_hour = int(hourly.idxmin())
    stable_delay= hourly.min()
else:
    peak_hour = 8; peak_delay = avg_delay; stable_hour = 14; stable_delay = avg_delay * 0.5

time_pt1 = (
    f"Delays on <b>{route_label}</b> peak at <b>{peak_hour}:00</b> "
    f"with an average of <b>{peak_delay:.1f} mins</b>, "
    f"aligning with typical commuter rush hours."
)
time_pt2 = (
    f"The most stable operating window is around <b>{stable_hour}:00</b>, "
    f"where average delay drops to <b>{stable_delay:.1f} mins</b>."
)
time_pt3 = (
    f"Scheduling additional vehicles or dynamic rerouting between "
    f"<b>{peak_hour-1}:00–{peak_hour+1}:00</b> could yield the most improvement in punctuality."
)

# --- Vehicle Performance ---
if "VehicleType" in fdf.columns:
    veh_delay   = fdf.groupby("VehicleType")["Delay_Minutes"].mean()
    worst_veh   = veh_delay.idxmax()
    best_veh    = veh_delay.idxmin()
    worst_delay = veh_delay.max()
    best_delay  = veh_delay.min()
    veh_counts  = fdf["VehicleType"].value_counts()
    dominant_veh= veh_counts.idxmax()
    dominant_n  = veh_counts.max()
else:
    worst_veh = best_veh = dominant_veh = "N/A"
    worst_delay = best_delay = dominant_n = 0

veh_pt1 = (
    f"<b>{dominant_veh}</b> handles the most trips on <b>{route_label}</b> "
    f"(<b>{dominant_n}</b> trips), making it the primary vehicle type for this corridor."
)
veh_pt2 = (
    f"<b>{worst_veh}</b> shows the highest average delay of <b>{worst_delay:.1f} mins</b>, "
    f"while <b>{best_veh}</b> performs best at <b>{best_delay:.1f} mins</b> average."
)
veh_pt3 = (
    f"The delay gap between vehicle types on this route suggests that "
    f"<b>{best_veh}</b> operations should be prioritised during peak congestion windows."
)

# --- Weather & Traffic ---
if "WeatherCondition" in fdf.columns:
    weath_delay  = fdf.groupby("WeatherCondition")["Delay_Minutes"].mean()
    worst_weath  = weath_delay.idxmax()
    worst_wdelay = weath_delay.max()
    best_weath   = weath_delay.idxmin()
    best_wdelay  = weath_delay.min()
else:
    worst_weath = best_weath = "N/A"; worst_wdelay = best_wdelay = 0

wthr_pt1 = (
    f"<b>{worst_weath}</b> weather causes the highest delays on <b>{route_label}</b>, "
    f"averaging <b>{worst_wdelay:.1f} mins</b> per trip."
)
wthr_pt2 = (
    f"<b>{best_weath}</b> conditions result in the smoothest operations "
    f"at just <b>{best_wdelay:.1f} mins</b> average delay."
)
wthr_pt3 = (
    f"The <b>{worst_wdelay - best_wdelay:.1f} min gap</b> between worst and best weather "
    f"confirms that environmental conditions are a major controllable risk factor for this route."
)

# --- Route Performance ---
all_routes_avg = df.groupby("RouteID")["Delay_Minutes"].mean()
network_avg    = all_routes_avg.mean()

if route_filter == "ALL":
    route_rank  = "N/A"
    route_avg   = fdf["Delay_Minutes"].mean()
    diff        = route_avg - network_avg
    diff_label  = f"{abs(diff):.1f} mins {'above' if diff > 0 else 'below'}"
    rte_pt1 = (
        f"Showing data across <b>all {len(all_routes_avg)} routes</b> with an overall "
        f"average delay of <b>{route_avg:.1f} mins</b> vs the network average of "
        f"<b>{network_avg:.1f} mins</b>."
    )
else:
    route_rank  = int(all_routes_avg.rank(ascending=False)[route_filter])
    total_routes= len(all_routes_avg)
    route_avg   = all_routes_avg[route_filter]
    diff        = route_avg - network_avg
    diff_label  = f"{abs(diff):.1f} mins {'above' if diff > 0 else 'below'}"
    rte_pt1 = (
        f"Route <b>{route_filter}</b> ranks <b>#{route_rank}</b> out of "
        f"<b>{total_routes}</b> routes by average delay, with <b>{route_avg:.1f} mins</b> "
        f"vs the network average of <b>{network_avg:.1f} mins</b>."
    )
cancel_rate = ((fdf["Status"] == "Cancelled").sum() / trip_count) * 100

rte_pt2 = (
    f"The selected {'network' if route_filter == 'ALL' else 'route'}'s delay is "
    f"<b>{diff_label}</b> the network average, "
    f"{'indicating below-average performance that needs attention.' if diff > 0 else 'indicating above-average reliability.'}"
)
rte_pt3 = (
    f"The cancellation rate is <b>{cancel_rate:.1f}%</b>, "
    f"{'which is a significant operational concern.' if cancel_rate > 5 else 'which remains within acceptable limits.'}"
)

# ======================================================
# HELPER
# ======================================================

def dyn_box(title, pts):
    items = "".join(f"<li>{p}</li>" for p in pts)
    st.markdown(
        f'<div class="dyn-box"><h4>{title}</h4><ul>{items}</ul></div>',
        unsafe_allow_html=True
    )

# ======================================================
# KEY INSIGHTS SECTION
# ======================================================

header_label = "All Routes" if route_filter == "ALL" else f"Route {route_filter}"
st.header(f"📊 Key Insights — {header_label}")

left_col, right_col = st.columns(2)

with left_col:
    with st.container(border=True):
        dyn_box("🚍 Transport Operations",   [ops_pt1,  ops_pt2,  ops_pt3])
        dyn_box("🚦 Delay Severity",         [sev_pt1,  sev_pt2,  sev_pt3])
        dyn_box("⏰ Time-Based Observations", [time_pt1, time_pt2, time_pt3])

with right_col:
    with st.container(border=True):
        dyn_box("🚆 Vehicle Performance",        [veh_pt1,  veh_pt2,  veh_pt3])
        dyn_box("🌦️ Weather and Traffic Impact", [wthr_pt1, wthr_pt2, wthr_pt3])
        dyn_box("🛣️ Route Performance",          [rte_pt1,  rte_pt2,  rte_pt3])

st.divider()

# ======================================================
# FOOTER
# ======================================================

st.caption("Public Transport Analytics Dashboard • Operational Insights Module")
