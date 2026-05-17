import streamlit as st

st.set_page_config(page_title="Home page ",layout="wide")

st.write(" ")
st.markdown("""
<style>

/* Sidebar App Title */
section[data-testid="stSidebar"]::before {
    content: "🚍 Route Analytics";
    display: block;
    margin-top: 70px;   /* move title downward */
    padding: 0px 20px 15px 20px;
    font-size: 26px;
    font-weight: bold;
    color: white;
    border-bottom: 1px solid #374151;  /* divider line */
}

/* Sidebar Background */
section[data-testid="stSidebar"] {
    background-color: #111827;
}

</style>
""", unsafe_allow_html=True)

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
