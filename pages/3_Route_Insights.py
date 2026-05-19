# # import streamlit as st
# # import pandas as pd
# # import plotly.express as px

# # # ======================================================
# # # PAGE CONFIG
# # # ======================================================

# # st.set_page_config(
# #     page_title="Route Insights",
# #     layout="wide"
# # )

# # # ======================================================
# # # SIDEBAR TITLE + STYLING
# # # ======================================================

# # st.markdown("""
# # <style>

# # /* ---- Sidebar Title ---- */
# # section[data-testid="stSidebar"]::before {
# #     content: "🚍 Route Analytics";
# #     display: block;
# #     margin-top: 70px;
# #     padding: 0px 20px 15px 20px;
# #     font-size: 26px;
# #     font-weight: bold;
# #     color: #e2d9f3;
# #     border-bottom: 1px solid #4a3470;
# # }



# # /* ---- App Background ---- */
# # .stApp {
# #     color: #e2d9f3;
# # }

# # /* ---- Metric Tiles ---- */
# # [data-testid="stMetric"] {
# #     border: 1px solid #6b3fa0;
# #     padding: 16px;
# #     border-radius: 12px;
# #     text-align: center;
# # }

# # [data-testid="stMetricLabel"] {
# #     color: #c4b0e8 !important;
# #     font-size: 0.85rem;
# #     letter-spacing: 0.05em;
# #     text-transform: uppercase;
# # }

# # [data-testid="stMetricValue"] {
# #     color: #f0eaff !important;
# #     font-weight: 700;
# # }

# # /* ---- Headings ---- */
# # h1, h2, h3 {
# #     color: #c084fc !important;
# # }

# # /* ---- Plotly Chart Container ---- */
# # div[data-testid="stPlotlyChart"] {
# #     background: linear-gradient(135deg, #1e0f3d 0%, #2a1555 100%);
# #     padding: 10px;
# #     border-radius: 14px;
# #     border: 1px solid #4a3470;
# #     box-shadow: 0 4px 20px rgba(90, 40, 160, 0.2);
# # }

# # /* ---- Sidebar multiselect labels ---- */
# # .stMultiSelect label, .stMultiSelect span {
# #     color: #c4b0e8 !important;
# # }

# # /* ---- Sidebar filter pills ---- */
# # [data-testid="stMultiSelect"] span[data-baseweb="tag"] {
# #     background-color: #5b21b6 !important;
# #     color: #f0eaff !important;
# # }

# # /* ---- Divider ---- */
# # hr {
# #     border-color: #4a3470 !important;
# # }

# # /* ---- General text ---- */
# # p, span, label {
# #     color: #d8cef0;
# # }

# # /* ---- Caption ---- */
# # .stCaption {
# #     color: #9d86c4 !important;
# # }

# # </style>
# # """, unsafe_allow_html=True)
# # # ======================================================
# # # LOAD DATA
# # # ======================================================

# # trips = pd.read_excel("data/Fact_Trips_Cleaned.xlsx")
# # routes = pd.read_excel("data/Dim_Routes_Cleaned.xlsx")

# # # ======================================================
# # # MERGE DATA
# # # ======================================================

# # if "RouteID" in routes.columns:

# #     df = trips.merge(
# #         routes,
# #         on="RouteID",
# #         how="left"
# #     )

# # else:
# #     df = trips.copy()

# # # ======================================================
# # # DATA CLEANING
# # # ======================================================

# # df["Delay_Minutes"] = pd.to_numeric(
# #     df["Delay_Minutes"],
# #     errors="coerce"
# # )

# # df["VehicleType"] = (
# #     df["VehicleType"]
# #     .astype(str)
# #     .str.strip()
# # )

# # df["Status"] = (
# #     df["Status"]
# #     .astype(str)
# #     .str.strip()
# # )

# # # ======================================================
# # # SIDEBAR FILTERS
# # # ======================================================

# # st.sidebar.subheader("🎛️ Filters")

# # route_filter = st.sidebar.selectbox(
# #     "Select Route",
# #     sorted(df["RouteID"].dropna().unique()),
# #     key="route_filter"
# # )

# # vehicle_filter = st.sidebar.multiselect(
# #     "Vehicle Type",
# #     sorted(df["VehicleType"].dropna().unique()),
# #     default=sorted(df["VehicleType"].dropna().unique()),
# #     key="vehicle_filter"
# # )

# # status_filter = st.sidebar.multiselect(
# #     "Trip Status",
# #     sorted(df["Status"].dropna().unique()),
# #     default=sorted(df["Status"].dropna().unique()),
# #     key="status_filter"
# # )

# # # ======================================================
# # # FILTER DATA
# # # ======================================================

# # filtered_df = df[
# #     (df["RouteID"] == route_filter) &
# #     (df["VehicleType"].isin(vehicle_filter)) &
# #     (df["Status"].isin(status_filter))
# # ]

# # # ======================================================
# # # EMPTY CHECK
# # # ======================================================

# # if filtered_df.empty:

# #     st.warning("No data available for selected filters.")
# #     st.stop()

# # # ======================================================
# # # PAGE TITLE
# # # ======================================================

# # st.title("🛣️ Route Insights Dashboard")

# # st.markdown("""
# # Analyze transport route performance,
# # delay trends, congestion levels,
# # weather impact, and vehicle operations.
# # """)

# # st.divider()

# # # ======================================================
# # # KPI SECTION
# # # ======================================================

# # avg_delay = filtered_df["Delay_Minutes"].mean()

# # max_delay = filtered_df["Delay_Minutes"].max()

# # trip_count = len(filtered_df)

# # on_time_percent = (
# #     (filtered_df["Status"] == "On-Time").sum()
# #     / len(filtered_df)
# # ) * 100

# # k1, k2, k3, k4 = st.columns(4)

# # with k1:
# #     st.metric(
# #         "Average Delay",
# #         f"{avg_delay:.1f} mins"
# #     )

# # with k2:
# #     st.metric(
# #         "Maximum Delay",
# #         f"{max_delay:.1f} mins"
# #     )

# # with k3:
# #     st.metric(
# #         "Trips Count",
# #         trip_count
# #     )

# # with k4:
# #     st.metric(
# #         "On-Time %",
# #         f"{on_time_percent:.1f}%"
# #     )

# # st.divider()

# # # ======================================================
# # # ROUTE INFORMATION
# # # ======================================================

# # st.subheader("📍 Route Information")

# # route_info = filtered_df.iloc[0]

# # info1, info2, info3, info4 = st.columns(4)

# # with info1:

# #     st.info(
# #         f"**Origin**\n\n"
# #         f"{route_info.get('Origin', 'N/A')}"
# #     )

# # with info2:

# #     st.info(
# #         f"**Destination**\n\n"
# #         f"{route_info.get('Destination', 'N/A')}"
# #     )

# # with info3:

# #     st.info(
# #         f"**Distance**\n\n"
# #         f"{route_info.get('DistanceKM', 'N/A')} KM"
# #     )

# # with info4:

# #     st.info(
# #         f"**Vehicle**\n\n"
# #         f"{', '.join(vehicle_filter)}"
# #     )

# # st.divider()

# # # ======================================================
# # # CHARTS
# # # ======================================================

# # # Delay Distribution
# # fig_hist = px.histogram(
# #     filtered_df,
# #     x="Delay_Minutes",
# #     nbins=20,
# #     title="📊 Delay Distribution"
# # )

# # # Vehicle Distribution
# # fig_vehicle = px.pie(
# #     filtered_df,
# #     names="VehicleType",
# #     title="🚍 Vehicle Distribution"
# # )

# # # Weather Impact
# # weather_df = (
# #     filtered_df.groupby("WeatherCondition")[
# #         "Delay_Minutes"
# #     ]
# #     .mean()
# #     .reset_index()
# # )

# # fig_weather = px.bar(
# #     weather_df,
# #     x="WeatherCondition",
# #     y="Delay_Minutes",
# #     color="WeatherCondition",
# #     title="🌦️ Weather Impact"
# # )

# # # Congestion Impact
# # congestion_df = (
# #     filtered_df.groupby("CongestionLevel")[
# #         "Delay_Minutes"
# #     ]
# #     .mean()
# #     .reset_index()
# # )

# # fig_congestion = px.bar(
# #     congestion_df,
# #     x="CongestionLevel",
# #     y="Delay_Minutes",
# #     color="CongestionLevel",
# #     title="🚦 Congestion Impact"
# # )

# # # Peak Hour Analysis
# # peak_df = (
# #     filtered_df.groupby("PeakHour")[
# #         "Delay_Minutes"
# #     ]
# #     .mean()
# #     .reset_index()
# # )

# # fig_peak = px.bar(
# #     peak_df,
# #     x="PeakHour",
# #     y="Delay_Minutes",
# #     color="PeakHour",
# #     title="⏰ Peak Hour Analysis"
# # )

# # # Status Distribution
# # fig_status = px.pie(
# #     filtered_df,
# #     names="Status",
# #     title="✅ Trip Status Distribution"
# # )

# # # ======================================================
# # # COMMON CHART STYLING
# # # ======================================================

# # all_figures = [
# #     fig_hist,
# #     fig_vehicle,
# #     fig_weather,
# #     fig_congestion,
# #     fig_peak,
# #     fig_status
# # ]

# # for fig in all_figures:

# #     fig.update_layout(
# #         height=320,
# #         paper_bgcolor="#111827",
# #         plot_bgcolor="#111827",
# #         font_color="white",
# #         margin=dict(
# #             l=10,
# #             r=10,
# #             t=40,
# #             b=10
# #         )
# #     )

# # # ======================================================
# # # DASHBOARD LAYOUT
# # # ======================================================

# # # ROW 1
# # row1_col1, row1_col2 = st.columns(2)

# # with row1_col1:

# #     st.plotly_chart(
# #         fig_hist,
# #         use_container_width=True
# #     )

# # with row1_col2:

# #     st.plotly_chart(
# #         fig_vehicle,
# #         use_container_width=True
# #     )

# # # ROW 2
# # row2_col1, row2_col2 = st.columns(2)

# # with row2_col1:

# #     st.plotly_chart(
# #         fig_weather,
# #         use_container_width=True
# #     )

# # with row2_col2:

# #     st.plotly_chart(
# #         fig_congestion,
# #         use_container_width=True
# #     )

# # # ROW 3
# # row3_col1, row3_col2 = st.columns(2)

# # with row3_col1:

# #     st.plotly_chart(
# #         fig_peak,
# #         use_container_width=True
# #     )

# # with row3_col2:

# #     st.plotly_chart(
# #         fig_status,
# #         use_container_width=True
# #     )

# # # ======================================================
# # # FOOTER
# # # ======================================================

# # st.markdown("---")

# # st.caption(
# #     "🛣️ Route Insights Dashboard • Public Transport Delay Analysis"
# # )




# import streamlit as st
# import pandas as pd
# import plotly.express as px
# from groq import Groq

# # ======================================================
# # PAGE CONFIG
# # ======================================================

# st.set_page_config(
#     page_title="Route Insights",
#     layout="wide"
# )

# # ======================================================
# # GROQ CLIENT
# # ======================================================

# client = Groq(
#     api_key=st.secrets["API_KEY"]
# )

# # ======================================================
# # CUSTOM CSS
# # ======================================================

# st.markdown("""
# <style>

# /* ===== MAIN APP ===== */
# .stApp {
#     background: linear-gradient(
#         135deg,
#         #0f172a 0%,
#         #111827 50%,
#         #1e1b4b 100%
#     );
#     color: #f8fafc;
# }

# /* ===== SIDEBAR ===== */
# section[data-testid="stSidebar"] {
#     background: #0b1120;
#     border-right: 1px solid #312e81;
# }

# section[data-testid="stSidebar"]::before {
#     content: "🚍 Route Analytics";
#     display: block;
#     padding: 22px 20px;
#     font-size: 28px;
#     font-weight: 700;
#     color: white;
#     border-bottom: 1px solid #312e81;
# }

# /* ===== TITLES ===== */
# h1 {
#     font-size: 42px !important;
#     font-weight: 800 !important;
#     color: white !important;
# }

# h2, h3 {
#     color: #c4b5fd !important;
# }

# /* ===== METRIC CARDS ===== */
# [data-testid="stMetric"] {
#     background: rgba(255,255,255,0.05);

#     border: 1px solid rgba(139,92,246,0.35);

#     backdrop-filter: blur(12px);

#     padding: 20px;

#     border-radius: 18px;

#     box-shadow:
#         0 8px 30px rgba(0,0,0,0.25);

#     transition: all 0.3s ease;
# }

# [data-testid="stMetric"]:hover {
#     transform: translateY(-4px);
#     border-color: #8b5cf6;
# }

# [data-testid="stMetricLabel"] {
#     color: #d8b4fe !important;
#     font-size: 15px !important;
# }

# [data-testid="stMetricValue"] {
#     color: white !important;
#     font-size: 32px !important;
#     font-weight: 700 !important;
# }

# /* ===== CHARTS ===== */
# div[data-testid="stPlotlyChart"] {
#     background: rgba(17,24,39,0.75);

#     border: 1px solid rgba(139,92,246,0.2);

#     border-radius: 18px;

#     padding: 12px;

#     margin-top: 10px;

#     box-shadow:
#         0 8px 25px rgba(0,0,0,0.25);
# }

# /* ===== BUTTONS ===== */
# .stButton > button {
#     background: linear-gradient(
#         135deg,
#         #7c3aed,
#         #8b5cf6
#     );

#     color: white;

#     border: none;

#     border-radius: 12px;

#     padding: 10px 20px;

#     font-weight: 600;
# }

# /* ===== INPUT BOX ===== */
# .stTextInput input {
#     background-color: #111827 !important;
#     color: white !important;

#     border: 1px solid #7c3aed !important;

#     border-radius: 10px !important;
# }

# /* ===== MULTISELECT ===== */
# [data-baseweb="select"] {
#     background-color: #111827 !important;
# }

# [data-testid="stMultiSelect"] span[data-baseweb="tag"] {
#     background-color: #7c3aed !important;
#     color: white !important;
# }

# /* ===== DIVIDER ===== */
# hr {
#     border-color: rgba(255,255,255,0.08);
# }

# /* ===== DATAFRAME ===== */
# [data-testid="stDataFrame"] {
#     border-radius: 16px;
#     overflow: hidden;
# }

# </style>
# """, unsafe_allow_html=True)

# st.write(" ")

# # ======================================================
# # LOAD DATA
# # ======================================================

# @st.cache_data
# def load_data():

#     trips = pd.read_excel(
#         "data/Fact_Trips_Cleaned.xlsx"
#     )

#     routes = pd.read_excel(
#         "data/Dim_Routes_Cleaned.xlsx"
#     )

#     return trips, routes


# trips, routes = load_data()

# # ======================================================
# # MERGE DATA
# # ======================================================

# if "RouteID" in routes.columns:

#     df = trips.merge(
#         routes,
#         on="RouteID",
#         how="left"
#     )

# else:

#     df = trips.copy()

# # ======================================================
# # DATA CLEANING
# # ======================================================

# df["Delay_Minutes"] = pd.to_numeric(
#     df["Delay_Minutes"],
#     errors="coerce"
# )

# df["VehicleType"] = (
#     df["VehicleType"]
#     .astype(str)
#     .str.strip()
# )

# df["Status"] = (
#     df["Status"]
#     .astype(str)
#     .str.strip()
# )

# df["WeatherCondition"] = (
#     df["WeatherCondition"]
#     .astype(str)
#     .str.strip()
# )

# # ======================================================
# # SIDEBAR FILTERS
# # ======================================================

# st.sidebar.subheader("🎛️ Filters")

# route_filter = st.sidebar.selectbox(
#     "Select Route",
#     sorted(df["RouteID"].dropna().unique()),
#     key="route_filter"
# )

# vehicle_filter = st.sidebar.multiselect(
#     "Vehicle Type",
#     sorted(df["VehicleType"].dropna().unique()),
#     default=sorted(df["VehicleType"].dropna().unique()),
#     key="vehicle_filter"
# )

# status_filter = st.sidebar.multiselect(
#     "Trip Status",
#     sorted(df["Status"].dropna().unique()),
#     default=sorted(df["Status"].dropna().unique()),
#     key="status_filter"
# )

# # ======================================================
# # FILTER DATA
# # ======================================================

# filtered_df = df[
#     (df["RouteID"] == route_filter) &
#     (df["VehicleType"].isin(vehicle_filter)) &
#     (df["Status"].isin(status_filter))
# ]

# # ======================================================
# # EMPTY CHECK
# # ======================================================

# if filtered_df.empty:

#     st.warning(
#         "No data available for selected filters."
#     )

#     st.stop()

# # ======================================================
# # PAGE TITLE
# # ======================================================

# st.title("🛣️ Route Insights Dashboard")

# st.markdown("""
# Analyze transport route performance,
# delay trends, congestion levels,
# weather impact, and vehicle operations.
# """)

# st.divider()

# # ======================================================
# # KPI SECTION
# # ======================================================

# avg_delay = filtered_df["Delay_Minutes"].mean()

# max_delay = filtered_df["Delay_Minutes"].max()

# trip_count = len(filtered_df)

# on_time_percent = (
#     (filtered_df["Status"] == "On-Time").sum()
#     / len(filtered_df)
# ) * 100

# k1, k2, k3, k4 = st.columns(4)

# with k1:

#     st.metric(
#         "Average Delay",
#         f"{avg_delay:.1f} mins"
#     )

# with k2:

#     st.metric(
#         "Maximum Delay",
#         f"{max_delay:.1f} mins"
#     )

# with k3:

#     st.metric(
#         "Trips Count",
#         trip_count
#     )

# with k4:

#     st.metric(
#         "On-Time %",
#         f"{on_time_percent:.1f}%"
#     )

# st.divider()

# # ======================================================
# # AI FUNCTION
# # ======================================================

# def ask_ai(question, data):

#     summary = f"""

#     Route Selected:
#     {route_filter}

#     Average Delay:
#     {data['Delay_Minutes'].mean():.2f}

#     Maximum Delay:
#     {data['Delay_Minutes'].max():.2f}

#     On Time Percentage:
#     {on_time_percent:.2f}

#     Weather Analysis:
#     {data.groupby('WeatherCondition')['Delay_Minutes'].mean().to_string()}

#     Congestion Analysis:
#     {data.groupby('CongestionLevel')['Delay_Minutes'].mean().to_string()}

#     Vehicle Performance:
#     {data.groupby('VehicleType')['Delay_Minutes'].mean().to_string()}
#     """

#     prompt = f"""
#     You are an AI transport operations analyst.

#     Analyze this transport dataset summary.

#     Dataset Summary:
#     {summary}

#     User Question:
#     {question}

#     Give:
#     - concise answer
#     - operational insight
#     - useful recommendation
#     """

#     try:

#         response = client.chat.completions.create(
#             model="llama-3.3-70b-versatile",
#             messages=[
#                 {
#                     "role": "user",
#                     "content": prompt
#                 }
#             ],
#             temperature=0.3,
#             max_tokens=400
#         )

#         return response.choices[0].message.content

#     except Exception as e:

#         return f"❌ AI Service Error: {str(e)}"

# # ======================================================
# # ROUTE INFORMATION
# # ======================================================

# st.subheader("📍 Route Information")

# route_info = filtered_df.iloc[0]

# info1, info2, info3, info4 = st.columns(4)

# with info1:

#     st.info(
#         f"**Origin**\n\n"
#         f"{route_info.get('Origin', 'N/A')}"
#     )

# with info2:

#     st.info(
#         f"**Destination**\n\n"
#         f"{route_info.get('Destination', 'N/A')}"
#     )

# with info3:

#     st.info(
#         f"**Distance**\n\n"
#         f"{route_info.get('DistanceKM', 'N/A')} KM"
#     )

# with info4:

#     st.info(
#         f"**Vehicle**\n\n"
#         f"{', '.join(vehicle_filter)}"
#     )

# st.divider()

# # ======================================================
# # CHARTS
# # ======================================================

# # Delay Distribution
# fig_hist = px.histogram(
#     filtered_df,
#     x="Delay_Minutes",
#     nbins=20,
#     title="📊 Delay Distribution",
#     color_discrete_sequence=["#8b5cf6"]
# )

# # Vehicle Distribution
# fig_vehicle = px.pie(
#     filtered_df,
#     names="VehicleType",
#     title="🚍 Vehicle Distribution"
# )

# # Weather Impact
# weather_df = (
#     filtered_df.groupby("WeatherCondition")[
#         "Delay_Minutes"
#     ]
#     .mean()
#     .reset_index()
# )

# fig_weather = px.bar(
#     weather_df,
#     x="WeatherCondition",
#     y="Delay_Minutes",
#     color="WeatherCondition",
#     title="🌦️ Weather Impact"
# )

# # Congestion Impact
# congestion_df = (
#     filtered_df.groupby("CongestionLevel")[
#         "Delay_Minutes"
#     ]
#     .mean()
#     .reset_index()
# )

# fig_congestion = px.bar(
#     congestion_df,
#     x="CongestionLevel",
#     y="Delay_Minutes",
#     color="CongestionLevel",
#     title="🚦 Congestion Impact"
# )

# # Peak Hour Analysis
# peak_df = (
#     filtered_df.groupby("PeakHour")[
#         "Delay_Minutes"
#     ]
#     .mean()
#     .reset_index()
# )

# fig_peak = px.bar(
#     peak_df,
#     x="PeakHour",
#     y="Delay_Minutes",
#     color="PeakHour",
#     title="⏰ Peak Hour Analysis"
# )

# # Status Distribution
# fig_status = px.pie(
#     filtered_df,
#     names="Status",
#     title="✅ Trip Status Distribution"
# )

# # ======================================================
# # COMMON CHART STYLING
# # ======================================================

# all_figures = [
#     fig_hist,
#     fig_vehicle,
#     fig_weather,
#     fig_congestion,
#     fig_peak,
#     fig_status
# ]

# for fig in all_figures:

#     fig.update_layout(
#         height=320,
#         paper_bgcolor="#111827",
#         plot_bgcolor="#111827",
#         font_color="white",
#         margin=dict(
#             l=10,
#             r=10,
#             t=40,
#             b=10
#         )
#     )

# # ======================================================
# # DASHBOARD LAYOUT
# # ======================================================

# # ROW 1
# row1_col1, row1_col2 = st.columns(2)

# with row1_col1:

#     st.plotly_chart(
#         fig_hist,
#         use_container_width=True
#     )

# with row1_col2:

#     st.plotly_chart(
#         fig_vehicle,
#         use_container_width=True
#     )

# # ROW 2
# row2_col1, row2_col2 = st.columns(2)

# with row2_col1:

#     st.plotly_chart(
#         fig_weather,
#         use_container_width=True
#     )

# with row2_col2:

#     st.plotly_chart(
#         fig_congestion,
#         use_container_width=True
#     )

# # ROW 3
# row3_col1, row3_col2 = st.columns(2)

# with row3_col1:

#     st.plotly_chart(
#         fig_peak,
#         use_container_width=True
#     )

# with row3_col2:

#     st.plotly_chart(
#         fig_status,
#         use_container_width=True
#     )

# # ======================================================
# # AI ASSISTANT
# # ======================================================

# st.divider()

# st.subheader("🤖 AI Transport Assistant")

# st.markdown("""
# Ask AI questions about:

# - Delay causes
# - Weather impact
# - Congestion patterns
# - Vehicle performance
# - Route efficiency
# - Operational improvements
# """)

# user_question = st.text_input(
#     "Ask AI about transport operations"
# )

# if st.button(
#     "🚀 Analyze with AI",
#     use_container_width=True
# ):

#     if user_question:

#         with st.spinner(
#             "Analyzing transport data..."
#         ):

#             ai_result = ask_ai(
#                 user_question,
#                 filtered_df
#             )

#         st.markdown(
#             f"""
#             <div class="ai-panel">
#             <h3>🤖 AI Insights</h3>
#             <p>{ai_result}</p>
#             </div>
#             """,
#             unsafe_allow_html=True
#         )

#     else:

#         st.warning(
#             "Please enter a question."
#         )

# # ======================================================
# # FOOTER
# # ======================================================

# st.markdown("---")

# st.caption(
#     "🛣️ Route Insights Dashboard • AI-Powered Transport Analytics"
# )




# ======================================================
# IMPORTS
# ======================================================

import streamlit as st
import pandas as pd
import plotly.express as px
from groq import Groq

# ======================================================
# PAGE CONFIG
# ======================================================

st.set_page_config(
    page_title="Route Insights",
    layout="wide"
)

# ======================================================
# GROQ CLIENT
# ======================================================

client = Groq(
    api_key=st.secrets["API_KEY"]
)

# ======================================================
# CUSTOM CSS
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

st.write(" ")

# ======================================================
# LOAD DATA
# ======================================================

@st.cache_data
def load_data():

    trips = pd.read_excel(
        "data/Fact_Trips_Cleaned.xlsx"
    )

    routes = pd.read_excel(
        "data/Dim_Routes_Cleaned.xlsx"
    )

    return trips, routes


trips, routes = load_data()

# ======================================================
# MERGE DATA
# ======================================================

if "RouteID" in routes.columns:

    df = trips.merge(
        routes,
        on="RouteID",
        how="left"
    )

else:

    df = trips.copy()

# ======================================================
# DATA CLEANING
# ======================================================

df["Delay_Minutes"] = pd.to_numeric(
    df["Delay_Minutes"],
    errors="coerce"
)

df["VehicleType"] = (
    df["VehicleType"]
    .astype(str)
    .str.strip()
)

df["Status"] = (
    df["Status"]
    .astype(str)
    .str.strip()
)

df["WeatherCondition"] = (
    df["WeatherCondition"]
    .astype(str)
    .str.strip()
)

# ======================================================
# SIDEBAR FILTERS
# ======================================================

st.sidebar.subheader("🎛️ Filters")

route_filter = st.sidebar.selectbox(
    "Select Route",
    sorted(df["RouteID"].dropna().unique()),
    key="route_filter"
)

vehicle_filter = st.sidebar.multiselect(
    "Vehicle Type",
    sorted(df["VehicleType"].dropna().unique()),
    default=sorted(df["VehicleType"].dropna().unique()),
    key="vehicle_filter"
)

status_filter = st.sidebar.multiselect(
    "Trip Status",
    sorted(df["Status"].dropna().unique()),
    default=sorted(df["Status"].dropna().unique()),
    key="status_filter"
)

# ======================================================
# FILTER DATA
# ======================================================

filtered_df = df[
    (df["RouteID"] == route_filter) &
    (df["VehicleType"].isin(vehicle_filter)) &
    (df["Status"].isin(status_filter))
]

# ======================================================
# EMPTY CHECK
# ======================================================

if filtered_df.empty:

    st.warning(
        "No data available for selected filters."
    )

    st.stop()

# ======================================================
# PAGE TITLE
# ======================================================

st.title("🛣️ Route Insights Dashboard")

st.markdown("""
Analyze transport route performance,
delay trends, congestion levels,
weather impact, and vehicle operations.
""")

st.divider()

# ======================================================
# KPI SECTION
# ======================================================

avg_delay = filtered_df["Delay_Minutes"].mean()

max_delay = filtered_df["Delay_Minutes"].max()

trip_count = len(filtered_df)

on_time_percent = (
    (filtered_df["Status"] == "On-Time").sum()
    / len(filtered_df)
) * 100

k1, k2, k3, k4 = st.columns(4)

with k1:

    st.metric(
        "Average Delay",
        f"{avg_delay:.1f} mins"
    )

with k2:

    st.metric(
        "Maximum Delay",
        f"{max_delay:.1f} mins"
    )

with k3:

    st.metric(
        "Trips Count",
        trip_count
    )

with k4:

    st.metric(
        "On-Time %",
        f"{on_time_percent:.1f}%"
    )

st.divider()

# ======================================================
# ROUTE EFFICIENCY LEADERBOARD
# ======================================================

# ======================================================
# AI FUNCTION
# ======================================================

def ask_ai(question, data):

    summary = f"""

    Route Selected:
    {route_filter}

    Average Delay:
    {data['Delay_Minutes'].mean():.2f}

    Maximum Delay:
    {data['Delay_Minutes'].max():.2f}

    On Time Percentage:
    {on_time_percent:.2f}

    Weather Analysis:
    {data.groupby('WeatherCondition')['Delay_Minutes'].mean().to_string()}

    Congestion Analysis:
    {data.groupby('CongestionLevel')['Delay_Minutes'].mean().to_string()}

    Vehicle Performance:
    {data.groupby('VehicleType')['Delay_Minutes'].mean().to_string()}
    """

    prompt = f"""
    You are an AI transport operations analyst.

    Analyze this transport dataset summary.

    Dataset Summary:
    {summary}

    User Question:
    {question}

    Give:
    - concise answer
    - operational insight
    - useful recommendation
    """

    try:

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=400
        )

        return response.choices[0].message.content

    except Exception as e:

        return f"❌ AI Service Error: {str(e)}"

# ======================================================
# ROUTE INFORMATION
# ======================================================

st.subheader("📍 Route Information")

route_info = filtered_df.iloc[0]

info1, info2, info3, info4 = st.columns(4)

with info1:

    st.info(
        f"**Origin**\n\n"
        f"{route_info.get('Origin', 'N/A')}"
    )

with info2:

    st.info(
        f"**Destination**\n\n"
        f"{route_info.get('Destination', 'N/A')}"
    )

with info3:

    st.info(
        f"**Distance**\n\n"
        f"{route_info.get('DistanceKM', 'N/A')} KM"
    )

with info4:

    st.info(
        f"**Vehicle**\n\n"
        f"{', '.join(vehicle_filter)}"
    )

st.divider()

# ======================================================
# CHARTS
# ======================================================

# Delay Distribution
fig_hist = px.histogram(
    filtered_df,
    x="Delay_Minutes",
    nbins=20,
    title="📊 Delay Distribution",
    color_discrete_sequence=["#8b5cf6"]
)

# Vehicle Distribution
fig_vehicle = px.pie(
    filtered_df,
    names="VehicleType",
    title="🚍 Vehicle Distribution"
)

# Weather Impact
weather_df = (
    filtered_df.groupby("WeatherCondition")[
        "Delay_Minutes"
    ]
    .mean()
    .reset_index()
)

fig_weather = px.bar(
    weather_df,
    x="WeatherCondition",
    y="Delay_Minutes",
    color="WeatherCondition",
    title="🌦️ Weather Impact"
)

# Congestion Impact
congestion_df = (
    filtered_df.groupby("CongestionLevel")[
        "Delay_Minutes"
    ]
    .mean()
    .reset_index()
)

fig_congestion = px.bar(
    congestion_df,
    x="CongestionLevel",
    y="Delay_Minutes",
    color="CongestionLevel",
    title="🚦 Congestion Impact"
)

# Peak Hour Analysis
peak_df = (
    filtered_df.groupby("PeakHour")[
        "Delay_Minutes"
    ]
    .mean()
    .reset_index()
)

fig_peak = px.bar(
    peak_df,
    x="PeakHour",
    y="Delay_Minutes",
    color="PeakHour",
    title="⏰ Peak Hour Analysis"
)

# Status Distribution
fig_status = px.pie(
    filtered_df,
    names="Status",
    title="✅ Trip Status Distribution"
)

# ======================================================
# COMMON CHART STYLING
# ======================================================

all_figures = [
    fig_hist,
    fig_vehicle,
    fig_weather,
    fig_congestion,
    fig_peak,
    fig_status
]

for fig in all_figures:

    fig.update_layout(
        height=320,
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font_color="white",
        margin=dict(
            l=10,
            r=10,
            t=40,
            b=10
        )
    )

# ======================================================
# DASHBOARD LAYOUT
# ======================================================

# ROW 1
row1_col1, row1_col2 = st.columns(2)

with row1_col1:

    st.plotly_chart(
        fig_hist,
        use_container_width=True
    )

with row1_col2:

    st.plotly_chart(
        fig_vehicle,
        use_container_width=True
    )

# ROW 2
row2_col1, row2_col2 = st.columns(2)

with row2_col1:

    st.plotly_chart(
        fig_weather,
        use_container_width=True
    )

with row2_col2:

    st.plotly_chart(
        fig_congestion,
        use_container_width=True
    )

# ROW 3
row3_col1, row3_col2 = st.columns(2)

with row3_col1:

    st.plotly_chart(
        fig_peak,
        use_container_width=True
    )

with row3_col2:

    st.plotly_chart(
        fig_status,
        use_container_width=True
    )

# ======================================================
# AI ASSISTANT
# ======================================================

st.divider()

st.subheader("🤖 AI Transport Assistant")

st.markdown("""
Ask AI questions about:

- Delay causes
- Weather impact
- Congestion patterns
- Vehicle performance
- Route efficiency
- Operational improvements
""")

user_question = st.text_input(
    "Ask AI about transport operations"
)

if st.button(
    "🚀 Analyze with AI",
    use_container_width=True
):

    if user_question:

        with st.spinner(
            "Analyzing transport data..."
        ):

            ai_result = ask_ai(
                user_question,
                filtered_df
            )

        # ✅ FIX: Render the container with HTML, but use st.markdown
        # for the AI text separately to avoid HTML injection issues
        st.markdown(
            """
            <div style="
                background:rgba(91,33,182,0.15);
                border:1px solid rgba(139,92,246,0.25);
                border-radius:16px;
                padding:20px;
                margin-top:10px;
            ">
                <h3 style="color:#c4b5fd;">
                    🤖 AI Insights
                </h3>
            </div>
            """,
            unsafe_allow_html=True
        )

        # ✅ Render AI text safely outside the HTML block
        st.markdown(
            ai_result,
            unsafe_allow_html=False
        )

    else:

        st.warning(
            "Please enter a question."
        )

# ======================================================
# FOOTER
# ======================================================

st.markdown("---")

st.caption(
    "🛣️ Route Insights Dashboard • AI-Powered Transport Analytics"
)
