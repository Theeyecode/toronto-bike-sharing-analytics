import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from app_data import get_bike_data

from time_analysis import (
    trips_per_hour,
    trips_per_weekday,
    trips_per_month,
    trips_by_user_type
)

from plots_time import (
    plot_trips_per_hour,
    plot_trips_per_weekday,
    plot_trips_per_month
)

st.set_page_config(
    page_title="Toronto Bike Sharing Dashboard",
    layout="wide"
)

@st.cache_data
def get_data():
    df = get_bike_data()

    # Ensure datetime
    df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
    df["end_time"] = pd.to_datetime(df["end_time"], errors="coerce")

    # Derived fields
    df["start_hour"] = df["start_time"].dt.hour
    df["start_weekday"] = df["start_time"].dt.day_name()
    df["start_month"] = df["start_time"].dt.month

    return df


df = get_data()

st.sidebar.header("Filters")

# Hour filter
hour_range = st.sidebar.slider(
    "Filter Start Hour",
    0, 23,
    (0, 23)
)

# User Type filter
user_options = ["All"]
if "User Type" in df.columns:
    user_options += sorted(df["User Type"].dropna().unique().tolist())

selected_user = st.sidebar.selectbox("User Type", user_options)

# Date filter
min_date = df["start_time"].min().date()
max_date = df["start_time"].max().date()

date_range = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date),
    min_value=min_date,
    max_value=max_date,
)

# Apply filters
filtered_df = df.copy()

# Hour filter
filtered_df = filtered_df[
    (filtered_df["start_hour"] >= hour_range[0]) &
    (filtered_df["start_hour"] <= hour_range[1])
]

# User type filter
if selected_user != "All":
    filtered_df = filtered_df[filtered_df["User Type"] == selected_user]

# Date filter
if isinstance(date_range, tuple) and len(date_range) == 2:
    start_date, end_date = date_range
    filtered_df = filtered_df[
        (filtered_df["start_time"].dt.date >= start_date) &
        (filtered_df["start_time"].dt.date <= end_date)
    ]

st.title("Toronto Bike Sharing — Analytics Dashboard")

st.write(
    f"Showing **{len(filtered_df):,} trips** after applying filters."
)

# Trips per hour
st.subheader("Trips per Hour of Day")
hour_fig = plot_trips_per_hour(filtered_df) 
st.image(str(hour_fig), caption="Trips per Hour", use_container_width=True)
#st.pyplot(hour_fig)

# Trips per weekday
st.subheader("Trips per Weekday")
weekday_fig = plot_trips_per_weekday(filtered_df)
st.image(str(weekday_fig), caption="Trips per Hour", use_container_width=True)
#st.pyplot(weekday_fig)

# Trips per month
st.subheader("Trips per Month")
month_fig = plot_trips_per_month(filtered_df)
st.image(str(month_fig), caption="Trips per Hour", use_container_width=True)
#st.pyplot(month_fig)

# Trips by user type
st.subheader("Trips by User Type")

try:
    user_df = trips_by_user_type(filtered_df)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(user_df["User Type"], user_df["trip_count"])
    ax.set_title("User Type Breakdown")
    ax.set_ylabel("Trips")

    st.pyplot(fig)

except KeyError as e:
    st.warning(str(e))


