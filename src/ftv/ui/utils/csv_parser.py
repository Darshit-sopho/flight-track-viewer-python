import pandas as pd

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
        
    data = {
        'lats': lats,
        'lons': lons,
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