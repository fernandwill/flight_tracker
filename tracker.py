# flight_tracker.py
import requests
import json
import pandas as pd
import numpy as np
from bokeh.plotting import figure, show
from bokeh.tile_providers import get_provider, Vendors
from bokeh.models import HoverTool, ColumnDataSource

# Define area coordinates (New York area - smaller, busier region)
lon_min, lat_min = -75.0, 40.0
lon_max, lat_max = -73.0, 42.0

# Function to convert GPS coordinates to web mercator (for map display)
def wgs84_to_web_mercator(df, lon="long", lat="lat"):
    k = 6378137

    # Convert columns to float, bad values become NaN
    df[lon] = pd.to_numeric(df[lon], errors='coerce')
    df[lat] = pd.to_numeric(df[lat], errors='coerce')

    # Drop rows where lon/lat is missing
    df = df.dropna(subset=[lon, lat]).copy()

    # Safely create new columns
    df["x"] = df[lon] * (k * np.pi / 180.0)
    df["y"] = np.log(np.tan((90 + df[lat]) * np.pi / 360.0)) * k

    return df


def wgs84_web_mercator_point(lon, lat):
    k = 6378137
    x = lon * (k * np.pi/180.0)
    y = np.log(np.tan((90 + lat) * np.pi/360.0)) * k
    return x, y

# Create API URL (anonymous access)
url_data = f'https://opensky-network.org/api/states/all'

print("Fetching flight data...")
print(f"API URL: {url_data}")

try:
    # Make the request
    response = requests.get(url_data)
    print(f"Response status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        
        if data['states'] and len(data['states']) > 0:
            print(f"Success! Found {len(data['states'])} flights")
            
            # Convert to pandas DataFrame
            col_names = ['icao24', 'callsign', 'origin_country', 'time_position', 'last_contact', 
                        'long', 'lat', 'baro_altitude', 'on_ground', 'velocity', 'true_track', 
                        'vertical_rate', 'sensors', 'geo_altitude', 'squawk', 'spi', 'position_source']
            
            flight_df = pd.DataFrame(data['states'], columns=col_names)
            flight_df[["callsign", "origin_country"]] = flight_df[["callsign", "origin_country"]].fillna('No Data')
            
            print("\nFlight data preview:")
            print(flight_df[['callsign', 'origin_country', 'long', 'lat', 'velocity', 'baro_altitude']].head())
            
            print(f"\nTotal flights: {len(flight_df)}")
            print(f"Countries: {flight_df['origin_country'].unique()}")
            
            # Convert coordinates for map display
            flight_df = wgs84_to_web_mercator(flight_df)
            
            # Convert map boundaries
            xy_min = (-20000000, -10000000)
            xy_max = (20000000, 10000000)
            
            # Create the map
            print("\nCreating map...")
            p = figure(
                x_range=[xy_min[0], xy_max[0]], 
                y_range=[xy_min[1], xy_max[1]],
                x_axis_type='mercator', 
                y_axis_type='mercator',
                width=800, 
                height=600,
                title="Flight Tracker - Global"
            )
            
            # Add map tiles
            tile_provider = get_provider(Vendors.CARTODBPOSITRON)
            p.add_tile(tile_provider)
            
            # Create data source for Bokeh
            flight_source = ColumnDataSource(flight_df)
            
            # Plot aircraft as circles
            p.circle('x', 'y', source=flight_source, 
                    size=8, fill_color='red', fill_alpha=0.7, 
                    line_color='darkred', line_width=1)
            
            # Add hover tool
            hover = HoverTool(tooltips=[
                ('Callsign', '@callsign'),
                ('Country', '@origin_country'),
                ('Velocity (m/s)', '@velocity'),
                ('Altitude (m)', '@baro_altitude')
            ])
            p.add_tools(hover)
            
            print("Displaying map...")
            show(p)
            
        else:
            print("No flights found in this area")
    else:
        print(f"API request failed with status {response.status_code}")
        
except Exception as e:
    print(f"Error: {e}")