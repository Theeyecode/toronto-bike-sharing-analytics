from __future__ import annotations
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

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

def render(df: pd.DataFrame) -> None:
    st.title("Time-based Trends — Dhruv")

    st.markdown(
        """
        This page includes:
        - Trip counts by **hour of day**
        - Patterns by **day of week**
        - Monthly / seasonal trends
        - Breakdown by **user type**
        - Filters for **date** and **hour range**
        """
    )

    df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
    df["start_hour"] = df["start_time"].dt.hour
    df["start_weekday"] = df["start_time"].dt.day_name()
    df["start_month"] = df["start_time"].dt.month

    # DATE FILTER
    st.subheader("Filter by Start & End Date")

    min_date = df["start_time"].min().date()
    max_date = df["start_time"].max().date()

    start_date = st.date_input("Start Date", min_value=min_date, value=min_date)
    end_date   = st.date_input("End Date", min_value=min_date, value=max_date)

    mask_date = (df["start_time"] >= pd.to_datetime(start_date)) & \
                (df["start_time"] <= pd.to_datetime(end_date))

    filtered_df = df[mask_date]

  
    # HOUR FILTER
    st.subheader("Filter by Hour of Day")

    hour_range = st.slider(
        "Select Hour Range",
        min_value=0,
        max_value=23,
        value=(0, 23)
    )

    filtered_df = filtered_df[
        (filtered_df["start_hour"] >= hour_range[0]) &
        (filtered_df["start_hour"] <= hour_range[1])
    ]

    st.markdown(f"**Filtered rows:** {len(filtered_df):,}")

    
    # VISUALS
    st.subheader("Time Trend Visuals")

    col1, col2 = st.columns(2)

    # Trips by Hour
    with col1:
        st.markdown("### Trips by Hour of Day")
        hour_path = plot_trips_per_hour(filtered_df)
        st.image(str(hour_path), use_container_width=True)

    # Trips by Weekday
    with col2:
        st.markdown("### Trips by Day of Week")
        weekday_path = plot_trips_per_weekday(filtered_df)
        st.image(str(weekday_path), use_container_width=True)

    # Trips by Month
    st.markdown("### Trips per Month")
    month_path = plot_trips_per_month(filtered_df)
    st.image(str(month_path), use_container_width=True)

   
    # TRIPS BY USER TYPE
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

    st.markdown("---")
    st.info("Developer notes:")




# from __future__ import annotations
# import pandas as pd
# import streamlit as st

# from plots_time import (
#     plot_trips_per_hour,
#     plot_trips_per_weekday,
#     plot_trips_per_month
# )

# def render(df: pd.DataFrame) -> None:
#     st.title("Time-based Trends — Dhruv")

#     st.markdown(
#         """
#         This page is owned by **Dhruv**.

#         It includes:
#         - Trip counts by **hour of day**
#         - Patterns by **day of week**
#         - Monthly / seasonal trends

#         These visuals come directly from your analysis functions.
#         """
#     )

#     # ===========================
#     # 🔧 Ensure datetime & derived columns (IMPORTANT)
#     # ===========================
#     df["start_time"] = pd.to_datetime(df["start_time"], errors="coerce")
#     df["end_time"] = pd.to_datetime(df["end_time"], errors="coerce")

#     df["start_hour"] = df["start_time"].dt.hour
#     df["start_weekday"] = df["start_time"].dt.day_name()
#     df["start_month"] = df["start_time"].dt.month

#     # ===========================
#     # 🔍 DATE FILTER SECTION
#     # ===========================
#     st.subheader("Filter by Start & End Time")

#     min_date = df["start_time"].min().date()
#     max_date = df["start_time"].max().date()

#     start_date = st.date_input("Start Date", min_date)
#     end_date   = st.date_input("End Date", max_date)

#     # Filter dataframe
#     mask = (df["start_time"] >= pd.to_datetime(start_date)) & \
#            (df["start_time"] <= pd.to_datetime(end_date))

#     filtered_df = df[mask]

#     st.markdown(f"**Filtered rows:** {len(filtered_df):,}")

#     # ===========================
#     # 📈 VISUALS (Same Layout)
#     # ===========================
#     st.subheader("Time Trend Visuals")

#     col1, col2 = st.columns(2)

#     # ---- Trips by Hour ----
#     with col1:
#         st.markdown("### Trips by Hour of Day")
#         hour_path = plot_trips_per_hour(filtered_df)
#         st.image(str(hour_path), use_container_width=True)

#     # ---- Trips by Weekday ----
#     with col2:
#         st.markdown("### Trips by Day of Week")
#         weekday_path = plot_trips_per_weekday(filtered_df)
#         st.image(str(weekday_path), use_container_width=True)

#     # ---- Trips by Month ----
#     st.markdown("### Trips per Month")
#     month_path = plot_trips_per_month(filtered_df)
#     st.image(str(month_path), use_container_width=True)

#     # ---- Dev Notes ----
#     st.markdown("---")
#     st.markdown("### Developer Notes")
#     st.info("Visuals generated using Matplotlib and stored in outputs/plots/time_based_analysis/")






# from __future__ import annotations

# import pandas as pd
# import streamlit as st


# def render(df: pd.DataFrame) -> None:
#     st.title("Time-based Trends — Dhruv")

#     st.markdown(
        
#           """
#         This page is owned by **Dhruv**.

#         It will include:
#         - Trip counts by **hour of day**
#         - Patterns by **day of week / weekend vs weekday**
#         - Possibly **monthly/seasonal** 
#         - check Story #8 for more details

#         Ingrid will help here later with design & styling of the charts.
#         """


       
#     )

#     st.subheader("Layout Placeholder")

#     col1, col2 = st.columns(2)
#     with col1:
#         st.markdown("#### Trips by Hour of Day")
#         st.info("TODO (Dhruv): Add line/bar chart of trips vs hour_of_day.")
#     with col2:
#         st.markdown("#### Trips by Day of Week")
#         st.info("TODO (Dhruv): Add chart using weekday / weekend flags.")

#     st.markdown(
        

#              """
#         **Developer notes goes here :**

#         """
       
#     )
