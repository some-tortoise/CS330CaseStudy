### NOT FOR SUBMISSION ONLY FOR VISUALIZING DATA

import pandas as pd
import plotly.express as px

# Read passengers and drivers data into Pandas DataFrames
df_passengers = pd.read_csv("data/passengers.csv", delimiter=',', skiprows=0, low_memory=False)
df_drivers = pd.read_csv("data/drivers.csv", delimiter=',', skiprows=0, low_memory=False)

# Add a new column 'Type' to distinguish between passengers and drivers
df_passengers['Type'] = 'Passenger'
df_drivers['Type'] = 'Driver'

# Concatenate both DataFrames
df_combined = pd.concat([df_passengers, df_drivers], ignore_index=True)

# Create a scatter plot on a Mapbox map using Plotly Express
fig_combined = px.scatter_mapbox(df_combined, 
                                  lat="Source Lat", 
                                  lon="Source Lon", 
                                  zoom=8, 
                                  color="Type",  # Use the 'Type' column for color differentiation
                                  color_discrete_map={"Passenger": "red", "Driver": "blue"},  # Specify colors
                                  height=800,
                                  width=800)

# Customize the map layout
fig_combined.update_layout(mapbox_style="open-street-map")
fig_combined.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})

# Display the interactive plot
fig_combined.show()
