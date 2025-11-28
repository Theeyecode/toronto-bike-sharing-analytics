from data_loader import load_bike_data,save_cleaned_data
from data_cleaning import (standardize_user_type, group_bike_model, parse_datetime_columns, clean_trip_duration,clean_station_fields)
from feature_engineering import (
    compute_distance_fields,
    add_time_features,
    add_weekend_flag,
    add_rush_hour_flag,
)
from station_normalization import normalize_station_fields
from visualizations import (
    plot_hourly_demand,
    plot_trip_duration_distribution,
    plot_top_busiest_stations,
    plot_user_type_comparison,
    plot_daily_trips_decomposition,
)

def main():
    df = load_bike_data("toronto-bike.csv")
    df = standardize_user_type(df)
    df = group_bike_model(df)
    df = parse_datetime_columns(df)
    df = clean_trip_duration(df)
    df = clean_station_fields(df)
    df = normalize_station_fields(df)


    df = compute_distance_fields(df)
    df = add_time_features(df)
    df = add_weekend_flag(df)
    df = add_rush_hour_flag(df)
    

    plot_hourly_demand(df)
    plot_trip_duration_distribution(df)
    plot_top_busiest_stations(df)
    plot_user_type_comparison(df)
    plot_daily_trips_decomposition(df)

    save_cleaned_data(df, "toronto-bike-clean.csv", index=False)
    
    if __name__ == "__main__":
    main()
