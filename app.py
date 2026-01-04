import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from src.load_data import load_flight_data

# ---------------s-- Page Setup -----------------
st.set_page_config(
    page_title="✈ Flight Delays Dashboard",
    page_icon="✈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------- Theme -----------------
st.markdown(
    """
    <style>
    body {
        background-color: #0A3D62;
        color: #E0FFFF;
        font-family: 'Segoe UI', sans-serif;
    }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A3D62 0%, #062d46 100%);
        color: #E0FFFF;
        border-right: 2px solid #0D47A1;
    }
    [data-testid="stSidebar"] h1, 
    [data-testid="stSidebar"] h2, 
    [data-testid="stSidebar"] h3 {
        color: #00BFFF;
        font-weight: bold;
    }

    /* Sidebar labels */
    [data-testid="stSidebar"] label {
        color: #FFFFFF !important;
        font-weight: 500;
    }

    /* Sidebar markdown text */
    [data-testid="stSidebar"] .stMarkdown p {
        color: #87CEFA !important;
        font-size: 13px;
    }

    /* Headings */
    h1,h2,h3,h4,h5,h6 {
        color: #00BFFF;
        font-weight: 600;
        letter-spacing: 0.5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------- Load Data -----------------
@st.cache_data
def load_data():
    return load_flight_data()

try:
    data = load_data()
    df_flights = data["flights"]
except:
    st.error("❌ Error loading data")
    st.stop()

# ----------------- Clean Data -----------------
delay_cols = [
    'DEPARTURE_DELAY', 'ARRIVAL_DELAY', 'AIR_SYSTEM_DELAY',
    'SECURITY_DELAY', 'AIRLINE_DELAY', 'LATE_AIRCRAFT_DELAY', 'WEATHER_DELAY'
]
df_flights[delay_cols] = df_flights[delay_cols].fillna(0)

df_flights['AIRLINE'] = df_flights['AIRLINE'].astype(str)
df_flights['ORIGIN_AIRPORT'] = df_flights['ORIGIN_AIRPORT'].astype(str)
df_flights['DESTINATION_AIRPORT'] = df_flights['DESTINATION_AIRPORT'].astype(str)

important_cols = [
    'YEAR', 'MONTH', 'DAY', 'DAY_OF_WEEK', 'AIRLINE',
    'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT',
    'DEPARTURE_DELAY', 'ARRIVAL_DELAY',
    'CANCELLED', 'DIVERTED'
]
df_flights = df_flights[important_cols]

# ----------------- Filters -----------------
st.sidebar.title("🎛 Filters & Options")

selected_airline = st.sidebar.multiselect(
    "Select Airline",
    options=sorted(df_flights['AIRLINE'].unique())
)

selected_month = st.sidebar.slider(
    "Select Month Range", 1, 12, (1, 12)
)

df_filtered = df_flights
if selected_airline:
    df_filtered = df_filtered[df_filtered['AIRLINE'].isin(selected_airline)]
df_filtered = df_filtered[
    (df_filtered['MONTH'] >= selected_month[0]) &
    (df_filtered['MONTH'] <= selected_month[1])
]

# ----------------- Title -----------------
st.title("✈ Flight Delay Dashboard 2015")
st.markdown("Interactive BI Dashboard for Flight Delays Analysis")

# ----------------- Summary Statistics -----------------
st.subheader("📊 Summary Statistics")
col1, col2, col3, col4 = st.columns(4)

def metric_card(title, value, color, container):
    container.markdown(
        f"""
        <div style='background: linear-gradient(135deg, {color}, #062d46);
                    padding:15px; border-radius:12px; text-align:center; 
                    box-shadow: 2px 2px 8px rgba(0,0,0,0.3); margin:2px'>
            <h5 style='color:#AAAAAA; font-weight:500'>{title}</h5>
            <h2 style='color:#FFFFFF; font-size:24px; font-weight:bold'>{value}</h2>
        </div>
        """,
        unsafe_allow_html=True
    )

metric_card("Total Flights", df_filtered.shape[0], "#1E90FF", col1)
metric_card("Cancelled Flights", int(df_filtered['CANCELLED'].sum()), "#00BFFF", col2)
metric_card("Diverted Flights", int(df_filtered['DIVERTED'].sum()), "#00CED1", col3)
metric_card("Average Arrival Delay", round(df_filtered['ARRIVAL_DELAY'].mean(), 2), "#1E90FF", col4)

# ----------------- Unified Dark Blue -----------------
dark_blue = "#0D47A1"

# ----------------- Visual Analytics -----------------
st.subheader("📈 Visual Analytics")

# Row 1
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("Arrival Delay by Origin Airport")
    state_data = df_filtered.groupby("ORIGIN_AIRPORT")["ARRIVAL_DELAY"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#0A3D62")
    ax.set_facecolor("#0A3D62")
    state_data.plot(kind="bar", ax=ax, color=dark_blue)
    ax.set_title("Arrival Delay by Origin Airport", color="#00BFFF")
    ax.tick_params(colors="white")
    fig.tight_layout()
    st.pyplot(fig)

with col_b:
    st.markdown("Arrival Delay by Airline")
    business_data = df_filtered.groupby("AIRLINE")["ARRIVAL_DELAY"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#0A3D62")
    ax.set_facecolor("#0A3D62")
    business_data.plot(kind="barh", ax=ax, color=dark_blue)
    ax.set_title("Arrival Delay by Airline", color="#00BFFF")
    ax.tick_params(colors="white")
    fig.tight_layout()
    st.pyplot(fig)

# Row 2
col_c, col_d = st.columns(2)

with col_c:
    st.markdown("Average Arrival Delay by Day of Week")
    line_data = df_filtered.groupby("DAY_OF_WEEK")["ARRIVAL_DELAY"].mean()
    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#0A3D62")
    ax.set_facecolor("#0A3D62")
    ax.plot(line_data.index, line_data.values, marker='o', color=dark_blue, linewidth=2)
    ax.set_title("Average Arrival Delay by Day of Week", color="#00BFFF")
    ax.tick_params(colors="white")
    ax.set_xlabel("Day of Week", color="white")
    ax.set_ylabel("Avg Arrival Delay", color="white")
    fig.tight_layout()
    st.pyplot(fig)

with col_d:
    st.markdown("Cancelled Flights Percentage per Month")
    cancelled_pct = df_filtered.groupby("MONTH")["CANCELLED"].mean() * 100
    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#0A3D62")
    ax.set_facecolor("#0A3D62")
    cancelled_pct.plot(kind="bar", ax=ax, color=dark_blue)
    ax.set_title("Cancelled Flights Percentage", color="#00BFFF")
    ax.tick_params(colors="white")
    fig.tight_layout()
    st.pyplot(fig)

# Row 3
col_e, col_f = st.columns(2)

with col_e:
    st.markdown("Top 10 Origin Airports by Average Arrival Delay")
    top_airports = df_filtered.groupby("ORIGIN_AIRPORT")["ARRIVAL_DELAY"].mean().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#0A3D62")
    ax.set_facecolor("#0A3D62")
    top_airports.plot(kind="bar", ax=ax, color=dark_blue)
    ax.set_title("Top Origin Airports by Avg Arrival Delay", color="#00BFFF")
    ax.tick_params(colors="white")
    fig.tight_layout()
    st.pyplot(fig)

with col_f:
    st.markdown("Monthly Average Arrival Delay")
    monthly_delay = df_filtered.groupby("MONTH")["ARRIVAL_DELAY"].mean()
    fig, ax = plt.subplots(figsize=(6, 4), facecolor="#0A3D62")
    ax.set_facecolor("#0A3D62")
    monthly_delay.plot(kind="line", marker="o", ax=ax, color=dark_blue, linewidth=2)
    ax.set_title("Monthly Average Arrival Delay", color="#00BFFF")
    ax.tick_params(colors="white")
    fig.tight_layout()
    st.pyplot(fig)

# ----------------- Table -----------------
st.subheader("📋 Flights Table (first 100 rows)")
st.dataframe(df_filtered.head(100))