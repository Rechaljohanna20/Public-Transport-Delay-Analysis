import streamlit as st

st.set_page_config(page_title="Home page ",layout="wide")

st.write(" ")
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

st.write(" ")

# st.sidebar.divider()
st.header("Project Overview")
st.write("""The **Public Transport Delay Analysis System** is designed to monitor,
analyze, and visualize delays in public transportation networks.

Using transport schedules, traffic conditions, travel timings,
and operational data, the system provides data-driven insights
to identify delay patterns, congestion trends, and route performance.

Dashboards and analytical tools help improve transport
efficiency, support smarter travel planning, and enhance overall
commuter experience.""")

st.header("Objectives")
st.markdown("""
- Analyze public transport delays
- Identify peak congestion hours
- Compare route performances
- Improve transport efficiency
- Support better travel planning
""")
st.divider()


st.header("Key Features")

col1, col2 = st.columns(2)

with col1:
    # st.info("Interactive Dashboard")
    st.info("Route-wise Delay Analysis")
    st.info("Peak Traffic Insights")


with col2:
    st.info("Delay Trend Visualization")
    st.info(" Delay Predictions")

st.write("")
st.write("")

d1, c2, c3, c4 = st.columns(4, gap="large")

with d1:
    st.metric("Active Routes", "128", "+12")

with c2:
    st.metric("Running Vehicles", "542", "+24")

with c3:
    st.metric("Average Delay", "7 mins", "-2 mins")

with c4:
    st.metric("On-Time Performance", "89%", "+5%")
