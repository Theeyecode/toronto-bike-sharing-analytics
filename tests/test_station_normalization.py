import pandas as pd
from station_normalization import normalize_station_name, normalize_station_fields


def test_normalize_station_name_basic():
    assert normalize_station_name(" KING STATION  ") == "King Station"
    assert normalize_station_name("BATHURST & KING") == "Bathurst And King"
    assert normalize_station_name("queen-st.") == "Queen-St"
    assert normalize_station_name(float("nan")) == "Unknown Station"


def test_normalize_station_fields_dataframe():
    df = pd.DataFrame({
        "start_station_name_clean": [" Bloor & Yonge ", "College  Station"],
        "end_station_name_clean": ["Spadina Ave.", "Bay  Station "]
    })

    cleaned = normalize_station_fields(df)

    assert cleaned.loc[0, "start_station_normalized"] == "Bloor And Yonge"
    assert cleaned.loc[1, "start_station_normalized"] == "College Station"

    assert cleaned.loc[0, "end_station_normalized"] == "Spadina Ave"
    assert cleaned.loc[1, "end_station_normalized"] == "Bay Station"