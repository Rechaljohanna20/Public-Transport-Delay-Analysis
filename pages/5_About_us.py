mport streamlit as st

st.set_page_config(
    page_title="Public Transport Delay Analysis",
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
    font-size: 52px !important;
    font-weight: 800 !important;
    color: white !important;
    text-align: center;
    margin-top: 70px;
}

h3 {
    color: #c4b5fd !important;
    text-align: center;
    margin-top: 10px;
}

/* ===== TEXT ===== */
.center-text {
    text-align: center;
    font-size: 18px;
    color: #d1d5db;
    max-width: 950px;
    margin: auto;
    line-height: 1.8;
    padding-top: 25px;
}

/* ===== FEATURE SECTION ===== */
.feature-box {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(139,92,246,0.25);
    border-radius: 24px;
    padding: 50px;
    margin-top: 60px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.25);
}

/* ===== HIGHLIGHTS ===== */
.highlight {
    text-align: center;
    font-size: 17px;
    color: #e5e7eb;
    padding-top: 15px;
}

</style>
""", unsafe_allow_html=True)

# ======================================================
# LANDING PAGE CONTENT
# ======================================================

st.markdown("""
<div class="feature-box">

<h1>Public Transport Delay Analysis</h1>

<h3>
Interactive Analytics for Monitoring Transport Delays and Operational Trends
</h3>

<p class="center-text">
Welcome to the Public Transport Delay Analysis.  
This application helps users analyze delay behavior across public transportation systems using operational and historical transport data.
</p>

<p class="center-text">
Explore route performance, traffic congestion patterns, peak-hour disruptions, and time-based delay trends through interactive visualizations and analytics modules.
</p>

<p class="highlight">
📊 Delay Insights &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;
🚦 Congestion Analysis &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;
🚌 Route Performance Monitoring
</p>

</div>
""", unsafe_allow_html=True)

st.write("")
st.write("")
st.caption("Public Transport Delay Analytics ")
