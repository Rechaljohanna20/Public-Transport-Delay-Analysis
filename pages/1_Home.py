import streamlit as st

st.set_page_config(
    page_title="Dashboard Home",
    layout="wide"
)

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

/* ===== INFO BOX ===== */
div[data-testid="stAlert"] {
    border-radius: 14px;
    border: 1px solid rgba(139,92,246,0.25);
    background: rgba(255,255,255,0.04);
}

/* ===== METRIC CARDS ===== */
[data-testid="stMetric"] {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(139,92,246,0.35);
    backdrop-filter: blur(12px);
    padding: 20px;
    border-radius: 18px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
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

/* ===== DIVIDER ===== */
hr {
    border-color: rgba(255,255,255,0.08);
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# HEADER
# ======================================================

st.title("Transport Operations Center")

st.write("""
Monitor transport operations, track delay behavior, and view key performance indicators across the public transportation network.
""")

st.divider()

# ======================================================
# SYSTEM OVERVIEW
# ======================================================

st.header("System Overview")

col1, col2 = st.columns(2)

with col1:
    st.info("📊 Route Performance Status")
    st.info("🚦 Traffic Congestion Overview")
    st.info("⏱ Peak-Hour Activity")

with col2:
    st.info("📈 Delay Monitoring")
    st.info("🌦 Weather Condition Impact")
    st.info("🚌 Operational Performance")

st.divider()

# ======================================================
# QUICK METRICS
# ======================================================

st.header("Quick Metrics")

d1, d2, d3, d4 = st.columns(4, gap="large")

with d1:
    st.metric("Total Records", "20K+")

with d2:
    st.metric("Analyzed Trips", "15K+")

with d3:
    st.metric("Avg Delay Time", "7 mins")

with d4:
    st.metric("On Time Performance", "89%")

st.divider()

# ======================================================
# STATUS SECTION
# ======================================================

st.header("Network Status")

st.write("""
The transport monitoring system is actively tracking operational trends, delay variations, and congestion behavior across available transport routes.
""")

st.caption("Public Transport Analytics Dashboard")
