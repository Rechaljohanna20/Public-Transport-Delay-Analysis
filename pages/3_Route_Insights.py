import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from groq import Groq

st.set_page_config(page_title="Route Insights", layout="wide")

client = Groq(
             api_key=st.secrets["API_KEY"]
)
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #111827 50%, #1e1b4b 100%);
    color: white;
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
h1 { color: white !important; font-size: 42px !important; font-weight: 800 !important; }
h2, h3 { color: #c4b5fd !important; }
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(139,92,246,0.3);
    border-radius: 18px;
    padding: 20px;
}
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
</style>
""", unsafe_allow_html=True)

# ── Load & merge ──────────────────────────────────────
@st.cache_data
def load_data():
    trips  = pd.read_excel("data/Fact_Trips_Cleaned.xlsx")
    routes = pd.read_excel("data/Dim_Routes_Cleaned.xlsx")
    return trips, routes

trips, routes = load_data()
df = trips.merge(routes, on="RouteID", how="left") if "RouteID" in routes.columns else trips.copy()

# ── Clean ─────────────────────────────────────────────
df["Delay_Minutes"] = pd.to_numeric(df["Delay_Minutes"], errors="coerce")
df["Date"]  = pd.to_datetime(df["Date"], errors="coerce")
df["Hour"]  = pd.to_datetime(df["Time"], errors="coerce").dt.hour
df["Month"] = df["Date"].dt.month

def get_season(m):
    if m in [3,4,5]:     return "Summer"
    elif m in [6,7,8,9]: return "Monsoon"
    elif m in [10,11]:   return "Post-Monsoon"
    else:                return "Winter"

def get_time_period(h):
    if pd.isna(h):      return "Unknown"
    elif 6  <= h < 10:  return "Morning Rush"
    elif 10 <= h < 16:  return "Afternoon"
    elif 16 <= h < 21:  return "Evening Rush"
    else:               return "Night"

df["Season"]     = df["Month"].apply(get_season)
df["TimePeriod"] = df["Hour"].apply(get_time_period)

for col in ["VehicleType","Status","WeatherCondition","CongestionLevel"]:
    df[col] = df[col].astype(str).str.strip()

# ── Sidebar filters ───────────────────────────────────
st.sidebar.subheader("🎛️ Filters")

all_routes     = sorted(df["RouteID"].dropna().unique())
route_options  = ["All"] + list(all_routes)
route_filter   = st.sidebar.selectbox("Select Route", route_options)

vehicle_filter = st.sidebar.multiselect("Vehicle Type",      sorted(df["VehicleType"].dropna().unique()),      default=sorted(df["VehicleType"].dropna().unique()))
status_filter  = st.sidebar.multiselect("Trip Status",       sorted(df["Status"].dropna().unique()),           default=sorted(df["Status"].dropna().unique()))
weather_filter = st.sidebar.multiselect("Weather Condition", sorted(df["WeatherCondition"].dropna().unique()), default=sorted(df["WeatherCondition"].dropna().unique()))

# ── Filter data ───────────────────────────────────────
if route_filter == "All":
    filtered_df = df[
        (df["VehicleType"].isin(vehicle_filter)) &
        (df["Status"].isin(status_filter)) &
        (df["WeatherCondition"].isin(weather_filter))
    ]
else:
    filtered_df = df[
        (df["RouteID"] == route_filter) &
        (df["VehicleType"].isin(vehicle_filter)) &
        (df["Status"].isin(status_filter)) &
        (df["WeatherCondition"].isin(weather_filter))
    ]

if filtered_df.empty:
    st.warning("No data available.")
    st.stop()

# ── Title ─────────────────────────────────────────────
st.title("🛣️ Route Insights Dashboard")
st.markdown("Understand WHY delays happen, WHEN operational instability occurs, and WHICH conditions create disruption.")
st.divider()

# ── Route info ────────────────────────────────────────
st.subheader("📍 Route Information")

if route_filter == "All":
    i1, i2, i3, i4 = st.columns(4)
    i1.info(f"**Routes**\n\n{len(all_routes)} Routes")
    i2.info(f"**Total Trips**\n\n{len(filtered_df)}")
    i3.info(f"**Avg Distance**\n\nAll Routes")
    i4.info(f"**Vehicle Types**\n\n{', '.join(vehicle_filter)}")
else:
    ri = filtered_df.iloc[0]
    i1, i2, i3, i4 = st.columns(4)
    i1.info(f"**Origin**\n\n{ri.get('Origin','N/A')}")
    i2.info(f"**Destination**\n\n{ri.get('Destination','N/A')}")
    i3.info(f"**Distance**\n\n{ri.get('DistanceKM','N/A')} KM")
    i4.info(f"**Vehicle Types**\n\n{', '.join(vehicle_filter)}")

st.divider()

# ── KPIs ──────────────────────────────────────────────
avg_delay       = filtered_df["Delay_Minutes"].mean()
max_delay       = filtered_df["Delay_Minutes"].max()
trip_count      = len(filtered_df)
on_time_percent = ((filtered_df["Status"]=="On-Time").sum() / len(filtered_df)) * 100

k1, k2, k3, k4 = st.columns(4)
k1.metric("Average Delay", f"{avg_delay:.1f} mins")
k2.metric("Maximum Delay", f"{max_delay:.1f} mins")
k3.metric("Trips",         trip_count)
k4.metric("On-Time %",     f"{on_time_percent:.1f}%")
st.divider()

# ── Root cause banner ─────────────────────────────────
st.subheader("🚨 Root Cause Analysis")

wi = filtered_df.groupby("WeatherCondition").agg(A=("Delay_Minutes","mean"), T=("Delay_Minutes","count"))
wi["S"] = wi["A"] * wi["T"]
top_weather = wi["S"].idxmax()

ci = filtered_df.groupby("CongestionLevel").agg(A=("Delay_Minutes","mean"), T=("Delay_Minutes","count"))
ci["S"] = ci["A"] * ci["T"]
top_congestion = ci["S"].idxmax()

ti = filtered_df.groupby("TimePeriod").agg(A=("Delay_Minutes","mean"), T=("Delay_Minutes","count"))
ti["S"] = ti["A"] * ti["T"]
top_time = ti["S"].idxmax()

route_label = "All Routes" if route_filter == "All" else f"Route {route_filter}"

st.markdown(f"""
<div class="insight-box">
🌦️ Major delays are strongly associated with <b>{top_weather}</b> weather conditions.<br><br>
🚦 Route instability becomes severe during <b>{top_congestion.lower()}</b> congestion periods.<br><br>
⏰ Most operational disruptions occur during <b>{top_time}</b>.
</div>
""", unsafe_allow_html=True)
st.divider()

# ── Helper ────────────────────────────────────────────
def summary_box(points):
    items = "".join(f"<li>{p}</li>" for p in points)
    st.markdown(f'<div class="chart-summary"><ul>{items}</ul></div>', unsafe_allow_html=True)

# ======================================================
# CHART DATA
# ======================================================

# Chart 1 — Seasonal
seas_df = (
    filtered_df.groupby(["Season","WeatherCondition"])
    .agg(AvgDelay=("Delay_Minutes","mean"), Trips=("Delay_Minutes","count"))
    .reset_index()
)
seas_df = seas_df[seas_df["Trips"] >= 15]
seas_df["ImpactScore"] = seas_df["AvgDelay"] * seas_df["Trips"]

# Chart 2 — Congestion across day
cong_df = (
    filtered_df.groupby(["TimePeriod","CongestionLevel"])
    .agg(AvgDelay=("Delay_Minutes","mean"), Trips=("Delay_Minutes","count"))
    .reset_index()
)
cong_df["ImpactScore"] = cong_df["AvgDelay"] * cong_df["Trips"]
top_cong_df = cong_df.loc[cong_df.groupby("TimePeriod")["ImpactScore"].idxmax()]
time_order  = ["Morning Rush","Afternoon","Evening Rush","Night"]
top_cong_df = top_cong_df.copy()
top_cong_df["TimePeriod"] = pd.Categorical(top_cong_df["TimePeriod"], categories=time_order, ordered=True)
top_cong_df = top_cong_df.sort_values("TimePeriod")
top_cong_df["Reason"] = (
    top_cong_df["CongestionLevel"] + " congestion caused " +
    top_cong_df["AvgDelay"].round(1).astype(str) + " mins delay"
)

# Chart 3 — Scattered Column Chart: Avg Delay by Weather Condition & Time Period
scatter_col_df = (
    filtered_df.groupby(["WeatherCondition", "TimePeriod"])["Delay_Minutes"]
    .mean().reset_index()
)
scatter_col_df.columns = ["WeatherCondition", "TimePeriod", "AvgDelay"]
time_order_cat = ["Morning Rush", "Afternoon", "Evening Rush", "Night"]
scatter_col_df["TimePeriod"] = pd.Categorical(
    scatter_col_df["TimePeriod"], categories=time_order_cat, ordered=True
)
scatter_col_df = scatter_col_df.sort_values("TimePeriod")

# Chart 4 — Hour-wise
hour_df = (
    filtered_df.groupby(["Hour","CongestionLevel"])["Delay_Minutes"]
    .mean().reset_index()
)

# ======================================================
# DYNAMIC SUMMARIES
# ======================================================

# Chart 1 (Seasonal)
if not seas_df.empty:
    ws_row = seas_df.loc[seas_df["ImpactScore"].idxmax()]
    bs_row = seas_df.loc[seas_df["ImpactScore"].idxmin()]
    ss_pt1 = (
        f"<b>{ws_row['Season']}</b> is the most delay-prone season for <b>{route_label}</b>, "
        f"with <b>{ws_row['WeatherCondition']}</b> weather causing the highest impact."
    )
    ss_pt2 = (
        f"<b>{bs_row['Season']}</b> records the lowest delay impact, where "
        f"<b>{bs_row['WeatherCondition']}</b> conditions allow the smoothest operations."
    )
else:
    ss_pt1 = f"Insufficient seasonal data for <b>{route_label}</b> with current filters."
    ss_pt2 = "Adjust filters to include more trips for a complete seasonal breakdown."

# Chart 2 (Congestion)
hi_row = top_cong_df.loc[top_cong_df["ImpactScore"].idxmax()]
lo_row = top_cong_df.loc[top_cong_df["ImpactScore"].idxmin()]
cg_pt1 = (
    f"<b>{hi_row['TimePeriod']}</b> has the highest congestion impact for <b>{route_label}</b>, "
    f"driven by <b>{hi_row['CongestionLevel'].lower()}</b> congestion "
    f"({hi_row['AvgDelay']:.1f} mins avg delay)."
)
cg_pt2 = (
    f"<b>{lo_row['TimePeriod']}</b> is the least affected period, with "
    f"<b>{lo_row['CongestionLevel'].lower()}</b> congestion "
    f"({lo_row['AvgDelay']:.1f} mins avg delay)."
)

# Chart 3 (Scattered Column)
if not scatter_col_df.empty:
    worst_sc = scatter_col_df.loc[scatter_col_df["AvgDelay"].idxmax()]
    best_sc  = scatter_col_df.loc[scatter_col_df["AvgDelay"].idxmin()]
    sc_pt1 = (
        f"For <b>{route_label}</b>, the highest avg delay is during "
        f"<b>{worst_sc['WeatherCondition']}</b> weather at <b>{worst_sc['TimePeriod']}</b> "
        f"({worst_sc['AvgDelay']:.1f} mins)."
    )
    sc_pt2 = (
        f"The lowest delay occurs under <b>{best_sc['WeatherCondition']}</b> weather during "
        f"<b>{best_sc['TimePeriod']}</b> ({best_sc['AvgDelay']:.1f} mins) — "
        f"the most reliable operating window."
    )
else:
    sc_pt1 = "Insufficient data for analysis with current filters."
    sc_pt2 = "Adjust filters to see delay trends across weather and time periods."

# Chart 4 (Hour-wise)
pk_row = hour_df.loc[hour_df["Delay_Minutes"].idxmax()]
lw_row = hour_df.loc[hour_df["Delay_Minutes"].idxmin()]
hr_pt1 = (
    f"<b>{route_label}</b> peaks at <b>{int(pk_row['Hour'])}:00</b> under "
    f"<b>{pk_row['CongestionLevel'].lower()}</b> congestion "
    f"({pk_row['Delay_Minutes']:.1f} mins avg delay)."
)
hr_pt2 = (
    f"The most stable hour is <b>{int(lw_row['Hour'])}:00</b> with "
    f"<b>{lw_row['CongestionLevel'].lower()}</b> congestion "
    f"({lw_row['Delay_Minutes']:.1f} mins avg) — best window for extra trips."
)

# ======================================================
# BUILD FIGURES
# ======================================================

fig_season = px.bar(
    seas_df, x="Season", y="ImpactScore",
    color="WeatherCondition", barmode="group",
    title=f"🌦️ Seasonal Operational Delay Causes — {route_label}"
)

fig_congestion = px.bar(
    top_cong_df, x="TimePeriod", y="ImpactScore",
    color="CongestionLevel", text="Reason",
    title=f"🚦 Main Congestion Cause Across Day — {route_label}"
)
fig_congestion.update_traces(textposition="outside")

# ── Scattered Column Chart (replaces heatmap) ─────────
# Grouped bars (columns) per Time Period, colored by Weather Condition,
# with individual scatter dots overlaid to show the "scattered" effect
fig_scatter_col = px.bar(
    scatter_col_df,
    x="TimePeriod",
    y="AvgDelay",
    color="WeatherCondition",
    barmode="group",
    text=scatter_col_df["AvgDelay"].round(1).astype(str) + " m",
    title=f"🔥 Weather vs Time Period: Avg Delay Breakdown — {route_label}",
    labels={"AvgDelay": "Avg Delay (mins)", "TimePeriod": "Time Period"},
)
fig_scatter_col.update_traces(
    textposition="outside",
    marker_line_width=0,
    opacity=0.85,
)

# Overlay scatter dots on top of each bar for the "scattered column" look
for weather in scatter_col_df["WeatherCondition"].unique():
    grp = scatter_col_df[scatter_col_df["WeatherCondition"] == weather]
    fig_scatter_col.add_trace(
        go.Scatter(
            x=grp["TimePeriod"],
            y=grp["AvgDelay"],
            mode="markers",
            marker=dict(size=10, symbol="diamond", line=dict(width=1.5, color="white")),
            showlegend=False,
            name=weather,
            hovertemplate=f"<b>{weather}</b><br>%{{x}}<br>Avg Delay: %{{y:.1f}} mins<extra></extra>",
        )
    )

fig_scatter_col.update_xaxes(
    categoryorder="array",
    categoryarray=["Morning Rush", "Afternoon", "Evening Rush", "Night"]
)

fig_hour = px.line(
    hour_df, x="Hour", y="Delay_Minutes",
    color="CongestionLevel", markers=True,
    title=f"⏰ Hour-wise Operational Instability — {route_label}"
)

for fig in [fig_season, fig_congestion, fig_scatter_col, fig_hour]:
    fig.update_layout(
        height=360,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white",
        margin=dict(l=10, r=10, t=50, b=10)
    )

# ======================================================
# LAYOUT
# ======================================================

r1c1, r1c2 = st.columns(2)
with r1c1:
    st.plotly_chart(fig_season, use_container_width=True)
    summary_box([ss_pt1, ss_pt2])
with r1c2:
    st.plotly_chart(fig_congestion, use_container_width=True)
    summary_box([cg_pt1, cg_pt2])

r2c1, r2c2 = st.columns(2)
with r2c1:
    st.plotly_chart(fig_scatter_col, use_container_width=True)
    summary_box([sc_pt1, sc_pt2])
with r2c2:
    st.plotly_chart(fig_hour, use_container_width=True)
    summary_box([hr_pt1, hr_pt2])

# ======================================================
# AI OPERATIONAL ASSISTANT
# ======================================================

st.divider()
st.header("🤖 AI Operational Assistant")

user_question = st.text_area(
    "Ask anything about delays, congestion, timings, or route performance",
    placeholder=(
        "Example:\n"
        "- When is congestion highest on this route?\n"
        "- How can delays be reduced?\n"
        "- What time is better for travel?\n"
        "- Why is this route unstable during peak hours?"
    ),
    height=200
)

if st.button("Ask AI"):
    if not user_question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Analyzing operational patterns..."):

            avg_delay_ai     = round(filtered_df["Delay_Minutes"].mean(), 2)
            max_delay_ai     = round(filtered_df["Delay_Minutes"].max(), 2)
            total_trips      = len(filtered_df)
            busiest_time     = filtered_df.groupby("TimePeriod")["Delay_Minutes"].mean().idxmax()
            best_time        = filtered_df.groupby("TimePeriod")["Delay_Minutes"].mean().idxmin()
            worst_weather    = filtered_df.groupby("WeatherCondition")["Delay_Minutes"].mean().idxmax()
            worst_congestion = filtered_df.groupby("CongestionLevel")["Delay_Minutes"].mean().idxmax()
            on_time_rate     = round(((filtered_df["Status"]=="On-Time").sum()/len(filtered_df))*100, 2)

            context = f"""
            Public Transport Operational Dataset Analysis

            Scope: {route_label}

            Operational Statistics:
            - Average Delay: {avg_delay_ai} mins
            - Maximum Delay: {max_delay_ai} mins
            - Total Trips: {total_trips}
            - On-Time Percentage: {on_time_rate}%

            Operational Patterns:
            - Highest congestion period: {busiest_time}
            - Lowest delay period: {best_time}
            - Worst weather condition: {worst_weather}
            - Most severe congestion level: {worst_congestion}

            User Question:
            {user_question}

            Instructions:
            - Answer ONLY using the operational context provided
            - Give practical and analytical responses
            - Do NOT invent alternative routes or unavailable transport systems
            - Keep answers concise and professional
            - Focus on delays, congestion, timing, and operational behavior
            """

            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are an AI transport operations analyst "
                            "specialized in public transport delay analysis."
                        )
                    },
                    {"role": "user", "content": context}
                ],
                temperature=0.3,
                max_tokens=400
            )

            ai_response = response.choices[0].message.content

            st.markdown(
                f'<div class="insight-box">{ai_response}</div>',
                unsafe_allow_html=True
            )

st.markdown("---")
st.caption("🛣️ Route Insights Dashboard • AI-Powered Operational Analytics")
