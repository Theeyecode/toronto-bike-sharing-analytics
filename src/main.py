from data_loader import load_bike_data
from data_cleaning import (standardize_user_type, group_bike_model, parse_datetime_columns,)



def main():
    df = load_bike_data("toronto-bike.csv")
    df = group_bike_model(df)
    df = parse_datetime_columns(df)
    print("Shape:", df.shape)
    print(df[["Start Time", "End Time", "start_time", "end_time"]].head())


    
    # validation will come here

if __name__ == "__main__":
    main()
