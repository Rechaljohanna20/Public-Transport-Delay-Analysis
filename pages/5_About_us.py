import streamlit as st

st.set_page_config(page_title="About us",layout="wide")
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
# st.title("About us page")


st.header("Summary")
st.write("""

The Public Transport Delay Analysis System is a data analytics project developed using Streamlit to analyze and 
visualize delays in public transportation systems such as buses and trains. The system uses transport-related data 
including routes, travel timings, traffic conditions, and congestion patterns to identify delay trends and route 
performance.The project provides dashboards and visual insights that help monitor transport efficiency, detect 
peak congestion hours, and support better travel planning. By transforming raw transport data into meaningful 
analytics, the system helps improve operational efficiency and enables smarter decision-making in public 
transportation management.""")

st.divider()

st.markdown("""
- AnalyseTransport delays
- Identify peak congestion hours
- Improve route efficiency
- Supoort better travel planning""")


st.divider()

st.header("Technologies and Tools used")
st.markdown("""
-Python
-PowerBI
""")

st.divider()
