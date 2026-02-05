import pandas as pd
import numpy as np

def calculate_bearing(lat1, lon1, lat2, lon2):
    """
    Calculate the bearing between two points.
    All args are in degrees and can be numpy arrays.
    Returns bearing in degrees from North.
    """
    lat1_rad = np.radians(lat1)
    lat2_rad = np.radians(lat2)
    diff_lon_rad = np.radians(lon2 - lon1)

    x = np.sin(diff_lon_rad) * np.cos(lat2_rad)
    y = np.cos(lat1_rad) * np.sin(lat2_rad) - (np.sin(lat1_rad) * np.cos(lat2_rad) * np.cos(diff_lon_rad))

    initial_bearing = np.degrees(np.arctan2(x, y))
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing

def parse_flight_data(csv_path):
    """
    Reads CSV and returns a dictionary of clean numpy arrays 
    and a summary text string.
    """
    df = pd.read_csv(csv_path)
    
    # Extract Coordinates
    if 'Position' in df.columns:
        pos = df['Position'].str.replace('"', '').str.split(',', expand=True)
        lats = pos[0].astype(float).values
        lons = pos[1].astype(float).values
    else:
        lats = df['Latitude'].values
        lons = df['Longitude'].values

    # --- CALCULATE HEADINGS ---
    # We compare point N to point N+1.
    # Create shifted arrays (next_lat, next_lon) for vectorized calculation
    lats_next = np.roll(lats, -1)
    lons_next = np.roll(lons, -1)
    
    # Calculate headings for all points at once
    headings = calculate_bearing(lats, lons, lats_next, lons_next)

    # Fix the last point:
    # np.roll moves the first point to the end, creating a false heading for the last point.
    # We simply repeat the second-to-last heading for the final point.
    if len(headings) > 1:
        headings[-1] = headings[-2]
    else:
        headings[-1] = 0.0 # Single point case
        
    data = {
        'lats': lats,
        'lons': lons,
        'heading': headings,
        'alt': df['Altitude'].values if 'Altitude' in df.columns else [],
        'speed': df['Speed'].values if 'Speed' in df.columns else [],
        'count': len(df)
    }
    
    # Generate Info Text
    info = f"Rows: {len(df)}\n"
    if 'Callsign' in df.columns: info += f"Callsign: {df['Callsign'].iloc[0]}\n"
    if 'Altitude' in df.columns: info += f"Max Alt: {df['Altitude'].max()} ft\n"
    if 'Speed' in df.columns: info += f"Max Speed: {df['Speed'].max()} kts\n"
        
    return data, info