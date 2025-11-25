from data_loader import load_bike_data,save_cleaned_data
from data_cleaning import (standardize_user_type, group_bike_model, parse_datetime_columns, clean_trip_duration,clean_station_fields)



def main():
    df = load_bike_data("toronto-bike.csv")
    df = group_bike_model(df)
    df = parse_datetime_columns(df)
    df = clean_trip_duration(df)
    df = clean_station_fields(df)
    save_cleaned_data(df, "toronto-bike-clean.csv", index=False)


if __name__ == "__main__":
    main()
