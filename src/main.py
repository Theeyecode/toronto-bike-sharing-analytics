from data_loader import load_bike_data, save_cleaned_data
from data_cleaning import (
    standardize_user_type,
    group_bike_model,
    parse_datetime_columns,
    clean_trip_duration,
    clean_station_fields,
)
from feature_engineering import (
    compute_distance_fields,
    add_time_features,
    add_weekend_flag,
    add_rush_hour_flag,
)
from station_normalization import normalize_station_fields
from analysis import (
    summarize_trip_duration_by_user_type,
    get_peak_stations_by_user_type,
    summarize_time_of_day_by_user_type,
)
    # 🔹 Limpieza / enriquecimiento base
from visualizations import (
    plot_hourly_demand,
    plot_trip_duration_distribution,
    plot_top_busiest_stations,
    plot_user_type_comparison,
    plot_daily_trips_decomposition,
)

from plots_time import (
    plot_trips_per_hour,
    plot_trips_per_weekday,
    plot_trips_per_month,   
)

from time_analysis import (
    trips_per_hour,
    trips_per_weekday,
    trips_per_month,
)
def main():
    df = load_bike_data("toronto-bike.csv")
    df = standardize_user_type(df)
    df = group_bike_model(df)
    df = parse_datetime_columns(df)
    df = clean_trip_duration(df)
    df = clean_station_fields(df)
    df = normalize_station_fields(df)
    save_cleaned_data(df, "toronto-bike-clean.csv", index=False)

    # 🔹 AQUÍ estandarizamos el tipo de usuario (IMPORTANTE)
    df = standardize_user_type(df)

    # 🔹 Feature engineering
    df = compute_distance_fields(df)
    df = add_time_features(df)
    df = add_weekend_flag(df)
    df = add_rush_hour_flag(df)

    # Time-based Analysis Visualizations
    trips_per_hour_df = trips_per_hour(df)
    trips_per_weekday_df = trips_per_weekday(df)
    trips_per_month_df = trips_per_month(df)    

    plot_trips_per_hour(trips_per_hour_df)
    plot_trips_per_weekday(trips_per_weekday_df)
    plot_trips_per_month(trips_per_month_df)

    # 🔹 DEBUG rápido: ver columnas disponibles
    print("\nColumns in df right before analysis:")
    print(df.columns)

    # 🔹 Análisis
    duration_summary = summarize_trip_duration_by_user_type(df)
    peak_stations = get_peak_stations_by_user_type(df, top_n=10)
    time_of_day_summary = summarize_time_of_day_by_user_type(df)

    print("\n=== Trip Duration Summary by User Type ===")
    print(duration_summary.head())

    print("\n=== Peak START Stations by User Type ===")
    print(peak_stations["start_stations"].head())

    print("\n=== Peak END Stations by User Type ===")
    print(peak_stations["end_stations"].head())

    print("\n=== Time-of-Day vs User Type Summary (first rows) ===")
    print(time_of_day_summary.head())

    plot_hourly_demand(df)
    plot_trip_duration_distribution(df)
    plot_top_busiest_stations(df)
    plot_user_type_comparison(df)
    plot_daily_trips_decomposition(df)

    
    
if __name__ == "__main__":
     main()
