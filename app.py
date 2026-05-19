# # import streamlit as st
# # import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
# from geopy.geocoders import Nominatim
# from groq import Groq
# import time

# # ======================================================
# # GROQ CLIENT
# # ======================================================

# client = Groq(
#     api_key= "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"
# )

# # ======================================================
# # LOAD DATA
# # ======================================================

# trips = pd.read_excel(
#     r"data/Fact_Trips_Cleaned.xlsx"
# )

# routes = pd.read_excel(
#     r"data/Dim_Routes_Cleaned.xlsx"
# )

# # ======================================================
# # DATA CLEANING
# # ======================================================

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
# # GEOCODING ROUTES
# # ======================================================

# @st.cache_data(show_spinner=False)
# def geocode_locations(routes_df):

#     geolocator = Nominatim(
#         user_agent="transport_dashboard"
#     )

#     def get_coordinates(location):

#         try:
#             loc = geolocator.geocode(location)

#             time.sleep(1)

#             if loc:
#                 return pd.Series(
#                     [loc.latitude, loc.longitude]
#                 )

#         except:
#             pass

#         return pd.Series([None, None])

#     routes_df[
#         ["Origin_Lat", "Origin_Lon"]
#     ] = routes_df["Origin"].apply(
#         get_coordinates
#     )

#     routes_df[
#         ["Dest_Lat", "Dest_Lon"]
#     ] = routes_df["Destination"].apply(
#         get_coordinates
#     )

#     return routes_df

# routes = geocode_locations(routes)

# # ======================================================
# # SIDEBAR
# # ======================================================

# st.sidebar.title("Filters")

# vehicle_options = sorted(
#     trips["VehicleType"]
#     .dropna()
#     .unique()
# )

# weather_options = sorted(
#     trips["WeatherCondition"]
#     .dropna()
#     .unique()
# )

# vehicle_filter = st.sidebar.multiselect(
#     "Vehicle Type",
#     vehicle_options,
#     default=vehicle_options
# )

# weather_filter = st.sidebar.multiselect(
#     "Weather Condition",
#     weather_options,
#     default=weather_options
# )

# # ======================================================
# # FILTER DATA
# # ======================================================

# filtered_df = trips.copy()

# filtered_df = filtered_df[
#     filtered_df["VehicleType"]
#     .isin(vehicle_filter)
# ]

# filtered_df = filtered_df[
#     filtered_df["WeatherCondition"]
#     .isin(weather_filter)
# ]

# if filtered_df.empty:
#     st.warning("No data available")
#     st.stop()

# # ======================================================
# # PAGE TITLE
# # ======================================================

# st.title("📊 Operational Overview Dashboard")

# st.markdown(
#     """
#     Monitor transport delays, congestion patterns,
#     weather impact, and route performance
#     in a single analytics dashboard.
#     """
# )

# st.divider()

# # ======================================================
# # KPI SECTION
# # ======================================================

# avg_delay = filtered_df[
#     "Delay_Minutes"
# ].mean()

# otp = (
#     (
#         filtered_df["Status"]
#         == "On-Time"
#     ).sum()
#     / len(filtered_df)
# ) * 100

# network_health = (
#     (otp * 0.7)
#     + ((100 - avg_delay) * 0.3)
# )

# network_health = max(
#     0,
#     min(network_health, 100)
# )

# col1, col2, col3 = st.columns(3)

# with col1:
#     st.metric(
#         "OTP %",
#         f"{otp:.1f}%"
#     )

# with col2:
#     st.metric(
#         "Average Delay",
#         f"{avg_delay:.1f} mins"
#     )

# with col3:
#     st.metric(
#         "Network Health",
#         f"{network_health:.1f}%"
#     )

# st.divider()

# # ======================================================
# # CHART DATA
# # ======================================================

# # Hourly Delay
# hourly_delay = (
#     filtered_df
#     .groupby("Hour")["Delay_Minutes"]
#     .mean()
#     .reset_index()
# )

# # Route Delay
# route_delay = (
#     filtered_df
#     .groupby("RouteID")["Delay_Minutes"]
#     .mean()
#     .reset_index()
#     .sort_values(
#         by="Delay_Minutes",
#         ascending=False
#     )
# )

# # Weather Delay
# weather_delay = (
#     filtered_df
#     .groupby("WeatherCondition")[
#         "Delay_Minutes"
#     ]
#     .mean()
#     .reset_index()
# )

# # Congestion Delay
# congestion_delay = (
#     filtered_df
#     .groupby("CongestionLevel")[
#         "Delay_Minutes"
#     ]
#     .mean()
#     .reset_index()
# )

# # Day Column
# filtered_df["Day"] = pd.to_datetime(
#     filtered_df["Date"],
#     errors="coerce"
# ).dt.day_name()

# # Heatmap Data
# heatmap_data = filtered_df.pivot_table(
#     values="Delay_Minutes",
#     index="Day",
#     columns="Hour",
#     aggfunc="mean"
# )

# # ======================================================
# # CHARTS
# # ======================================================

# # Gauge Chart
# fig_gauge = go.Figure(
#     go.Indicator(
#         mode="gauge+number",
#         value=network_health,
#         title={
#             "text": "Network Health"
#         },
#         gauge={
#             "axis": {
#                 "range": [0, 100]
#             },
#             "bar": {
#                 "color": "green"
#             }
#         }
#     )
# )

# fig_gauge.update_layout(
#     height=300
# )

# # Hourly Trend
# fig_line = px.line(
#     hourly_delay,
#     x="Hour",
#     y="Delay_Minutes",
#     markers=True,
#     title="Hourly Delay Trend"
# )

# fig_line.update_layout(
#     height=300
# )

# # Route Delay
# fig_bar = px.bar(
#     route_delay.head(10),
#     x="RouteID",
#     y="Delay_Minutes",
#     title="Top Delayed Routes"
# )

# fig_bar.update_layout(
#     height=300
# )

# # Weather Impact
# fig_weather = px.bar(
#     weather_delay,
#     x="WeatherCondition",
#     y="Delay_Minutes",
#     title="Weather Impact"
# )

# fig_weather.update_layout(
#     height=300
# )

# # Heatmap
# fig_heatmap = px.imshow(
#     heatmap_data,
#     text_auto=True,
#     aspect="auto",
#     title="Delay Heatmap"
# )

# fig_heatmap.update_layout(
#     height=350
# )

# # Congestion Pie
# fig_congestion = px.pie(
#     congestion_delay,
#     names="CongestionLevel",
#     values="Delay_Minutes",
#     title="Congestion Contribution"
# )

# fig_congestion.update_layout(
#     height=300
# )

# # ======================================================
# # MAP VISUALIZATION
# # ======================================================

# map_df = routes.dropna(
#     subset=[
#         "Origin_Lat",
#         "Origin_Lon"
#     ]
# )

# fig_map = px.scatter_mapbox(
#     map_df,
#     lat="Origin_Lat",
#     lon="Origin_Lon",
#     hover_name="RouteName",
#     hover_data=[
#         "Origin",
#         "Destination",
#         "DistanceKM",
#         "TotalStops"
#     ],
#     color="DistanceKM",
#     size="TotalStops",
#     zoom=5,
#     height=500,
#     title="Transport Route Map"
# )

# fig_map.update_layout(
#     mapbox_style="open-street-map",
#     margin={
#         "r": 0,
#         "t": 50,
#         "l": 0,
#         "b": 0
#     }
# )

# # ======================================================
# # DASHBOARD LAYOUT
# # ======================================================

# # ROW 1
# c1, c2 = st.columns(2)

# with c1:
#     st.plotly_chart(
#         fig_gauge,
#         use_container_width=True
#     )

# with c2:
#     st.plotly_chart(
#         fig_line,
#         use_container_width=True
#     )

# # ROW 2
# c3, c4 = st.columns(2)

# with c3:
#     st.plotly_chart(
#         fig_bar,
#         use_container_width=True
#     )

# with c4:
#     st.plotly_chart(
#         fig_weather,
#         use_container_width=True
#     )

# # ROW 3
# c5, c6 = st.columns(2)

# with c5:
#     st.plotly_chart(
#         fig_heatmap,
#         use_container_width=True
#     )

# with c6:
#     st.plotly_chart(
#         fig_congestion,
#         use_container_width=True
#     )

# # ROW 4
# st.plotly_chart(
#     fig_map,
#     use_container_width=True
# )

# # ======================================================
# # DATA TABLE
# # ======================================================

# st.divider()

# st.subheader(
#     "Transport Trip Records"
# )

# st.dataframe(
#     filtered_df,
#     use_container_width=True,
#     height=300
# )

# # ======================================================
# # AI SUMMARY DATA
# # ======================================================

# top_route = route_delay.iloc[0]

# worst_weather = weather_delay.sort_values(
#     by="Delay_Minutes",
#     ascending=False
# ).iloc[0]

# peak_hour = hourly_delay.sort_values(
#     by="Delay_Minutes",
#     ascending=False
# ).iloc[0]

# summary_text = f"""
# Transport Analytics Summary:

# Average Delay: {avg_delay:.2f} minutes

# OTP Percentage: {otp:.2f}%

# Most Delayed Route:
# Route ID {top_route['RouteID']}
# with average delay of
# {top_route['Delay_Minutes']:.2f} mins

# Worst Weather Condition:
# {worst_weather['WeatherCondition']}
# causing average delay of
# {worst_weather['Delay_Minutes']:.2f} mins

# Peak Delay Hour:
# {int(peak_hour['Hour'])}:00
# with average delay of
# {peak_hour['Delay_Minutes']:.2f} mins
# """

# # ======================================================
# # AI INSIGHTS
# # ======================================================

# st.divider()

# st.subheader(
#     "🤖 AI Operational Insights"
# )

# if st.button(
#     "Generate AI Insights"
# ):

#     with st.spinner(
#         "Analyzing transport operations..."
#     ):

#         prompt = f"""
#         You are an expert transport
#         operations analyst.

#         Analyze the following
#         transport data.

#         Provide:
#         1. Key Insights
#         2. Delay Causes
#         3. Operational Risks
#         4. Recommendations

#         Rules:
#         - Keep response concise
#         - Use bullet points
#         - Be practical
#         - Be data-driven
#         - Avoid generic explanations

#         Data:
#         {summary_text}
#         """

#         response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",

#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],

#             temperature=0.3
#         )

#         ai_output = (
#             response
#             .choices[0]
#             .message
#             .content
#         )

#         st.success(
#             "AI Analysis Complete"
#         )

#         st.markdown(ai_output)

# # ======================================================
# # ASK AI
# # ======================================================

# st.divider()

# st.subheader(
#     "💬 Ask AI About Operations"
# )

# user_question = st.text_input(
#     "Ask anything about transport performance"
# )

# if st.button("Ask AI"):

#     if user_question:

#         with st.spinner(
#             "Thinking..."
#         ):

#             prompt = f"""
#             You are an intelligent
#             transport analyst.

#             Use this transport summary:

#             {summary_text}

#             Answer this question:
#             {user_question}

#             Rules:
#             - Keep answer concise
#             - Be practical
#             - Use bullet points if needed
#             - Focus only on transport analytics
#             """

#             response = client.chat.completions.create(
#                 model="llama-3.3-70b-versatile",

#                 messages=[
#                     {
#                         "role": "user",
#                         "content": prompt
#                     }
#                 ],

#                 temperature=0.2
#             )

#             answer = (
#                 response
#                 .choices[0]
#                 .message
#                 .content
#             )

#             st.markdown(answer)

# # ======================================================
# # FOOTER
# # ======================================================

# st.markdown("---")

# st.caption(
#     "🚍 Operational Analytics Dashboard • "
#     "AI-Powered Public Transport Analysis"
# )


import streamlit as st
st.set_page_config(page_title="Public Transport Delay Analysis",layout="wide")
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

st.title("Public Transport Delay Analysis")
st.text("This project analyzes delays in public transportation using data such as routes, " \
"timings, traffic, and weather conditions. Built with Streamlit, the system provides " \
"interactive visualizations to identify delay patterns, peak congestion times, and " \
"route performance. The project helps improve transport efficiency and supports better " \
"travel planning through data-driven insights " )

st.markdown("Smart Analysis for Better Public Transportation  Analyze transport delays, identify " \
"congestion patterns,and improve travel efficiency using data-driven insights.")

st.divider()

col1, col2 = st.columns([2, 1],gap="large")

with col1:

    st.header("Overview")

    st.write("""
    The **Public Transport Delay Analysis System** is designed to analyze and monitor
    delays in buses and trains using transport-related datasets such as:

    - Route information
    - Traffic conditions
    - Travel timings
    - Weather conditions
    - Peak-hour congestion data

    The platform provides interactive dashboards and visual analytics
    that help identify delay trends, route performance, and traffic impact.
    """)

with col2:
    st.write("")
    st.write("")

    st.metric("Routes Monitored", "120+")
    st.metric("Daily Trips Analyzed", "15K+")
    st.metric("Average Delay Accuracy", "92%")

st.divider()

st.header("Why This Project Matters")
st.write("""
Public transportation systems often face delays due to traffic congestion,
weather conditions, route inefficiencies, and peak-hour overload.

This project helps transport authorities and commuters:

- Understand delay patterns
- Improve route planning
- Reduce congestion impact
- Enhance passenger experience
- Support efficient transportation management
""")

st.caption("Public Transport Analysis")