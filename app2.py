import streamlit as st
import pandas as pd
import folium
import branca.colormap as cm
from streamlit_folium import st_folium

df = pd.read_csv("forecast_results1.csv")


# Rename columns as per your new data
df.rename(columns={
    'latitude': 'Latitude',
    'longitude': 'Longitude',
    'month': 'Month',
    'year': 'Year',
    'predicted_goldsteinscore': 'GoldsteinScore'
}, inplace=True)

# Sidebar Filters
st.sidebar.title("Filter")
selected_year = st.sidebar.selectbox("Select Year", sorted(df["Year"].unique()))
selected_month = st.sidebar.selectbox(
    "Select Month",
    options=list(range(1, 13)),
    format_func=lambda x: pd.to_datetime(f"2022-{x}-01").strftime("%B")
)

# Filter data based on selected year and month
filtered = df[(df["Year"] == selected_year) & (df["Month"] == selected_month)]

# Title and subtitle for the map
st.title("Sudan conflict Map")
st.subheader(f"{pd.to_datetime(f'{selected_year}-{selected_month}-01').strftime('%B %Y')}")

if filtered.empty:
    st.warning("No data available.")
else:
      # Define fixed color range for Goldstein Score
    vmin, vmax = -10, 10

    # Reverse color scale: Red (conflict) → Blue (peace)
    colormap = cm.LinearColormap(["red", "yellow", "green", "blue"], vmin=vmin, vmax=vmax)
    colormap.caption = "Predicted Goldstein Score (-10 = Conflict, +10 = Peace)"

    # Create the map centered at a specified location
    m = folium.Map(location=[15, 32], zoom_start=6)
    colormap.add_to(m)

    # Add the circle markers for each location
    for _, row in filtered.iterrows():
        folium.CircleMarker(
            location=[row["Latitude"], row["Longitude"]],
            radius=8,
            color=colormap(row["GoldsteinScore"]),
            fill=True,
            fill_color=colormap(row["GoldsteinScore"]),
            fill_opacity=0.7,
            popup=f"Goldstein Score: {row['GoldsteinScore']:.1f}"
        ).add_to(m)

    # Render the map in the Streamlit app
    st_folium(m, width=700, height=500)
