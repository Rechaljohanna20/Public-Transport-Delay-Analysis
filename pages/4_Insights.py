# import streamlit as st
# import pandas as pd

# # ======================================================
# # PAGE CONFIG
# # ======================================================

# st.set_page_config(
#     page_title="Insights",
#     layout="wide"
# )

# # ======================================================
# # LOAD DATA
# # ======================================================

# trips = pd.read_excel("data/Fact_Trips_Cleaned.xlsx")
# routes = pd.read_excel("data/Dim_Routes_Cleaned.xlsx")
# external = pd.read_excel("data/Fact_External_Cleaned.xlsx")
# calendar = pd.read_excel("data/Dim_Time_Cleaned.xlsx")
# time_df = pd.read_excel("data/Dim_Time_Cleaned.xlsx")

# # ======================================================
# # TITLE
# # ======================================================

# st.title("📌 Insights")

# st.write(
#     "Overall analytical observations and operational findings "
#     "generated from public transport datasets."
# )

# st.divider()

# # ======================================================
# # OVERVIEW METRICS
# # ======================================================

# m1, m2, m3, m4 = st.columns(4)

# with m1:
#     st.metric(
#         "Total Trips",
#         len(trips)
#     )

# with m2:
#     st.metric(
#         "Total Routes",
#         routes["RouteID"].nunique()
#     )

# with m3:
#     st.metric(
#         "Average Delay",
#         f"{trips['Delay_Minutes'].mean():.2f} mins"
#     )

# with m4:

#     ontime = (
#         (trips["Status"] == "On-Time").sum()
#         / len(trips)
#     ) * 100

#     st.metric(
#         "On-Time Performance",
#         f"{ontime:.1f}%"
#     )

# st.divider()

# # ======================================================
# # KEY INSIGHTS
# # ======================================================

# st.header("Key Insights")

# left_col, right_col = st.columns(2)

# # ======================================================
# # LEFT SIDE
# # ======================================================

# with left_col:

#     st.markdown("""

# ### 🚍 Transport Operations
# - Most transport delays occur during heavy traffic periods.
# - Some routes consistently perform better with lower delay times.
# - High passenger movement increases operational pressure on vehicles.
# - Certain trips experience repeated delays due to route congestion.
# - Vehicle movement becomes less efficient during busy city hours.

# ### 🚦 Delay Severity
# - Largest number of trips experienced delays between 10–20 minutes.
# - More than 4,000 trips recorded delays between 20–30 minutes.
# - Only a small number of trips crossed the 50-minute delay mark.
# - Very few trips maintained delays below 5 minutes.
# - Medium-level delays were more common than extreme delays.

# ### ⏰ Time-Based Observations
# - Morning office hours show noticeable delay increases.
# - Evening return traffic creates longer travel durations.
# - Midday operations remain comparatively stable and smoother.
# - Delay frequency changes significantly across different hours.
# - Peak-hour analysis helps identify overloaded transport periods.

# """)

# # ======================================================
# # RIGHT SIDE
# # ======================================================

# with right_col:

#     st.markdown("""

# ### 🚆 Vehicle Performance Comparison
# - Buses handled the majority of transport operations across the network.
# - Bus services showed higher average delay duration compared to trains.
# - Train operations maintained better timing consistency and reliability.
# - Most cancellation cases were observed in bus transportation.
# - Train services performed more efficiently during congested conditions.

# ### 🌦️ Weather and Traffic Impact
# - Rainy weather conditions increase average delay time.
# - Clear weather supports smoother transport movement.
# - Heavy congestion combined with poor weather creates major delays.
# - External environmental conditions directly affect trip efficiency.
# - Traffic density plays a major role in route performance.

# ### 🛣️ Route Performance
# - Long-distance routes generally show higher delay accumulation.
# - Some routes maintain stable operational timing consistently.
# - Congested corridors reduce overall transport efficiency.
# - Route-level analysis helps identify traffic bottlenecks.
# - Delay variation differs from one route to another.

# """)
import streamlit as st
import pandas as pd

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Insights",
    layout="wide"
)

# ======================================================
# LOAD DATA
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

    border: 1px solid rgba(139,92,246,0.35);

    backdrop-filter: blur(12px);

    padding: 20px;

    border-radius: 18px;

    box-shadow:
        0 8px 30px rgba(0,0,0,0.25);

    transition: all 0.3s ease;
}

[data-testid="stMetric"]:hover {
    transform: translateY(-4px);
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

/* ===== CHARTS ===== */
div[data-testid="stPlotlyChart"] {
    background: rgba(17,24,39,0.75);

    border: 1px solid rgba(139,92,246,0.2);

    border-radius: 18px;

    padding: 12px;

    margin-top: 10px;

    box-shadow:
        0 8px 25px rgba(0,0,0,0.25);
}

/* ===== BUTTONS ===== */
.stButton > button {
    background: linear-gradient(
        135deg,
        #7c3aed,
        #8b5cf6
    );

    color: white;

    border: none;

    border-radius: 12px;

    padding: 10px 20px;

    font-weight: 600;
}

/* ===== INPUT BOX ===== */
.stTextInput input {
    background-color: #111827 !important;
    color: white !important;

    border: 1px solid #7c3aed !important;

    border-radius: 10px !important;
}

/* ===== MULTISELECT ===== */
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

/* ===== DATAFRAME ===== */
[data-testid="stDataFrame"] {
    border-radius: 16px;
    overflow: hidden;
}

</style>
""", unsafe_allow_html=True)

st.write("")
trips = pd.read_excel("data/Fact_Trips_Cleaned.xlsx")
routes = pd.read_excel("data/Dim_Routes_Cleaned.xlsx")
external = pd.read_excel("data/Fact_External_Cleaned.xlsx")
calendar = pd.read_excel("data/Dim_Time_Cleaned.xlsx")
time_df = pd.read_excel("data/Dim_Time_Cleaned.xlsx")

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
# OVERVIEW METRICS
# ======================================================

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "Total Trips",
        len(trips)
    )

with m2:
    st.metric(
        "Total Routes",
        routes["RouteID"].nunique()
    )

with m3:
    st.metric(
        "Average Delay",
        f"{trips['Delay_Minutes'].mean():.2f} mins"
    )

with m4:

    ontime = (
        (trips["Status"] == "On-Time").sum()
        / len(trips)
    ) * 100

    st.metric(
        "On-Time Performance",
        f"{ontime:.1f}%"
    )

st.divider()

# ======================================================
# KEY INSIGHTS
# ======================================================

st.header("📊 Key Insights")

left_col, right_col = st.columns(2)

# ======================================================
# LEFT SIDE
# ======================================================

with left_col:

    with st.container(border=True):

        st.markdown("""

### 🚍 Transport Operations
- Most transport delays occur during heavy traffic periods.
- Some routes consistently perform better with lower delay times.
- High passenger movement increases operational pressure on vehicles.
- Certain trips experience repeated delays due to route congestion.
- Vehicle movement becomes less efficient during busy city hours.

---

### 🚦 Delay Severity
- Largest number of trips experienced delays between 10–20 minutes.
- More than 4,000 trips recorded delays between 20–30 minutes.
- Only a small number of trips crossed the 50-minute delay mark.
- Very few trips maintained delays below 5 minutes.
- Medium-level delays were more common than extreme delays.

---

### ⏰ Time-Based Observations
- Morning office hours show noticeable delay increases.
- Evening return traffic creates longer travel durations.
- Midday operations remain comparatively stable and smoother.
- Delay frequency changes significantly across different hours.
- Peak-hour analysis helps identify overloaded transport periods.

""")

# ======================================================
# RIGHT SIDE
# ======================================================

with right_col:

    with st.container(border=True):

        st.markdown("""

### 🚆 Vehicle Performance Comparison
- Buses handled the majority of transport operations across the network.
- Bus services showed higher average delay duration compared to trains.
- Train operations maintained better timing consistency and reliability.
- Most cancellation cases were observed in bus transportation.
- Train services performed more efficiently during congested conditions.

---

### 🌦️ Weather and Traffic Impact
- Rainy weather conditions increase average delay time.
- Clear weather supports smoother transport movement.
- Heavy congestion combined with poor weather creates major delays.
- External environmental conditions directly affect trip efficiency.
- Traffic density plays a major role in route performance.

---

### 🛣️ Route Performance
- Long-distance routes generally show higher delay accumulation.
- Some routes maintain stable operational timing consistently.
- Congested corridors reduce overall transport efficiency.
- Route-level analysis helps identify traffic bottlenecks.
- Delay variation differs from one route to another.

""")

st.divider()

# ======================================================
# FOOTER
# ======================================================

st.caption(
    "Public Transport Analytics Dashboard • Operational Insights Module"
)