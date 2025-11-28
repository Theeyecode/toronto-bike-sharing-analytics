import plotly.express as px

def plot_trips_per_hour(df):
    fig = px.bar(df, x="start_hour", y="trip_count", title="Trips per Hour")
    return fig

def plot_trips_per_weekday(df):
    fig = px.bar(df, x="start_weekday", y="trip_count", title="Trips by Weekday")
    return fig

def plot_trips_per_month(df):
    fig = px.line(df, x="start_month", y="trip_count", title="Trips per Month")
    fig.update_traces(mode="lines+markers")
    return fig
