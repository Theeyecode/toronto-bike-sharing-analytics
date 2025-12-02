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
# st.pyplot(weekday_fig)

# Trips per month
st.subheader("Trips per Month")
month_fig = plot_trips_per_month(filtered_df)
st.image(str(month_fig), caption="Trips per Hour", use_container_width=True)
# st.pyplot(month_fig)

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







# import streamlit as st
# import pandas as pd
# from app_data import get_bike_data
# from feature_engineering import (
#     add_time_features,
#     add_weekend_flag,
#     add_rush_hour_flag,
# )

# from time_analysis import (
#     trips_per_hour,
#     trips_per_weekday,
#     trips_per_month,
#     trips_by_user_type,
# )

# from plots_time_plotly import (
#    plotly_trips_per_hour as plot_trips_per_hour,
#    plotly_trips_per_weekday as plot_trips_per_weekday,
#    plotly_trips_per_month as plot_trips_per_month,
#    plotly_trips_by_user_type as plot_trips_by_user_type,
# )

# # Streamlit Configuration
# st.set_page_config(
#     page_title="Toronto Bike Analytics Dashboard",
#     layout="wide"
# )

# st.title("Toronto Bike Sharing Analytics Dashboard")
# st.cache_data.clear()

# # File Upload
# with st.spinner("Loading bike data..."):
#     df = get_bike_data(use_clean_file=True)


# if df is not None:
#     # Feature Engineering
#     df = add_time_features(df)
#     df = add_weekend_flag(df)
#     df = add_rush_hour_flag(df)

#     st.success("Data Loaded & Processed Successfully!")

#     # FILTERS (Sidebar)
#     st.sidebar.header("Filters")

#     # User Type Filter
#     if "User Type" in df.columns:
#         all_user_types = df["User Type"].dropna().unique().tolist()
#     else:
#         st.error("Missing 'User Type' column in dataset.")
#         all_user_types = []

#     selected_user_types = st.sidebar.multiselect(
#         "Select User Type(s):",
#         options=all_user_types,
#         default=all_user_types
#     )

#     # Date Range Filter
#     df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
#     min_date = df["start_time"].min()
#     max_date = df["start_time"].max()

#     date_range = st.sidebar.date_input(
#         "Select Date Range:",
#         value=(min_date, max_date),
#         min_value=min_date,
#         max_value=max_date,
#     )

#     if len(date_range) == 2:
#         start_date, end_date = date_range
#         mask = (
#             df["User Type"].isin(selected_user_types)
#             & (df["start_time"] >= pd.to_datetime(start_date))
#             & (df["start_time"] <= pd.to_datetime(end_date))
#         )
#         df = df[mask]

#     st.info(f"Filtered dataset contains **{len(df):,} trips** after filters.")

#     # Time-Based Analysis 
#     st.header("Time-Based Analysis")

#     # Trips by Hour
#     st.subheader("Trips by Hour of Day")
#     hour_df = trips_per_hour(df)
#     st.plotly_chart(plot_trips_per_hour(hour_df), use_container_width=True)

#     # Trips by Weekday
#     st.subheader("Trips by Day of Week")
#     weekday_df = trips_per_weekday(df)
#     st.plotly_chart(plot_trips_per_weekday(weekday_df), use_container_width=True)

#     # Trips by Month
#     st.subheader("Trips per Month")
#     month_df = trips_per_month(df)
#     st.plotly_chart(plot_trips_per_month(month_df), use_container_width=True)

#     # Trips by User Type
#     st.subheader("Trips by User Type")
#     try:
#         user_type_df = trips_by_user_type(df)
#         st.plotly_chart(plot_trips_by_user_type(user_type_df), use_container_width=True)
#     except KeyError as e:
#         st.error(f"Error: {e}")

# else:
#     st.info("Upload a CSV file to begin.")

